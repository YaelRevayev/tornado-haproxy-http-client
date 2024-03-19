#!/usr/bin/env python
import os
import requests
import logging


logging.basicConfig(level=logging.INFO)

def send_files_to_server(source_dir, server_url):
    files_to_send = []

    for file_name in os.listdir(source_dir):
        file_path = os.path.join(source_dir, file_name)
        print(file_path)
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as file:
                file_data = file.read()
                files_to_send.append(('files', (file_name, file_data)))

    response = requests.post(server_url, files=files_to_send)

    if response.status_code == 200:
        logging.info("Files were sent successfully.")
    else:
        logging.error(f"Failed to send files. Status code: {response.status_code}")
    return response

if __name__ == "__main__":
    source_dir = 'task_azure_output'
    server_url = 'http://172.212.97.195/upload/'
    send_files_to_server(source_dir, server_url)
