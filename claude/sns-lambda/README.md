# AWS SNS and Lambda with aws-syndicate

This task involves creating the Lambda integration with an SNS topic. 'SNS Handler' Lambda should be triggered by an SNS topic and log the message content to CloudWatch Logs.

Architecture:

- SNS topic 'lambda_topic' -> AWS Lambda 'sns_handler'

Additional information:

- [aws-syndicate > wiki](https://github.com/epam/aws-syndicate/wiki)
- [pypi.org > aws-syndicate](https://pypi.org/project/aws-syndicate/)

## Prompt

According to README.md:

- Build a solution to resolve the task 'AWS SNS and Lambda with aws-syndicate'.
- Generate YAML and JSON examples and use the aws-syndicate CLI. Configure the solution (as per the `Objectives` section).
- Using AWS API calls, check if all necessary resources, permissions and policies that they are already configured (as per the `Task Resources` section).
- Verify the solution using the AWS Console and API calls.

## TOC

- [AWS SNS and Lambda with aws-syndicate](#aws-sns-and-lambda-with-aws-syndicate)
  - [Prompt](#prompt)
  - [TOC](#toc)
  - [Requirements](#requirements)
    - [Objectives](#objectives)
    - [Task Resources](#task-resources)
    - [AWS-Syndicate Aliases Usage](#aws-syndicate-aliases-usage)
    - [Lambda Versions \& Aliases](#lambda-versions--aliases)
    - [Task Verification](#task-verification)
  - [Prerequisites](#prerequisites)
    - [Install Python](#install-python)
    - [Install AWS-Syndicate](#install-aws-syndicate)
  - [Temporary credentials](#temporary-credentials)
    - [Task verification](#task-verification-1)
    - [Sandbox programmatic credentials](#sandbox-programmatic-credentials)
    - [Sandbox verification credentials](#sandbox-verification-credentials)
      - [Update Credentials](#update-credentials)
  - [Implementation](#implementation)
    - [1. Generate project](#1-generate-project)
    - [2. Generate config](#2-generate-config)
      - [2a. Set environment variables](#2a-set-environment-variables)
      - [2b. Check resources\_prefix and resources\_suffix in the syndicate.yml file](#2b-check-resources_prefix-and-resources_suffix-in-the-syndicateyml-file)
      - [2c. Change lambdas\_alias\_name in the syndicate\_aliases.yml file](#2c-change-lambdas_alias_name-in-the-syndicate_aliasesyml-file)
    - [3. Generate 'SNS Topic' Lambda Function](#3-generate-sns-topic-lambda-function)
    - [4. Generate SNS Topic Resource in Meta](#4-generate-sns-topic-resource-in-meta)
      - [4a. Change sns\_topic meta-data in the deployment\_resources.json file](#4a-change-sns_topic-meta-data-in-the-deployment_resourcesjson-file)
      - [4b. Change iam\_policy in the deployment\_resources.json file](#4b-change-iam_policy-in-the-deployment_resourcesjson-file)
    - [5. Configure Lambda to be Triggered by the Topic](#5-configure-lambda-to-be-triggered-by-the-topic)
    - [6. Implement Lambda Function Code](#6-implement-lambda-function-code)
    - [7. Deploy the Solution](#7-deploy-the-solution)
    - [8. Verification Steps](#8-verification-steps)
      - [8.1. AWS CLI Verification](#81-aws-cli-verification)
      - [8.2. Test the Integration](#82-test-the-integration)
      - [8.3. Check CloudWatch Logs](#83-check-cloudwatch-logs)
      - [8.4. AWS Console Verification](#84-aws-console-verification)
      - [8.5. Cleanup](#85-cleanup)
    - [9. Complete Project Structure](#9-complete-project-structure)
    - [10. Troubleshooting](#10-troubleshooting)
  - [Results](#results)


## Requirements

### Objectives

1. Use aws-syndicate framework.
2. Create an 'SNS Handler' Lambda that logs messages from an SNS topic.
3. Check with AWS Console
4. Check with AWS CLI

### Task Resources

Please note it is obligatory to stick to the following resources naming in order to pass the task:

- Lambda Function: sns_handler
- SNS Queue: lambda_topic

### AWS-Syndicate Aliases Usage

During verification, the following AWS-Syndicate aliases will be used:

- ./.syndicate-config-dev/syndicate_aliases.yml

```bash
lambdas_alias_name: learn
```

### Lambda Versions & Aliases

Please, make sure that your deployment resources define Lambda to be deployed with Version (Lambda Version) and Alias (Lambda Alias). It is required for the task verification to pass. Note, that usage of the Lambda Versions & Aliases is a best practice of lambdas management, so do not neglect to deep dive into versions and aliases management.

AWS-Syndicate project examples where Lambda Aliases are used:

- [Python](https://github.com/epam/aws-syndicate/tree/master/examples/python/lambda-cognito-api-gateway)

### Task Verification

To make sure everything is set up correctly, test your API by using a web-browser to invoke it.

Important Note:

- When a Lambda function is deployed with an alias, all related configurations—such as triggers, URL settings, and other resources—are linked to the alias, not the function itself.
- Always check configurations at the alias level to ensure proper functionality.
- To view the configuration, navigate to the Lambda function page in the AWS console. Ensure you are in the correct region, then open your Lambda function configuration. Once opened, switch to the Aliases tab and click on the alias name to view its configuration settings.

## Prerequisites

### Install Python

```bash
sudo apt install python3
sudo apt install python3-pip
```

### Install AWS-Syndicate

- Install from repo

```bash
pip3 install aws-syndicate
```

- Install from AWS

```bash
# from source code
git clone https://github.com/epam/aws-syndicate.git
python3 -m venv syndicate_venv
source syndicate_venv/bin/activate
pip3 install aws-syndicate/.
mvn install -f aws-syndicate/plugin/
```

## Temporary credentials

### Task verification

Verification resource naming:

- Prefix: cmtr-ze58tzcf-
- Suffix: -k3vb
- Region: eu-west-1

The suffix will be added automatically. Please don't duplicate it.

### Sandbox programmatic credentials

```bash
syndicate generate config --name "dev" \
    --region "eu-west-1" \
    --bundle_bucket_name "syndicate-education-platform-custom-sandbox-artifacts-7114/ze58tzcf/task04" \
    --prefix "cmtr-ze58tzcf-" \
    --suffix "-k3vb" \
    --extended_prefix "true" \
    --tags "run_id:Global-09,task_id:task04,topic_id:stm,user_id:ze58tzcf" \
    --access_key "" \
    --secret_key "" \
    --session_token ""
```

### Sandbox verification credentials

- [Console](https://signin.aws.amazon.com/federation?Action=login&Issuer=Example.org&Destination=https%3A%2F%2Feu-west-1.console.aws.amazon.com%2F&SigninToken=TS)

- Linux

```bash
export AWS_ACCESS_KEY_ID=""
export AWS_SECRET_ACCESS_KEY=""
export AWS_SESSION_TOKEN=""
```

#### Update Credentials

> ./.syndicate-config-dev/syndicate.yml

- expiration:
- temp_aws_access_key_id:
- temp_aws_secret_access_key:
- temp_aws_session_token:

## Implementation

### 1. Generate project

```bash
syndicate generate project --help
syndicate generate project --name sns-lambda
```

### 2. Generate config

```bash
cd sns-lambda
```

- [Run Sandbox programmatic credentials](#sandbox-programmatic-credentials)

#### 2a. Set environment variables

- Set SDCT_CONF environment variable

```bash
export SDCT_CONF="/home/ik/aws-syndicate/claude/sns-lambda/.syndicate-config-dev"
```

#### 2b. Check resources_prefix and resources_suffix in the syndicate.yml file

- ./.syndicate-config-dev/syndicate_aliases.yml

```bash
resources_prefix: cmtr-ze58tzcf-
resources_suffix: -k3vb
```

#### 2c. Change lambdas_alias_name in the syndicate_aliases.yml file

- ./.syndicate-config-dev/syndicate_aliases.yml

```bash
lambdas_alias_name: learn
```

### 3. Generate 'SNS Topic' Lambda Function

Inside your project, use aws-syndicate to [generate a Lambda function](https://github.com/epam/aws-syndicate/wiki/2.-Quick-start#224-creating-lambda-files) named 'sns_handler'. This step creates the necessary files and configurations for the Lambda.

```bash
syndicate generate lambda --name sns_handler --runtime python
```

### 4. Generate SNS Topic Resource in Meta

Use aws-syndicate to [generate metadata for an SNS topic resource](https://github.com/epam/aws-syndicate/wiki/4.-Resources-Meta-Descriptions#46-sns-topic).

- SNS Topic: sns_topic

```bash
# sns_topic
syndicate generate meta sns_topic --help
syndicate generate meta sns_topic --resource_name lambda_topic --region eu-west-1
```

- IAM policy
- cmtr-ze58tzcf-

```bash
syndicate generate meta iam_policy --help
```

#### 4a. Change sns_topic meta-data in the deployment_resources.json file

```json
{
  "lambda_topic": {
    "resource_type": "sns_topic",
    "region": "eu-west-1",
    "display_name": "Lambda Topic",
    "delivery_policy": {
      "healthyRetryPolicy": {
        "minDelayTarget": 20,
        "maxDelayTarget": 20,
        "numRetries": 3,
        "numMaxDelayRetries": 0,
        "numMinDelayRetries": 0,
        "numNoDelayRetries": 0,
        "backoffFunction": "linear"
      }
    },
    "policy": {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Principal": "*",
          "Action": [
            "sns:Publish",
            "sns:Subscribe"
          ],
          "Resource": "*"
        }
      ]
    },
    "tags": {}
  }
}
```

#### 4b. Change iam_policy in the deployment_resources.json file

```json
{
  "lambda-basic-execution": {
    "resource_type": "iam_policy",
    "policy_content": {
      "Statement": [
        {
          "Action": [
            "logs:CreateLogGroup",
            "logs:CreateLogStream",
            "logs:PutLogEvents",
            "dynamodb:GetItem",
            "dynamodb:Query",
            "dynamodb:PutItem",
            "dynamodb:Batch*",
            "dynamodb:DeleteItem",
            "ssm:PutParameter",
            "ssm:GetParameter",
            "kms:Decrypt",
            "sns:Receive",
            "sns:GetTopicAttributes"
          ],
          "Effect": "Allow",
          "Resource": "*"
        }
      ],
      "Version": "2012-10-17"
    },    
    "tags": {}
  }
}
```

### 5. Configure Lambda to be Triggered by the Topic

Complete Lambda configuration in deployment_resources.json:

```json
{
  "sns_handler": {
    "version": "1.0",
    "name": "sns_handler",
    "func_name": "handler.lambda_handler",
    "resource_type": "lambda",
    "iam_role_name": "sns_handler-role",
    "runtime": "python3.10",
    "memory": 128,
    "timeout": 100,
    "lambda_path": "lambdas/sns_handler",
    "dependencies": [],
    "event_sources": [
      {
        "resource_type": "sns_topic_trigger",
        "target_topic": "lambda_topic"
      }
    ],
    "env_variables": {},
    "publish_version": true,
    "alias": "${lambdas_alias_name}",
    "url_config": {},
    "ephemeral_storage": 512,
    "logs_expiration": "${logs_expiration}",
    "tags": {}
  }
}
```

### 6. Implement Lambda Function Code

Create the Lambda function code in `src/sns_handler.py`:

- Option 1 (Simple and tested)

```python
import json

def lambda_handler(event, context):
    for record in event['Records']:
        sns_message = record['Sns']['Message']
        print(f"Received SNS message: {sns_message}")
    return {
        'statusCode': 200,
        'body': json.dumps('SNS message processed successfully!')
    }
```

- Option 2 (Detailed logging)

```python
import json
import logging

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    SNS Handler Lambda function
    Processes messages from SNS topic and logs them to CloudWatch
    """
    
    logger.info(f"Received event: {json.dumps(event, indent=2)}")
    
    # Process each record from SNS
    for record in event['Records']:
        # Extract SNS message details
        sns = record['Sns']
        message = sns['Message']
        subject = sns.get('Subject', 'No Subject')
        topic_arn = sns['TopicArn']
        message_id = sns['MessageId']
        timestamp = sns['Timestamp']
        
        # Log message content
        logger.info(f"Processing SNS message ID: {message_id}")
        logger.info(f"Topic ARN: {topic_arn}")
        logger.info(f"Subject: {subject}")
        logger.info(f"Message: {message}")
        logger.info(f"Timestamp: {timestamp}")
        
        # Process the message (add your business logic here)
        try:
            # Parse JSON message if applicable
            if message.startswith('{'):
                parsed_message = json.loads(message)
                logger.info(f"Parsed JSON message: {parsed_message}")
            else:
                logger.info(f"Plain text message: {message}")
                
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON message: {e}")
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            raise e
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': f'Successfully processed {len(event["Records"])} SNS messages'
        })
    }
```

### 7. Deploy the Solution

```bash
# Package and deploy
syndicate build
syndicate deploy --deploy_name sns-lambda-dev
```

### 8. Verification Steps

#### 8.1. AWS CLI Verification

Check if resources are created:

```bash
# Check Lambda function
aws lambda get-function --function-name cmtr-ze58tzcf-sns_handler-k3vb --region eu-west-1

# Check Lambda alias
aws lambda get-alias --function-name cmtr-ze58tzcf-sns_handler-k3vb --name learn --region eu-west-1

# Check SNS topic
aws sns list-topics --region eu-west-1 | grep cmtr-ze58tzcf-lambda_topic-k3vb

# Get topic ARN
TOPIC_ARN=$(aws sns list-topics --region eu-west-1 --query 'Topics[?contains(TopicArn, `cmtr-ze58tzcf-lambda_topic-k3vb`)].TopicArn' --output text)

# Check topic attributes
aws sns get-topic-attributes --topic-arn $TOPIC_ARN --region eu-west-1

# Check topic subscriptions
aws sns list-subscriptions-by-topic --topic-arn $TOPIC_ARN --region eu-west-1

# Check IAM role
aws iam get-role --role-name cmtr-ze58tzcf-sns_handler-role-k3vb --region eu-west-1
```

#### 8.2. Test the Integration

Send a test message to SNS topic:

```bash
# Get topic ARN
TOPIC_ARN=$(aws sns list-topics --region eu-west-1 --query 'Topics[?contains(TopicArn, `cmtr-ze58tzcf-lambda_topic-k3vb`)].TopicArn' --output text)

# Send test message with subject
aws sns publish --topic-arn $TOPIC_ARN --message '{"test": "Hello from SNS!", "timestamp": "2024-01-01T12:00:00Z"}' --subject "Test Message" --region eu-west-1

# Send another test message
aws sns publish --topic-arn $TOPIC_ARN --message 'Plain text message for testing SNS-Lambda integration' --subject "Plain Text Test" --region eu-west-1

# Send message without subject
aws sns publish --topic-arn $TOPIC_ARN --message 'Message without subject' --region eu-west-1
```

#### 8.3. Check CloudWatch Logs

```bash
# List log groups
aws logs describe-log-groups --log-group-name-prefix "/aws/lambda/cmtr-ze58tzcf-sns_handler-k3vb" --region eu-west-1

# Get recent log events
LOG_GROUP="/aws/lambda/cmtr-ze58tzcf-sns_handler-k3vb"
aws logs describe-log-streams --log-group-name $LOG_GROUP --order-by LastEventTime --descending --region eu-west-1

# Get latest log stream
LATEST_STREAM=$(aws logs describe-log-streams --log-group-name $LOG_GROUP --order-by LastEventTime --descending --max-items 1 --query 'logStreams[0].logStreamName' --output text --region eu-west-1)

# Get log events
aws logs get-log-events --log-group-name $LOG_GROUP --log-stream-name $LATEST_STREAM --region eu-west-1
```

#### 8.4. AWS Console Verification

1. **Lambda Function:**
   - Navigate to AWS Lambda Console
   - Find function: `cmtr-ze58tzcf-sns_handler-k3vb`
   - Check Aliases tab for `learn` alias
   - Verify SNS trigger configuration
   - Check function permissions and execution role

2. **SNS Topic:**
   - Navigate to AWS SNS Console
   - Find topic: `cmtr-ze58tzcf-lambda_topic-k3vb`
   - Check topic subscriptions (should show Lambda function)
   - Verify topic permissions and delivery policy
   - Test publishing messages from console

3. **CloudWatch Logs:**
   - Navigate to CloudWatch Logs Console
   - Check log group: `/aws/lambda/cmtr-ze58tzcf-sns_handler-k3vb`
   - Verify message processing logs appear after publishing SNS messages
   - Check for any error logs or execution timeouts

#### 8.5. Cleanup

```bash
# Clean up resources
syndicate clean --deploy_name sns-lambda-dev
```

### 9. Complete Project Structure

```bash
sns-lambda/
├── .syndicate-config-dev/
│   ├── syndicate.yml
│   └── syndicate_aliases.yml
├── deployment_resources.json
├── src/
│   └── sns_handler.py
└── README.md
```

### 10. Troubleshooting

Common issues and solutions:

1. **Permission Denied:** Ensure Lambda execution role has necessary SNS permissions
2. **Lambda Not Triggered:** Check SNS topic subscription and confirm Lambda function is subscribed
3. **Logs Not Appearing:** Verify CloudWatch Logs permissions in IAM role
4. **Topic Not Found:** Check resource naming with prefix/suffix matches exactly
5. **Subscription Failed:** Ensure Lambda function exists before creating SNS subscription
6. **Dead Letter Queue:** Consider adding DLQ for failed message processing

**Additional Verification Commands:**

```bash
# Check if subscription is confirmed
aws sns get-subscription-attributes --subscription-arn $(aws sns list-subscriptions-by-topic --topic-arn $TOPIC_ARN --query 'Subscriptions[0].SubscriptionArn' --output text) --region eu-west-1

# Check Lambda function policy
aws lambda get-policy --function-name cmtr-ze58tzcf-sns_handler-k3vb:learn --region eu-west-1
```

This completes the AWS SNS and Lambda integration using aws-syndicate framework.

## Results

The solution Successfully tested the AWS SNS and Lambda integration with aws-syndicate!

1. ✅ Set up the SNS topic (`lambda_topic`) and Lambda function (`sns_handler`)
2. ✅ Configure the proper event source mapping between SNS and Lambda
3. ✅ Deploy using aws-syndicate with correct resource naming and aliases
4. ✅ Test the integration and verify message processing in CloudWatch Logs

The SNS-Lambda pattern is very useful for building event-driven architectures and decoupled systems. Having both SQS-Lambda and SNS-Lambda solutions in your aws-syndicate toolkit gives you flexibility for different messaging patterns:

- **SNS-Lambda**: Great for fanout scenarios, notifications, and pub/sub patterns
- **SQS-Lambda**: Ideal for reliable message processing, queuing, and batch processing
