from aws_cdk import (
    CfnOutput,
    Duration,
    Stack,
    aws_apigateway,
    aws_dynamodb,
    aws_events,
    aws_events_targets,
    aws_iam,
    aws_lambda,
    aws_route53,
    aws_ses,
    aws_stepfunctions,
    aws_stepfunctions_tasks,
    BundlingOptions,
)
from constructs import Construct


class AppStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create the Lambda function to receive the request
        fn = aws_lambda.Function(
            self,
            "StockApiLambda",
            function_name="StockApiLambda",
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            code=aws_lambda.Code.from_asset(
                "app",
                bundling=BundlingOptions(
                    image=aws_lambda.Runtime.PYTHON_3_9.bundling_image,
                    command=[
                        "bash",
                        "-c",
                        "cp -au . /asset-output && cd /asset-output && make clean && make clean-virtualenv && pip install --no-cache -r requirements.txt -t .",
                    ],
                ),
            ),
            handler="src.handler",
            memory_size=1024,
            environment={
                "DYNAMODB_ENDPOINT": "https://dynamodb.us-east-1.amazonaws.com",
            },
        )

        # Create API Gateway
        api = aws_apigateway.LambdaRestApi(
            self,
            "StockApiGateway",
            handler=fn,
        )

        # Step functions Definition
        call_api_state = aws_stepfunctions_tasks.CallApiGatewayRestApiEndpoint(
            self,
            "Call REST API endpoint",
            api=api,
            method=aws_stepfunctions_tasks.HttpMethod.POST,
            stage_name="prod",
            api_path="/daily-notifications",
        )

        fail_state = aws_stepfunctions.Fail(
            self,
            "Fail",
            cause="AWS Batch Job Failed",
            error="DescribeJob returned FAILED",
        )

        success_state = aws_stepfunctions.Succeed(
            self, "Succeeded", comment="AWS Job succeeded"
        )

        # Create step functions state conditions
        definition = call_api_state.add_catch(fail_state, errors=["States.ALL"]).next(
            success_state
        )

        # Create state machine
        state_machine = aws_stepfunctions.StateMachine(
            self,
            "StockApiNotificationsStateMachine",
            definition=definition,
            timeout=Duration.minutes(5),
        )

        # Create a CloudWatch Event Rule
        rule = aws_events.Rule(
            self,
            "StockApiStateMachineTriggerCronRule",
            schedule=aws_events.Schedule.cron(hour="15", minute="0"),
        )

        # Add a target to the rule that triggers the state machine
        rule.add_target(aws_events_targets.SfnStateMachine(state_machine))

        # Output the ARN of the state machine
        CfnOutput(self, "StateMachineArn", value=state_machine.state_machine_arn)

        my_hosted_zone = aws_route53.HostedZone.from_lookup(
            self, "MyHostedZone", domain_name="amuel.org"
        )

        aws_ses.EmailIdentity(
            self,
            "EmailIdentity",
            identity=aws_ses.Identity.public_hosted_zone(my_hosted_zone),
        )

        fn.add_to_role_policy(
            aws_iam.PolicyStatement(
                effect=aws_iam.Effect.ALLOW,
                actions=["ses:SendEmail", "ses:SendRawEmail"],
                resources=["*"],
            )
        )

        aws_dynamodb.Table(
            self,
            "DynamoDBSubscriptionsTable",
            table_name="SUBSCRIPTIONS",
            partition_key=aws_dynamodb.Attribute(
                name="PK", type=aws_dynamodb.AttributeType.STRING
            ),
            sort_key=aws_dynamodb.Attribute(
                name="SK", type=aws_dynamodb.AttributeType.STRING
            ),
            billing_mode=aws_dynamodb.BillingMode.PAY_PER_REQUEST
        )
