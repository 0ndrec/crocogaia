# Chek if file config.yaml exists
import os
import yaml
import logging

logger = logging.getLogger(__name__)


def load_config(path='config.yaml'):
    try:
        with open(path, 'r') as config_file:
            config = yaml.safe_load(config_file)
    except Exception as e:
        logger.error(e)
    return config

def save_changes(config, path='config.yaml'):
    try:
        with open(path, 'w') as config_file:
            yaml.dump(config, config_file)
    except Exception as e:
        logger.error(e)

def check_values(config):
    if len(config.get('EVM_ADDRESS')) != 42 or config.get('EVM_ADDRESS') is None:
        evm_address = input('Please enter your address: ')
        if evm_address.startswith('0x') and len(evm_address) == 42:
            config['EVM_ADDRESS'] = evm_address
            save_changes(config)
        else:
            logger.error('Invalid EVM address')
            exit() 
    else:
        logger.info("Setted EVM address: {}".format(config.get('EVM_ADDRESS')))

    if config.get('MIN_REQ_FREQUENCY') is None or config.get('MIN_REQ_FREQUENCY') == 0:
        val = input('Please enter your minimum request frequency per hour: ')
        config['MIN_REQ_FREQUENCY'] = int(val)
        save_changes(config)
    else:
        logger.info("Setted minimum request frequency per hour: {}".format(config.get('MIN_REQ_FREQUENCY')))


    if config.get('MIN_SENTENCE_LEN') is None or config.get('MIN_SENTENCE_LEN') == 0:
        val_len = input('Please enter your minimum sentence length: ')
        config['MIN_SENTENCE_LEN'] = int(val_len)
        save_changes(config)
    else:
        logger.info("Setted minimum sentence length: {}".format(config.get('MIN_SENTENCE_LEN')))


    if config.get('MAX_SENTENCE_LEN') is None or config.get('MAX_SENTENCE_LEN') == 0:
        val_len = input('Please enter your maximum sentence length: ')
        config['MAX_SENTENCE_LEN'] = int(val_len)
        save_changes(config)
    else:
        logger.info("Setted maximum sentence length: {}".format(config.get('MAX_SENTENCE_LEN')))


    return config
