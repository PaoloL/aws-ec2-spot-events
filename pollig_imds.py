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

def get_instance_metadata():
    """Retrieve instance metadata using the obtained IMDSv2 token."""
    token = get_token()
    metadata_url = "http://169.254.169.254/latest/meta-data/spot/instance-action"
    headers = {"X-aws-ec2-metadata-token": token}
    metadata_response = requests.get(metadata_url, headers=headers)
    return metadata_response

if __name__ == "__main__":
    while True:
        metadata_response = get_instance_metadata()
        if metadata_response.status_code == 200:
            termination_time = metadata_response.text
            print(f"Termination Time: {termination_time}")
            break
        else:
            print("Failed to retrieve termination time")
            time.sleep(5)