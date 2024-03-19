import os
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)  # Set the desired logging level

def send_files_to_server(source_dir, server_url):
    files_to_send = []

    # Iterate over all files in the source directory
    for file_name in os.listdir(source_dir):
        file_path = os.path.join(source_dir, file_name)
        if os.path.isfile(file_path):
            # Open the file in binary mode and add it to the list
            with open(file_path, 'rb') as file:
                files_to_send.append(('files', (file_name, file)))

    # Send a POST request with multipart/form-data containing the files list
    response = requests.post(server_url, files=files_to_send)

    # Check the response status code
    if response.status_code == 200:
        logging.info("Files were sent successfully.")
    else:
        logging.error(f"Failed to send files. Status code: {response.status_code}")
    return response

if __name__ == "__main__":
    source_dir = '/home/yael-vm2/task_azure_output'
    server_url = 'http://172.212.97.195/upload/'
    send_files_to_server(source_dir, server_url)
