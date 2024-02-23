import argparse
import requests
from dotenv import load_dotenv
import os

from pathlib import Path as p

# Load environment variables from a .env file
load_dotenv()

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Send a Markdown file as a string in a POST request to an API.")
parser.add_argument("file", help="Path to the Markdown file to be sent")
parser.add_argument("-d", action="store_true", help="Send to Dev")
parser.add_argument("-p", action="store_true", help="Send to Prod")
args = parser.parse_args()

# Read the content of the Markdown file
try:
    file = p(args.file)
    with open(p, 'r') as file:
        markdown_content = file.read()

    # Replace new line characters with \n
    markdown_content = markdown_content.replace("\n", "\\n")

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
    # Define the API URL
    # Change this to your actual API URL

    # Set up the headers including the API-Key
    headers = {
        "Content-Type": "application/json",
        "API-Key": f"{api_key}"
    }

    # Prepare the data payload
    data = {"markdown": markdown_content}
    print(data)

    '''
    # Send the POST request
    response = requests.post(api_url, json=data, headers=headers)

    # Check the response
    if response.status_code == 200:
        print("Markdown content successfully sent to the API.")
    else:
        print(f"Failed to send Markdown content. Status code: {response.status_code}, Message: {response.text}")
    '''

except FileNotFoundError:
    print("The specified file does not exist.")
except Exception as e:
    print(f"An error occurred: {e}")