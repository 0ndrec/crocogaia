import requests


def send_requests(textload: str, headers: dict, message: dict, endpoint: str, timeout: int) -> dict:

    if not endpoint.startswith("http") or not endpoint.startswith("https"):
        endpoint = "http://" + endpoint
    
    message["messages"][1]["content"] = textload
    print("Message: ", textload)

    response = requests.post(endpoint, json=message, headers=headers, timeout=timeout)

    if response.status_code == 404:
        print(f"Endpoint {endpoint} not found.")
        return None
    elif response.status_code == 504:
        print(f"Endpoint {endpoint} timed out.")
        return None
    return response.json()
