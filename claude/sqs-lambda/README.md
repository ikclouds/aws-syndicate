# AWS SQS and Lambda with aws-syndicate

This task involves creating the Lambda integration with SQS queue. The 'SQS Handler' Lambda should be triggered by an SQS queue and log the message content to CloudWatch Logs.

Architecture:

- SQS queue 'async_queue' -> AWS Lambda 'sqs_handler'

Additional information:

- [aws-syndicate > wiki](https://github.com/epam/aws-syndicate/wiki)
- [pypi.org > aws-syndicate](https://pypi.org/project/aws-syndicate/)

## Prompt

According to README.md:

- Build a solution to resolve the task 'AWS SQS and Lambda with aws-syndicate'.
- Generate YAML and JSON examples and use the aws-syndicate CLI. Configure the solution (as per the `Objectives` section).
- Using AWS API calls, check if all necessary resources, permissions and policies that they are already configured (as per the `Task Resources` section).
- Verify the solution using the AWS Console and API calls.

## TOC

## Requirements

### Objectives

1. Use aws-syndicate framework.
2. Create an 'SQS Handler' Lambda that logs messages from an SQS queue.
3. Check with AWS Console
4. Check with AWS CLI

### Task Resources

Please note it is obligatory to stick to the following resources naming in order to pass the task:

- Lambda Function: sqs_handler
- SQS Queue: async_queue

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
syndicate generate project --name sqs-lambda
```

### 2. Generate config

```bash
cd sqs-lambda
```

- [Run Sandbox programmatic credentials](#sandbox-programmatic-credentials)

#### 2a. Set environment variables

- Set SDCT_CONF environment variable

```bash
export SDCT_CONF="/home/ik/aws-syndicate/claude/sqs-lambda/.syndicate-config-dev"
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

### 3. Generate 'SQS Handler' Lambda Function

Inside your project, use aws-syndicate to [generate a Lambda function](https://github.com/epam/aws-syndicate/wiki/2.-Quick-start#224-creating-lambda-files) named 'SQS Handler'. This step creates the necessary files and configurations for the Lambda.

```bash
syndicate generate lambda --name sqs_handler --runtime python
```

### 4. Generate SQS Queue Resource in Meta

Use aws-syndicate to [generate metadata for an SQS queue resource](https://github.com/epam/aws-syndicate/wiki/4.-Resources-Meta-Descriptions#412-sqs-queue).

- SQS Queue: async_queue

```bash
# sqs_queue
syndicate generate meta sqs_queue --help
syndicate generate meta sqs_queue --resource_name async_queue --visibility_timeout 100
```

- IAM policy
- cmtr-ze58tzcf-

```bash
syndicate generate meta iam_policy --help
# syndicate generate meta iam_policy --resource_name async_queue_policy
# syndicate generate meta iam_policy --resource_name sqs_handler_policy
```

#### 4a. Change sqs_queue meta-data in the deployment_resources.json file

```json
{
    "async_queue": {
    "resource_type": "sqs_queue",
    "fifo_queue": false,
    "visibility_timeout": 100,
    "delay_seconds": 0,
    "maximum_message_size": 1024,
    "message_retention_period": 60,
    "receive_message_wait_time_seconds": 0,
    "policy": {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Principal": "*",
          "Action": [
            "sqs:SendMessage"
          ],
          "Resource": "*"
        }
      ]
    },
    "redrive_policy": {},
    "content_based_deduplication": false,
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
            "sqs:ReceiveMessage",
            "sqs:DeleteMessage",
            "sqs:GetQueueAttributes"
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

### 5. Configure Lambda to be Triggered by the Queue

Complete Lambda configuration in deployment_resources.json:

```json
{
    "version": "1.0",
    "name": "sqs_handler",
    "func_name": "handler.lambda_handler",
    "resource_type": "lambda",
    "iam_role_name": "sqs_handler-role",
    "runtime": "python3.10",
    "memory": 128,
    "timeout": 100,
    "lambda_path": "lambdas/sqs_handler",
    "dependencies": [],
    "event_sources": [
        {
            "resource_type": "sqs_trigger",
            "target_queue": "async_queue",
            "batch_size": 10,
            "maximum_batching_window_in_seconds": 5
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
```

### 6. Implement Lambda Function Code

Create the Lambda function code in `src/sqs_handler.py`:

- Option 1 (tested)

```python
import json

def lambda_handler(event, context):
    for record in event['Records']:
        message_body = record['body']
        print(f"Received SQS message: {message_body}")
    return {
        'statusCode': 200,
        'body': json.dumps('SQS message processed successfully!')
    }
```

- Option 2

```python
import json
import logging

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    SQS Handler Lambda function
    Processes messages from SQS queue and logs them to CloudWatch
    """
    
    logger.info(f"Received event: {json.dumps(event, indent=2)}")
    
    # Process each record from SQS
    for record in event['Records']:
        # Extract message details
        message_body = record['body']
        message_id = record['messageId']
        receipt_handle = record['receiptHandle']
        
        # Log message content
        logger.info(f"Processing message ID: {message_id}")
        logger.info(f"Message body: {message_body}")
        logger.info(f"Receipt handle: {receipt_handle}")
        
        # Process the message (add your business logic here)
        try:
            # Parse JSON message if applicable
            if message_body.startswith('{'):
                parsed_message = json.loads(message_body)
                logger.info(f"Parsed JSON message: {parsed_message}")
            else:
                logger.info(f"Plain text message: {message_body}")
                
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON message: {e}")
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            raise e
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': f'Successfully processed {len(event["Records"])} messages'
        })
    }
```

### 7. Deploy the Solution

```bash
# Package and deploy
syndicate build
syndicate deploy --deploy_name sqs-lambda-dev
```

### 8. Verification Steps

#### 8.1. AWS CLI Verification

Check if resources are created:

```bash
# Check Lambda function
aws lambda get-function --function-name cmtr-ze58tzcf-sqs_handler-k3vb --region eu-west-1

# Check Lambda alias
aws lambda get-alias --function-name cmtr-ze58tzcf-sqs_handler-k3vb --name learn --region eu-west-1

# Check SQS queue
aws sqs get-queue-url --queue-name cmtr-ze58tzcf-async_queue-k3vb --region eu-west-1

# Check queue attributes
aws sqs get-queue-attributes --queue-url $(aws sqs get-queue-url --queue-name cmtr-ze58tzcf-async_queue-k3vb --region eu-west-1 --query 'QueueUrl' --output text) --attribute-names All --region eu-west-1

# Check event source mapping
aws lambda list-event-source-mappings --function-name cmtr-ze58tzcf-sqs_handler-k3vb:learn --region eu-west-1

# Check IAM role
aws iam get-role --role-name cmtr-ze58tzcf-sqs_handler_execution_role-k3vb --region eu-west-1
```

#### 8.2. Test the Integration

Send a test message to SQS queue:

```bash
# Get queue URL
QUEUE_URL=$(aws sqs get-queue-url --queue-name cmtr-ze58tzcf-async_queue-k3vb --region eu-west-1 --query 'QueueUrl' --output text)

# Send test message
aws sqs send-message --queue-url $QUEUE_URL --message-body '{"test": "Hello from SQS!", "timestamp": "2024-01-01T12:00:00Z"}' --region eu-west-1

# Send another test message
aws sqs send-message --queue-url $QUEUE_URL --message-body 'Plain text message for testing' --region eu-west-1
```

#### 8.3. Check CloudWatch Logs

```bash
# List log groups
aws logs describe-log-groups --log-group-name-prefix "/aws/lambda/cmtr-ze58tzcf-sqs_handler-k3vb" --region eu-west-1

# Get recent log events
LOG_GROUP="/aws/lambda/cmtr-ze58tzcf-sqs_handler-k3vb"
aws logs describe-log-streams --log-group-name $LOG_GROUP --order-by LastEventTime --descending --region eu-west-1

# Get latest log stream
LATEST_STREAM=$(aws logs describe-log-streams --log-group-name $LOG_GROUP --order-by LastEventTime --descending --max-items 1 --query 'logStreams[0].logStreamName' --output text --region eu-west-1)

# Get log events
aws logs get-log-events --log-group-name $LOG_GROUP --log-stream-name $LATEST_STREAM --region eu-west-1
```

#### 8.4. AWS Console Verification

1. **Lambda Function:**
   - Navigate to AWS Lambda Console
   - Find function: `cmtr-ze58tzcf-sqs_handler-k3vb`
   - Check Aliases tab for `learn` alias
   - Verify event source mapping to SQS queue

2. **SQS Queue:**
   - Navigate to AWS SQS Console
   - Find queue: `cmtr-ze58tzcf-async_queue-k3vb`
   - Check queue properties and permissions

3. **CloudWatch Logs:**
   - Navigate to CloudWatch Logs Console
   - Check log group: `/aws/lambda/cmtr-ze58tzcf-sqs_handler-k3vb`
   - Verify message processing logs

#### 8.5. Cleanup

```bash
# Clean up resources
syndicate clean --deploy_name sqs-lambda-dev
```

### 9. Complete Project Structure

```bash
sqs-lambda/
├── .syndicate-config-dev/
│   ├── syndicate.yml
│   └── syndicate_aliases.yml
├── deployment_resources.json
├── src/
│   └── sqs_handler.py
└── README.md
```

### 10. Troubleshooting

Common issues and solutions:

1. **Permission Denied:** Ensure IAM role has correct SQS permissions
2. **Lambda Not Triggered:** Check event source mapping configuration
3. **Logs Not Appearing:** Verify CloudWatch Logs permissions in IAM role
4. **Queue Not Found:** Check resource naming with prefix/suffix

This completes the AWS SQS and Lambda integration using aws-syndicate framework.

## Results

The solution Successfully tested the AWS SQS and Lambda integration with aws-syndicate!

1. ✅ Set up the SQS queue (`async_queue`) and Lambda function (`sqs_handler`)
2. ✅ Configure the proper IAM policies and event source mappings
3. ✅ Deploy using aws-syndicate with the correct naming conventions
4. ✅ Test the integration and verify the logs in CloudWatch

The solution demonstrates a solid understanding of:

- AWS Syndicate framework usage
- SQS-Lambda integration patterns
- Proper resource naming with prefixes/suffixes
- Lambda aliases and versioning
- CloudWatch logging for monitoring
