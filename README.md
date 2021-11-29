# Notion Automation
Scripts to automate Notion and improve productivity

## 1. Day Plan
### What it does
Creates a new 'Day Plan' in a specified Notion page everyday.
![Day Plan format](/images/day-plan.png)
### Features
1. New background image everyday (using Unsplash API)
2. New Quote of the Day everyday (using ZenQuotes API)
3. Deployment to AWS
### How to use it
#### Notion set-up
1. Create a [Notion integration](https://www.notion.so/my-integrations)
2. Copy the unique 'Internal Integration Token' for your integration
3. Share the required page with the integration
    - On the top right corner of the page:
        - "Share" -> "Invite" -> Your integration
#### Code set-up
1. Create a new `.env` file with the same contents as the `.env.example` file
2. Replace `your_secret_here` with the Iternal Integration Token you have copied
3. Run `list_pages.py` to get the page ID for the required page
    - It should be a string of 36 random letters and numbers, separated by 4 hyphens
4. Replace the `page_parent_id` variable in `create_page.py` with the page ID for your page
    - Scroll down to the bottom of `create_page.py`
    - Replace `TODO` with your page ID
#### Deployment
The script will be deployed onto an AWS EC2 instance, which will be started and stopped automatically by a Lambda function. The EC2 instance will be started and stopped at a specific time configured in Amazon EventBridge Events, which will then trigger the Lambda function. Once the EC2 instance has started, it will run the script as a cron job and get terminated a few minutes later, once the cron job has been completed.
##### Create an EC2 instance
1. In the AWS management console, go to the EC2 service -> "Launch instances"
    - Select and configure the type of AMI, instance type, instance details (subnet, AZ), storage and tags. Just use the free-tier eligible defaults.
    - For the security group, make sure SSH is allowed from anywhere (source: 0.0.0.0/0). The protocol and port should be “TCP” and “22” respectively. Once done, select “Review and Launch” and then “Launch”.
        - Create a key pair if you don't have one

##### Create an IAM policy and role to allow Lambda to start & stop EC2 instances
1. Go to IAM -> Policies -> Create Policy
2. Click on "JSON" to us ethe JSON editor to create the policy
3. Copy and paste the following code into the editor:
```
{
    "Version": "2012-10-17",
    "Statement": [
    {
        "Effect": "Allow",
        "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
        ],
        "Resource": "arn:aws:logs:*:*:*"
    },
    {
        "Effect": "Allow",
        "Action": [
        "ec2:Start*",
        "ec2:Stop*"
        ],
        "Resource": "*"
    }
    ]
}
```
4. Create the policy
5. In IAM, go to Roles -> Create role
6. Choose "AWS service" as the trusted identity and "Lambda" as the use case
7. Next, attach the policy you just created to the role
8. Click on "Next" to complete the process.

##### Create Lambda functions to stop and start EC2 instances
1. Go to the Lambda service in AWS console
2. Click on "Create function"
    - Choose the option to "Author from scratch"
    - Give your function a name (I suggest "StopEC2Instance" for easy identification later)
    - Under "Runtime", choose Python 3.9
    - Click on the "Change default execution role" under "Permissions", and choose "Use an existing role"
    - Select the name of the IAM role you just created
    - Leave the rest of the options as default, and click on "Create function"
3. Go to the page that shows all your Lambda functions and select the function you just created
4. Click on the "Code" tab to edit the Lambda function
5. Copy and paste the following code into the code editor:
```
# This code is used to stop your EC2 instance
# Replace your_region and instance_id with your EC2 instance region and EC2 instance ID respectively
import boto3
region = 'your_region'
instances = ['instance_id']
ec2 = boto3.client('ec2', region_name=region)

def lambda_handler(event, context):
    ec2.stop_instances(InstanceIds=instances)
    print('stopped your instances: ' + str(instances))
```
6. Click on "Deploy"
7. Next, click on the "Configuration" tab -> "General settings" -> "Edit" and set the timeout to 10 seconds
8. Repeat steps 1 to 7 to create another Lambda function that starts the EC2 instance

##### Create Amazon EventBridge Rules to trigger Lambda functions on a schedule
In progress
