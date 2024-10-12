import requests
import time

def read_init_data(file_path):
    """Reads multiple init-data entries from the specified file."""
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines() if line.strip()]

def get_task(init_data):
    """Fetch tasks from the API."""
    url = "https://nordgatetest-gfe0dubkf7cgc7f4.westeurope-01.azurewebsites.net/api/v1/tasks"

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        "Origin": "https://nord-gate-web-app.vercel.app",
        "Referer": "https://nord-gate-web-app.vercel.app/",
        "x-telegram-init-data": init_data,
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0',
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch tasks. Status code: {response.status_code}")
        return None

def start_task(init_data, task_id):
    """Start a task."""
    url = f"https://nordgatetest-gfe0dubkf7cgc7f4.westeurope-01.azurewebsites.net/api/v1/tasks/start/{task_id}"

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        "Origin": "https://nord-gate-web-app.vercel.app",
        "Referer": "https://nord-gate-web-app.vercel.app/",
        "x-telegram-init-data": init_data,
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0',
    }

    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to start task. Status code: {response.status_code}")
        return None

def check_task_completion(init_data, task_id):
    """Check if the task is marked as completed before claiming the reward."""
    url = f"https://nordgatetest-gfe0dubkf7cgc7f4.westeurope-01.azurewebsites.net/api/v1/tasks/{task_id}"

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        "Origin": "https://nord-gate-web-app.vercel.app",
        "Referer": "https://nord-gate-web-app.vercel.app/",
        "x-telegram-init-data": init_data,
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0',
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        task_data = response.json()
        task_status = task_data.get('data', {}).get('status')
        return task_status == "completed"  # Make sure task is marked as completed
    else:
        print(f"Failed to check task completion status. Status code: {response.status_code}")
        return False

def claim_reward(init_data, task_id):
    """Claim reward for a task."""
    url = f"https://nordgatetest-gfe0dubkf7cgc7f4.westeurope-01.azurewebsites.net/api/v1/tasks/claim/{task_id}"

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        "Origin": "https://nord-gate-web-app.vercel.app",
        "Referer": "https://nord-gate-web-app.vercel.app/",
        "x-telegram-init-data": init_data,
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0',
    }

    response = requests.post(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to claim reward. Status code: {response.status_code}")
        print("Response content:", response.text)  # Debugging info
        return None

# Full execution block
if __name__ == "__main__":
    # Read all init_data entries from query.txt
    init_data_list = read_init_data("query.txt")
    
    for init_data in init_data_list:
        print(f"Processing query: {init_data}")

        # Fetch tasks
        task_response = get_task(init_data)
        if task_response:
            print("Tasks fetched successfully")
            tasks = task_response.get('data', {}).get('nordom', [])
            
            if tasks:
                for task in tasks:
                    print(f"Processing task: {task.get('name')}")
                    task_id = task.get('id')
                    
                    # Start the task
                    start_response = start_task(init_data, task_id)
                    if start_response:
                        print(f"Successfully started task: {task.get('name')}")

                        # Add a delay before checking task completion status
                        time.sleep(10)  # Wait 10 seconds or more if needed for task processing

                        # Check if the task is completed
                        is_completed = check_task_completion(init_data, task_id)
                        if is_completed:
                            print(f"Task {task.get('name')} completed, claiming reward...")

                            # Claim the reward
                            claim_response = claim_reward(init_data, task_id)
                            if claim_response:
                                print(f"Successfully claimed reward for task: {task.get('name')}")
                            else:
                                print(f"Failed to claim reward for task: {task.get('name')}")
                        else:
                            print(f"Task {task.get('name')} not completed, cannot claim reward.")
                    else:
                        print(f"Failed to start task: {task.get('name')}")
            else:
                print("No tasks available.")
        else:
            print("Failed to fetch tasks.")
