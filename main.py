import requests
import random
import logging
import time
from modules.configurator import load_config, check_values
from faker import Faker
from datetime import datetime



#----------------Logging----------------
logging.basicConfig(filename='chat_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')
#----------------Faker----------------
faker = Faker()
#----------------Headers----------------    
headers = {
    "accept": "application/json",
    "Content-Type": "application/json"
}






def send_message(node_url, message):
    try:
        response = requests.post(node_url, json=message, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logging.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {e}")

def extract_reply(response):
    if response and 'choices' in response:
        return response['choices'][0]['message']['content']
    return ""


if __name__ == "__main__":
    config = check_values(load_config())

    EVM_ADDRESS = config.get('EVM_ADDRESS')
    MIN_REQ_FREQENCY = config.get('MIN_REQ_FREQUENCY')
    MIN_SENTENCE_LEN = config.get('MIN_SENTENCE_LEN')
    MAX_SENTENCE_LEN = config.get('MAX_SENTENCE_LEN')
    node_url = EVM_ADDRESS + config.get('URL_API')

    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logging.info(f"{start_time} - Start")

    while True:

        random_question = faker.sentence(nb_words=random.randint(MIN_SENTENCE_LEN, MAX_SENTENCE_LEN))
        message = {
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": random_question}
            ]
        }

        question_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        response = send_message(node_url, message)
        reply = extract_reply(response)
        logging.info(f"{question_time} - {random_question} - {reply}")


        # Set the delay in seconds. value is req per hour
        delay = random.randint(MIN_REQ_FREQENCY, 3600)
        time.sleep(delay)

