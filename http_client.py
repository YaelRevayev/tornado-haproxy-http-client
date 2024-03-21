#!/usr/bin/env python
import os
import requests
import logging
from datetime import datetime


log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)


def create_error_logger():
    error_logger = logging.getLogger("error_logger")
    error_logger.setLevel(logging.ERROR)
    error_handler = logging.FileHandler(os.path.join(log_dir, "error_logs.txt"))
    error_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    error_handler.setFormatter(error_formatter)
    error_logger.addHandler(error_handler)
    return error_logger


def create_info_logger():
    info_logger = logging.getLogger("info_logger")
    info_logger.setLevel(logging.INFO)
    info_handler = logging.FileHandler(
        os.path.join(log_dir, f"client_logs_{datetime.now().strftime('%Y-%m-%d')}.txt")
    )
    info_formatter = logging.Formatter(
        "%(asctime)s - %(filename)s - %(levelname)s - %(message)s"
    )
    info_handler.setFormatter(info_formatter)
    info_logger.addHandler(info_handler)
    return info_logger


def send_files_to_server(source_dir, server_url, info_logger, error_logger):
    files_to_send = []

    for file_name in os.listdir(source_dir):
        file_path = os.path.join(source_dir, file_name)
        if os.path.isfile(file_path):
            with open(file_path, "rb") as file:
                file_data = file.read()
                files_to_send.append(("files", (file_name, file_data)))
                info_logger.info(f"Processing file: {file_name}")

    response = requests.post(server_url, files=files_to_send)

    if response.status_code == 200:
        info_logger.info("Files were sent successfully.")
    else:
        error_logger.error(f"Failed to send files. Status code: {response.status_code}")
    return response


if __name__ == "__main__":
    source_dir = "task_azure_output"
    server_url = "http://172.212.97.195/upload/"
    send_files_to_server(
        source_dir, server_url, create_info_logger(), create_error_logger()
    )
