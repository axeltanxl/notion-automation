import requests
import json
import os
from dotenv import load_dotenv
from datetime import date

# For JSON compatibility
null = None
false = False

# Load the .env file
load_dotenv()

# TODO: Make sure that you have a NOTION_SECRET environment variable set
NOTION_TOKEN = os.getenv('NOTION_SECRET', '')


def create_page(parent_id: str):
    # Gets quote of the day
    qotd = get_qotd()

    if qotd is None:
        print('Could not get quote of the day')
        return

    # Gets today's date
    today = date.today()
    today = today.strftime("%d/%m/%Y")

    payload = {
        'parent': {'page_id': parent_id},
        'icon': {
            'type': 'emoji',
            'emoji': '🚀'
        },
        'cover': {
            'type': 'external',
            'external': {
                    'url': 'https://unsplash.it/1920/1080?random'
            },
        },
        'properties': {
            'title': {
                'title': [
                    {
                        'text': {'content': 'Day Plan for '+today+''}
                    },
                ]
            },
        },
        'children': [
            {
                'object': 'block',
                'type': 'quote',
                'quote': {
                    'text': [{
                        'type': 'text',
                        'text': {
                            'content': "Quote of the day: \""+qotd[0]["q"]+"\"",
                        }
                    }]
                }
            },
            {
                "object": "block",
                "id": "e5ddbd2a-93cd-4162-85d9-a0de4eece691",
                "created_time": "2021-10-27T06:37:00.000Z",
                "last_edited_time": "2021-10-27T06:39:00.000Z",
                "has_children": false,
                "archived": false,
                "type": "heading_2",
                "heading_2": {
                    "text": [
                        {
                            "type": "text",
                            "text": {
                                "content": "Events",
                                "link": null
                            },
                            "annotations": {
                                "bold": false,
                                "italic": false,
                                "strikethrough": false,
                                "underline": false,
                                "code": false,
                                "color": "default"
                            },
                            "plain_text": "Events",
                            "href": null
                        }
                    ]
                }
            },
            {
                "object": "block",
                "id": "387f898a-b42e-4e76-a13e-830a344a05dd",
                "created_time": "2021-10-27T06:37:00.000Z",
                "last_edited_time": "2021-10-27T06:39:00.000Z",
                "has_children": false,
                "archived": false,
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "text": []
                }
            },
            {
                "object": "block",
                "id": "2d66cd5b-c453-411d-a964-0fa861140945",
                "created_time": "2021-10-27T06:39:00.000Z",
                "last_edited_time": "2021-10-27T06:39:00.000Z",
                "has_children": false,
                "archived": false,
                "type": "divider",
                "divider": {}
            },
            {
                "object": "block",
                "id": "852343f9-3f4e-4c9d-ae3c-8f4b542e2a0f",
                "created_time": "2021-10-27T06:37:00.000Z",
                "last_edited_time": "2021-10-27T06:37:00.000Z",
                "has_children": false,
                "archived": false,
                "type": "heading_2",
                "heading_2": {
                    "text": [
                        {
                            "type": "text",
                            "text": {
                                "content": "Daily Tasks",
                                "link": null
                            },
                            "annotations": {
                                "bold": false,
                                "italic": false,
                                "strikethrough": false,
                                "underline": false,
                                "code": false,
                                "color": "default"
                            },
                            "plain_text": "Daily Tasks",
                            "href": null
                        }
                    ]
                }
            },
            {
                "object": "block",
                "id": "452cbd05-23b1-4162-9494-ce78bfd24a57",
                "created_time": "2021-10-27T06:37:00.000Z",
                "last_edited_time": "2021-10-27T06:37:00.000Z",
                "has_children": false,
                "archived": false,
                "type": "to_do",
                "to_do": {
                    "text": [],
                    "checked": false
                }
            },
            {
                "object": "block",
                "id": "418a5cc5-8e32-4638-a4a2-ed8632fcb8a9",
                "created_time": "2021-10-27T06:37:00.000Z",
                "last_edited_time": "2021-10-27T06:37:00.000Z",
                "has_children": false,
                "archived": false,
                "type": "divider",
                "divider": {}
            },
            {
                "object": "block",
                "id": "931e4673-2358-4166-9386-1ed5e79f7e3a",
                "created_time": "2021-10-27T06:43:00.000Z",
                "last_edited_time": "2021-10-27T06:43:00.000Z",
                "has_children": false,
                "archived": false,
                "type": "heading_2",
                "heading_2": {
                    "text": [
                        {
                            "type": "text",
                            "text": {
                                "content": "Habit Tracker",
                                "link": null
                            },
                            "annotations": {
                                "bold": false,
                                "italic": false,
                                "strikethrough": false,
                                "underline": false,
                                "code": false,
                                "color": "default"
                            },
                            "plain_text": "Habit Tracker",
                            "href": null
                        }
                    ]
                }
            },
            {
                "object": "block",
                "id": "8bdec83a-ff52-4bcf-afd0-846bc42cb3db",
                "created_time": "2021-10-27T06:43:00.000Z",
                "last_edited_time": "2021-10-27T06:43:00.000Z",
                "has_children": false,
                "archived": false,
                "type": "to_do",
                "to_do": {
                    "text": [
                        {
                            "type": "text",
                            "text": {
                                "content": "Work out",
                                "link": null
                            },
                            "annotations": {
                                "bold": false,
                                "italic": false,
                                "strikethrough": false,
                                "underline": false,
                                "code": false,
                                "color": "default"
                            },
                            "plain_text": "Work out",
                            "href": null
                        }
                    ],
                    "checked": false
                }
            },
            {
                "object": "block",
                "id": "aea94681-1706-4247-bc5d-b9422ff19d72",
                "created_time": "2021-10-27T06:43:00.000Z",
                "last_edited_time": "2021-10-27T06:44:00.000Z",
                "has_children": false,
                "archived": false,
                "type": "to_do",
                "to_do": {
                    "text": [
                        {
                            "type": "text",
                            "text": {
                                "content": "Meditate",
                                "link": null
                            },
                            "annotations": {
                                "bold": false,
                                "italic": false,
                                "strikethrough": false,
                                "underline": false,
                                "code": false,
                                "color": "default"
                            },
                            "plain_text": "Meditate",
                            "href": null
                        }
                    ],
                    "checked": false
                }
            },
            {
                "object": "block",
                "id": "3fa86df1-26a9-4e4d-9baf-8f025b54ac4c",
                "created_time": "2021-10-27T06:45:00.000Z",
                "last_edited_time": "2021-10-27T06:46:00.000Z",
                "has_children": false,
                "archived": false,
                "type": "to_do",
                "to_do": {
                    "text": [
                        {
                            "type": "text",
                            "text": {
                                "content": "Read",
                                "link": null
                            },
                            "annotations": {
                                "bold": false,
                                "italic": false,
                                "strikethrough": false,
                                "underline": false,
                                "code": false,
                                "color": "default"
                            },
                            "plain_text": "Read",
                            "href": null
                        }
                    ],
                    "checked": false
                }
            },
            {
                "object": "block",
                "id": "3a58af86-fa92-4d90-b3fc-13b8d37455a3",
                "created_time": "2021-10-27T06:44:00.000Z",
                "last_edited_time": "2021-10-27T06:45:00.000Z",
                "has_children": false,
                "archived": false,
                "type": "to_do",
                "to_do": {
                    "text": [
                        {
                            "type": "text",
                            "text": {
                                "content": "Sleep by 11pm",
                                "link": null
                            },
                            "annotations": {
                                "bold": false,
                                "italic": false,
                                "strikethrough": false,
                                "underline": false,
                                "code": false,
                                "color": "default"
                            },
                            "plain_text": "Sleep by 11pm",
                            "href": null
                        }
                    ],
                    "checked": false
                }
            },
            {
                "object": "block",
                "id": "d3052fff-37a4-46ad-aa7c-36b9199c7559",
                "created_time": "2021-10-27T06:43:00.000Z",
                "last_edited_time": "2021-10-27T06:43:00.000Z",
                "has_children": false,
                "archived": false,
                "type": "divider",
                "divider": {}
            },
            {
                "object": "block",
                "id": "767819d7-c71f-4c04-b562-1495fc8edde1",
                "created_time": "2021-10-27T06:37:00.000Z",
                "last_edited_time": "2021-10-27T06:43:00.000Z",
                "has_children": false,
                "archived": false,
                "type": "heading_2",
                "heading_2": {
                    "text": [
                        {
                            "type": "text",
                            "text": {
                                "content": "Notes",
                                "link": null
                            },
                            "annotations": {
                                "bold": false,
                                "italic": false,
                                "strikethrough": false,
                                "underline": false,
                                "code": false,
                                "color": "default"
                            },
                            "plain_text": "Notes",
                            "href": null
                        }
                    ]
                }
            },
            {
                "object": "block",
                "id": "54c007ce-c789-4688-89c3-77b52543e4f9",
                "created_time": "2021-10-27T06:37:00.000Z",
                "last_edited_time": "2021-10-27T06:39:00.000Z",
                "has_children": false,
                "archived": false,
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "text": []
                }
            },
            {
                "object": "block",
                "id": "e01a6e6a-5856-4170-bec0-6cd1d3f68fa9",
                "created_time": "2021-10-27T06:37:00.000Z",
                "last_edited_time": "2021-10-27T06:37:00.000Z",
                "has_children": false,
                "archived": false,
                "type": "paragraph",
                "paragraph": {
                    "text": []
                }
            }
        ]
    }

    # API request to create page
    response = requests.post('https://api.notion.com/v1/pages/', json=payload, headers={
        'Authorization': 'Bearer '+NOTION_TOKEN, 'Notion-Version': '2021-08-16'})

   # If the request was not successful, we print the error and return
    if not response.ok:
        print('Error:', response.status_code)
        print('Error:', response.content)
        return

    # Parse response as JSON and return
    data = response.json()
    return data


def get_qotd():
    # Get the quote of the day
    r = requests.get('https://zenquotes.io/api/today')
    # Request failed, don't try to parse and just return None
    if not r.ok:
        return None

    # Parse JSON
    json_data = r.json()

    # Uncomment the following line to see the complete response
    # print(json.dumps(json_data, indent=4))
    return json_data


if __name__ == "__main__":

    # Use list_pages.py to get the page ID. It should be 36 characters long separated by 4 hyphens. This is the page the day plans will be created in
    page_parent_id = 'TODO'

    # Create a normal page

    page_data = create_page(page_parent_id)
    if page_data is not None:
        # print(json.dumps(data, indent=4))
        print('New page available here: {}'.format(page_data['url']))