import requests
import logging
import json
import sched, time

from urllib3.util.retry import Retry
from datetime import date, timedelta, datetime

# General global variables
EXPLORER_API_URL = "explorer.nymtech.net/api/v1"
# Your node ID
MIXNODE_ID = 1
MIN_PERFORMANCE = 0.7
MEASURE_INTERVAL = 60

# Telegram bot variables
TELEGRAM_HTTP_API = ""
TELEGRAM_API_URL = f"api.telegram.org/bot{TELEGRAM_HTTP_API}"
TELEGRAM_CHAT_ID = ""

session = requests.Session()
logger = logging.getLogger()

def get_mixnodes_info():
    logger.info(f"Getting data from all mixnodes")

    resp = session.get(
        f"http://{EXPLORER_API_URL}/mix-nodes"
    )

    if resp.status_code != 200:
        raise Exception(
            f"Error while fetching data from nym explorer: {resp.content.decode()}"
        )

    return resp.json()

def get_mixnode_info(mixnode_index):
    logger.info(f"Getting data from mixnode {mixnode_index}")

    resp = session.get(
        f"https://{EXPLORER_API_URL}/mix-node/{mixnode_index}"
    )

    if resp.status_code != 200:
        raise Exception(
            f"Error while fetching data from nym explorer: {resp.content.decode()}"
        )

    return resp.json()

def is_node_down(task):
    logger.info("Checking Nym node status...")
    task.enter(MEASURE_INTERVAL, 1, is_node_down, (task,))
    node_performance = float(get_mixnode_info(MIXNODE_ID)["node_performance"]["most_recent"])
    if node_performance < MIN_PERFORMANCE:
        print(node_performance)
        logger.info("Sending alert to telegram")
        message = f"Your mixer node performance is low: {node_performance}"
        resp = session.get(
            f"https://{TELEGRAM_API_URL}/sendMessage?chat_id={TELEGRAM_CHAT_ID}&text={message}"
        )

        if resp.status_code != 200:
            raise Exception(
                f"Error while fetching data from nym explorer: {resp.content.decode()}"
            )

        return resp.json()

def start_monitoring():
    task = sched.scheduler(time.time, time.sleep)
    task.enter(MEASURE_INTERVAL, 1, is_node_down, (task,))
    task.run()

if __name__ == "__main__":
    # print(json.dumps(get_mixnode_info(MIXNODE_ID), indent=2))
    start_monitoring()
