import argparse
import requests
from dotenv import load_dotenv
import os
import frontmatter

from pathlib import Path as p


load_dotenv()

parser = argparse.ArgumentParser(description="Send a Markdown file as a string in a POST request to an API.")
parser.add_argument("file", help="Path to the Markdown file to be sent")
parser.add_argument("-d", action="store_true", help="Send to Dev")
parser.add_argument("-p", action="store_true", help="Send to Prod")
args = parser.parse_args()


try:
    newFile = p(args.file)
    with open(newFile, 'r') as file:
        post = frontmatter.load(file)

    markdown_content = post.content.replace("\n", "\\n")
   
    post = dict(post)


    # Retrieve the API-Key from environment variables
    api_key = os.getenv("API_Key")

    if not api_key:
        print("API-Key is not set in environment variables.")
        exit(1)


    if args.d:
        api_url = os.getenv("Dev_Endpoint")
        if not api_url:
            print("Dev_Endpoint is not set in environment variables.")
            exit(1)
    elif args.p:
        api_url = os.getenv("Prod_Endpoint")
        if not api_url:
            print("Dev_Endpoint is not set in environment variables.")
            exit(1)
    else:
        print("Please specify -d or -p")
        exit(1)


    headers = {
        "Content-Type": "application/json",
        "API-Key": f"{api_key}"
    }

    response = requests.get(api_url, headers=headers)

    json_response = dict(response.json())

    for item in json_response['data']:
        if item['slug'] == newFile.name.replace(".md", ""):
            api_url = api_url + "/" + item['slug']



 
    data = {
        "title":  post["title"],
        "markdown": markdown_content,
        "slug": newFile.name.replace(".md", ""),
        "description": post["description"]
        }
    
    response = requests.post(api_url, json=data, headers=headers)


    if response.status_code == 200:
        print("Markdown content successfully sent to the API.")
    else:
        print(f"Failed to send Markdown content. Status code: {response.status_code}, Message: {response.text}")

except FileNotFoundError:
    print("The specified file does not exist.")
except Exception as e:
    print(f"An error occurred: {e}")