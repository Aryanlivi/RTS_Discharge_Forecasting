import logging
import socketio
import os
from dotenv import load_dotenv

import sys
# Add the parent directory of src to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ForecastManager import ForecastManager
class SocketClient:
    def __init__(self):
        # Load environment variables
        load_dotenv()

        # Get environment variables
        self.BASE_URL = os.getenv('socketBaseURL')
        self.SOCKET_NAMESPACE = os.getenv('SOCKET_NAMESPACE')

        if not self.BASE_URL or not self.SOCKET_NAMESPACE:
            print("Error: Missing required environment variables")
            sys.exit(1)

        # Set up logging configuration
        logging.basicConfig(
            filename='Socket/logs/socket_client.log', 
            level=logging.DEBUG,  
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

        self.socket_gss = socketio.Client()

        # Register events
        self.socket_gss.on('connect', self.connect)
        self.socket_gss.on('connect_error', self.connect_error)
        self.socket_gss.on(self.SOCKET_NAMESPACE, self.handle_namespace_event)
        self.socket_gss.on('disconnect', self.disconnect)

    def connect(self):
        logging.info('Socket connected')
        print("Socket Connected.")
        self.socket_gss.emit('client_request', self.SOCKET_NAMESPACE)

    def connect_error(self, error):
        logging.error(f'Connection error: {error}')

    def handle_namespace_event(self, data):
        logging.info(f"Received data from namespace")
        # Run the forecast computation and posting
        forecast_manager=ForecastManager(data)
        forecast_manager.post()

    def disconnect(self):
        logging.info('Socket disconnected')

    def init_socket_connection(self):
        try:
            self.socket_gss.connect(self.BASE_URL)
            logging.info(f'Connected to {self.BASE_URL}')
        except Exception as e:
            logging.error(f'Error connecting to {self.BASE_URL}: {e}')
            sys.exit(1)  # Exit if connection fails

    def run(self):
        self.init_socket_connection()
        try:
            self.socket_gss.wait()
        except KeyboardInterrupt:
            logging.info('Socket client terminated by user')
            self.socket_gss.disconnect()

# Run the client
if __name__ == "__main__":
    client = SocketClient()
    client.run()
