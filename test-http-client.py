import unittest
from unittest.mock import patch, Mock
from http_client import send_files_to_server

class TestSendFilesToServer(unittest.TestCase):
    global source_dir
    source_dir='./task_azure_output'
    global server_url
    server_url = 'http://172.212.97.195/upload/'

    @patch('http_client.requests.post')
    def test_send_files_to_server_success(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        with self.assertLogs() as log:
            response = send_files_to_server(source_dir, server_url)
            self.assertEqual(response.status_code, 200)
        
        # Check that the log message was generated
        self.assertIn("Files were sent successfully.", log.output[0])

    @patch('http_client.requests.post')
    def test_send_files_to_server_failure(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_post.return_value = mock_response

        source_dir = "empty"
        with self.assertLogs() as log:
            response = send_files_to_server(source_dir, server_url)
            self.assertEqual(response.status_code, 500)
        
        # Check that the log message was generated
        self.assertIn(f"Failed to send files. Status code: {response.status_code}", log.output[0])

if __name__ == '__main__':
    unittest.main()
