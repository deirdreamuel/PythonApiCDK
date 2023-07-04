#!/usr/bin/env python3
import aws_cdk as cdk

from infra.stock_api_stack import StockApiStack


app = cdk.App()

StockApiStack(
    app,
    "StockApiStack",
    env=cdk.Environment(account="582250362323", region="us-east-1"),
)

app.synth()
