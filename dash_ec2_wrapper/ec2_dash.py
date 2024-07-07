"""
ec2_dash.py
A custom Dash wrapper for automatic EC2 deployment, simplifying configuration
and deployment in an EC2 environment.

Environment Variables (in .env file):
    - PORT: The port to run the app on (default: 8050)
    - APPTYPE: Must be set to "dash" (other options [flask, streamlit] not supported)
    - APPNAME: The name of the app (default: "app")
author: @dariennouri
"""


import os
import logging
from typing import Optional
from dash import Dash as OriginalDash
from dotenv import load_dotenv

DEFAULT_PORT = 8050
DEFAULT_APP_NAME = 'app'

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DashConfig:
    def __init__(self, env_path: Optional[str] = None):
        load_dotenv(dotenv_path=env_path) if env_path else load_dotenv()
        self.port = int(os.getenv('PORT', DEFAULT_PORT))
        self.app_type = os.getenv('APPTYPE', 'dash')
        self.app_name = os.getenv('APPNAME', DEFAULT_APP_NAME)
        logger.info(f"Loaded configuration: PORT={self.port}, APPTYPE={self.app_type}, APPNAME={self.app_name}")

    def validate(self):
        if self.app_type != "dash":
            logger.error("APPTYPE must be set to 'dash' in the .env file")
            raise ValueError("APPTYPE must be set to 'dash' in the .env file")
        logger.info("Configuration validated successfully")

class Dash(OriginalDash):
    """
    A custom Dash wrapper for auto EC2 deployment.

    Note: Ensure the configured PORT is open in the EC2 security group.
    """

    def __init__(
        self,
        name: str,
        env_path: Optional[str] = None,
        url_base_pathname: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize the Dash instance.

        Args:
            name: The name of the Dash app.
            env_path: The path to the .env file.
            url_base_pathname: The base URL path for the Dash app.
            **kwargs: Additional keyword arguments for the original Dash class.
        """
        logger.info(f"Initializing Dash app: {name}")
        self.config = DashConfig(env_path)
        self.config.validate()

        if url_base_pathname is None:
            url_base_pathname = f'/{self.config.app_name}/'
        logger.info(f"Using URL base pathname: {url_base_pathname}")

        super().__init__(name, url_base_pathname=url_base_pathname, **kwargs)
        logger.info("Dash app initialized successfully")

    def run(self, debug: bool = False, **kwargs) -> None:
        host = kwargs.get('host', '0.0.0.0')
        port = kwargs.get('port', self.config.port)
        url = f"http://{host}:{port}{self.config.app_name}/"
        logger.info(f"Starting Dash app on {url}")
        print(f"Running app on {url}")
        try:
            super().run(debug=debug, host=host, port=port, **kwargs)
        except Exception as e:
            logger.error(f"Error running Dash app: {str(e)}")
            raise