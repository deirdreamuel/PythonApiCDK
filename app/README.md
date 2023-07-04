# Python Stock API Buy/Sell Notifications Project

## Overview

This project is a Python Stock API deployed using AWS CDK. This project uses AWS Lambda with API Gateway. The following code is using `{proxy+}` functionality and uses [Serverless WSGI](https://www.serverless.com/plugins/serverless-wsgi) with [Flask](https://flask.palletsprojects.com/en/2.3.x/).

## Prerequisites

1. Python >= 3.9

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

## Running Project
```
flask run --app src --debug run
```