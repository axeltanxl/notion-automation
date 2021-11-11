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
##### Create Lambda function
1. In progress
