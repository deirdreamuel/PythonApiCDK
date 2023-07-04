# Python Stock API Buy/Sell Notifications Project with AWS CDK

## Overview

This project is a Python Stock API deployed using AWS CDK.
This project uses AWS Step Functions to call the API and notify with SES and SMS.

The application code for the Lambda API is in `app` directory

## Prerequisites

1. Python >= 3.9
2. AWS CDK

## Setup

To manually create a virtualenv on MacOS and Linux:

```
python3 -m venv .venv
```

After the virtualenv is created, use the following
command to activate your virtualenv.

```
source .venv/bin/activate
```

Once the virtualenv is activated, install the required dependencies.

```
pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
cdk synth
```

## Useful commands

- `cdk ls` list all stacks in the app
- `cdk synth` emits the synthesized CloudFormation template
- `cdk deploy` deploy this stack to your default AWS account/region
- `cdk diff` compare deployed stack with current state
- `cdk docs` open CDK documentation
