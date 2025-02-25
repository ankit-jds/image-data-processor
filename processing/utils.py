# utils.py or your desired file in your Django project

import requests
import json
from apscheduler.schedulers.background import BackgroundScheduler

def hit_api_endpoint():
    """
    Function to send a request to the own backend API endpoint.
    This function will be scheduled to run at intervals.
    """
    url = "http://127.0.0.1:8000/api/p/upload/"  # Replace with your API endpoint
    method = "POST"  # or GET, PUT, DELETE based on your requirement
    params = {"query": "test"}  # URL parameters if needed
    json_body = {"key": "value"}  # Body in JSON format if needed
    headers = {'Content-Type': 'application/json'}

    try:
        if method.lower() == "post":
            response = requests.post(url, json=json_body, params=params, headers=headers)
        elif method.lower() == "get":
            response = requests.get(url, params=params, headers=headers)
        elif method.lower() == "put":
            response = requests.put(url, json=json_body, params=params, headers=headers)
        elif method.lower() == "delete":
            response = requests.delete(url, params=params, headers=headers)
        else:
            print(f"Unsupported HTTP method: {method}")
            return

        # Print the response status and message
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"Response Status: {response.status_code} - {response.reason}")
                print(f"Response Data: {json.dumps(data, indent=2)}")
            except json.JSONDecodeError:
                print(f"Response Status: {response.status_code} - {response.reason}")
                print("Response Content is not in JSON format.")
                print(f"Response: {response.text}")
        else:
            print(f"Error: {response.status_code} - {response.reason}")
            print(f"Message: {response.text}")

    except Exception as e:
        print(f"Error while sending request: {str(e)}")


def start_scheduler():
    """
    Function to start the APScheduler.
    This will run the task at defined intervals.
    """
    scheduler = BackgroundScheduler()

    # Schedule the job to run every 10 minutes (adjust the interval as needed)
    scheduler.add_job(hit_api_endpoint, "cron", hour=16, minute=4,second=30, max_instances=1)


    # Start the scheduler
    scheduler.start()

    print("Scheduler started, hitting the API every 10 minutes.")
