import requests
import time
from datetime import datetime, timedelta

def get_instance_termination_time():
    response = requests.get('http://169.254.169.254/latest/meta-data/spot/instance-action')
    if response.status_code == 404:
        return None
    return datetime.strptime(response.json()['time'], '%Y-%m-%dT%H:%M:%SZ')

def main(execute_secs_before_termination=30):
    # Continue polling until termination notice is found
    while True:
        termination_time = get_instance_termination_time()
        if termination_time is not None:
            break
        time.sleep(2)

    current_time = datetime.utcnow()
    time_to_termination = (termination_time - current_time).total_seconds()

    print(f"Current time is: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Spot Instance termination time is: {termination_time.strftime('%Y-%m-%d %H:%M:%S')}")

    # Execute commands some time before actual termination
    if time_to_termination >= execute_secs_before_termination:
        wait_time = time_to_termination - execute_secs_before_termination
        print(f"Waiting {int(wait_time)} seconds before executing termination commands")
        time.sleep(wait_time)

    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Wait script finished.")

if __name__ == "__main__":
    import sys
    execute_secs_before_termination = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    main(execute_secs_before_termination)
