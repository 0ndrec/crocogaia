import os
from utils.config import load_config, save_config, update_config, load_json
from utils.requester import send_requests
from utils.maker import make_sentence
from time import sleep

def analyze_config():
    config_file = "config.yaml"

    # Check if config exists, otherwise prompt user to create one
    if not os.path.exists(config_file):
        print("Configuration file not found. Creating a new one.")
        config = update_config()
        save_config(config_file, config)
    else:
        config = load_config(config_file)
        print("Configuration file found.")
        print('\n')
        for key, value in config.items():
            print(f"{key}: {value}")
        print('\n')

    # Load configuration
    try:
        num_requests = config.get("num_requests")
        request_interval = config.get("request_interval")
        sentence_length = config.get("sentence_length")
        endpoints = config.get("endpoints")
    except Exception as e:
        print(f"Error loading configuration: {e}")

    return num_requests, request_interval, sentence_length, endpoints

if __name__ == "__main__":
    # Unpack configuration
    num_requests, request_interval, sentence_length, endpoints = analyze_config()

    # Load headers and message
    try:
        headers = load_json("data/headers.json")
        message = load_json("data/message.json")
    except Exception as e:
        print(f"Error loading headers and message: {e}")


    while True:
        textload = make_sentence(sentence_length)

        for endpoint in endpoints:
            print("Sending request to: ", endpoint)
            resp = send_requests(textload, headers, message, endpoint, timeout= 500)

            if resp:
                print("Response content: ", resp["choices"][0]["message"]["content"])
                print("Response model: ", resp["model"])
                print("Response ID: ", resp["id"])
            else:
                pass

            print("\n")

        print("Sleeping for", request_interval, "seconds...")
        sleep(request_interval)