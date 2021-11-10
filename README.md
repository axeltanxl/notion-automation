# Notion Automation
Scripts to automate Notion and improve productivity

## 1. Day Plan
### What it does
Creates a new 'Day Plan' in a specified Notion page everyday.
![Day Plan format](/images/day-plan.png)
### Features
1. New background image everyday (using Unsplash API)
2. New Quote of the Day everyday (using ZenQuotes API)
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
- In progress
