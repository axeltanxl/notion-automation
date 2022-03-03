# Notion Day Plan Automation
Automate the process of creating day plans in Notion everyday.

## Day Plan
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
2. Replace `your_secret_here` with the Internal Integration Token you have copied
3. Run `list_pages.py` to get the page ID for the required page
    - It should be a string of 36 random letters and numbers, separated by 4 hyphens
4. Replace the `page_parent_id` variable in `create_page.py` with the page ID for your page
    - Scroll down to the bottom of `create_page.py`
    - Replace `TODO` with your page ID
#### Deployment
The script will be deployed onto an AWS EC2 instance, which will be started and stopped automatically by a Lambda function. The EC2 instance will be started and stopped at a specific time configured in Amazon EventBridge Events, which will trigger the Lambda function. Once the EC2 instance has started, it will run the script as a cron job and terminate a few minutes later, once the cron job has been completed.
##### Create an EC2 instance
1. In the AWS management console, go to EC2 -> "Launch instances"
    - Select and configure the type of AMI, instance type, instance details (subnet, AZ), storage and tags. Just use the free-tier eligible defaults.
    - For the security group, make sure SSH is allowed from anywhere (source: 0.0.0.0/0). The protocol and port should be “TCP” and “22” respectively. Once done, select “Review and Launch” and then “Launch”.
        - Create a key pair if you don't have one

##### Create an IAM policy and role to allow Lambda to start & stop EC2 instances
1. Go to IAM -> Policies -> Create Policy
2. Click on "JSON" to use the JSON editor to create the policy
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
    - Choose the option "Author from scratch"
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
1. Go to the Amazon EventBridge service in AWS
2. Select "Create rule"
    - Name and description:
        - Give the rule a name (e.g: StopEC2Instance)
        - Give the rule a description (e.g: Stops EC2 instance at 7:00am everyday)
    - Define pattern:
        - Select "Schedule" -> "cron expression"
        - Key in the cron expression for the required time to stop the EC2 instance everyday
            - Format: time_in_minutes time_in_hours * * ? *
            - The time should be entered in 24-hour format
            - The default time zone is GMT+0. Convert the time in your local time zone to GMT+0 before entering the values in the cron expression.
            - E.g: 30 17 * * ? * (Event will be triggered at 5:30pm GMT+0 everyday)
    - Select event bus:
        - Choose "AWS default event bus"
    - Select targets:
        - Select "Lambda function" from the dropdown menu
        - Select the Lambda function you created to stop the EC2 instance
        - Leave the rest as default
    - Click "Create"
3. Repeat step 2 to create another rule to trigger the Lambda function to start the EC2 instance

##### Transfer files to EC2 instance and create cron job
1. Go to EC2 service in AWS console
2. If your EC2 instance is stopped, start it.
3. Following [this](https://axeltan.com/how-to-transfer-files-from-your-computer-to-an-ec2-instance) guide, transfer the `create_page.py` & `.env` files to the EC2 instance.
4. Change the timezone of the EC2 instance to your local timezone
    - Find your local timezone from all aviable timezones
        - Command: `timedatectl list-timezones`
        - To jump to the next page, click "SPACE". Once you have found your local timezone, copy the text and exit out of the screen by typing "q".
    - Change the timezone of the EC2 instance to your local timezone
        - Command: `sudo timedatectl <your_local_timezone>`
        - Replace your_local_timezone with the text you copied
5. Install the required Python3 modules
    - requests: `python3 -m pip install requests`
    - dotenv: `python3 -m pip install dotenv`
6. Create a cron job in the EC2 instance to run the Python script
    - Make sure the cron job runs in-between the time when your EC2 instance starts and ends
    - This is similar to the cron expression used to create the EventBridge Rules with minor differences:
        - Use your local timezone for the values in the expression instead of the converted time.
        - The cron expression used in EC2 instances does not have the year specified (last field in cron expression for EventBridge)
        - Cron expressions in EC2 do not use ?. Use * instead.
    - Full crontab expression to execute Python script: *cron_expression* python3 /home/ec2-user/create_page.py
    - E.g: 5 8 * * * python3 /home/ec2-user/create_page.py
7. And you are done! You have successfully automated the process of creating a Notion day plan.
