import requests
import time

def get_token():
    """Retrieve the session token for IMDSv2."""
    url = "http://169.254.169.254/latest/api/token"
    headers = {"X-aws-ec2-metadata-token-ttl-seconds": "21600"}  # Token valid for 6 hours
    response = requests.put(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception("Failed to retrieve token from IMDSv2")

def get_instance_metadata(url):
    """Retrieve instance metadata using the obtained IMDSv2 token."""
    token = get_token()
    metadata_url = "http://169.254.169.254/latest/meta-data/"+url
    headers = {"X-aws-ec2-metadata-token": token}
    metadata_response = requests.get(metadata_url, headers=headers)
    return metadata_response

if __name__ == "__main__":
    while True:
        metadata_response = get_instance_metadata('events/recommendations/rebalance')
        if metadata_response.status_code == 200:
            signal_time = metadata_response.text
            print("Instance is at elevated risk of interruption")
            print(f"Signal Time: {signal_time}")
            break
        else:
            print("No signal detected, proceed")
            time.sleep(5)
    while True:   
        metadata_response = get_instance_metadata('spot/instance-action')
        if metadata_response.status_code == 200:
            termination_time = metadata_response.text
            print("Instance is marked to be stopped or terminated")
            print(f"Termination Time: {termination_time}")
            break
        else:
            print("No signal detected, proceed")
            time.sleep(5)