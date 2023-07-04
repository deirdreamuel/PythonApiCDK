from aws_cdk import Stack, aws_lambda, aws_apigateway as apigw, BundlingOptions
from constructs import Construct


class StockApiStack(Stack):
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
                        "pip install --no-cache -r requirements.txt -t /asset-output && cp -au . /asset-output",
                    ],
                ),
            ),
            handler="src.handler",
            memory_size=1024,
        )

        # Create API Gateway
        apigw.LambdaRestApi(
            self,
            "StockApiGateway",
            handler=fn,
        )
