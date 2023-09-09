import aws_cdk as cdk

from infra.stack import AppStack


app = cdk.App()

AppStack(
    app,
    "StockApiStack",
    env=cdk.Environment(account="582250362323", region="us-east-1"),
)

app.synth()
