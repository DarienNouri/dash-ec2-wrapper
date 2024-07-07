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
import yaml

DEFAULT_APP_TYPE = 'dash'
DEFAULT_APP_NAME = 'app'
DEFAULT_PORT = 8050
DEFAULT_HOST = '0.0.0.0'

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DashConfig:
    def __init__(self, env_path: Optional[str] = None, yaml_path: Optional[str] = 'app_settings.yml'):
        self.port = DEFAULT_PORT
        self.app_name = DEFAULT_APP_NAME
        self.host = DEFAULT_HOST
        self.app_type = DEFAULT_APP_TYPE
        
        # Try to load from YAML file
        if yaml_path:
            try:
                with open(yaml_path, 'r') as f:
                    yaml_config = yaml.safe_load(f)
                    self.app_type = yaml_config.get('APPTYPE', 'dash')
                    self.app_name = yaml_config.get('APPNAME', DEFAULT_APP_NAME)
                    self.port = yaml_config.get('PORT', DEFAULT_PORT)
                    self.host = yaml_config.get('HOST', DEFAULT_HOST)
            except FileNotFoundError:
                logger.warning(f"YAML file not found: {yaml_path}")
            except Exception as e:
                logger.warning(f"Error loading YAML file: {e}")
        else:
            # If YAML file doesn't exist or doesn't have required keys, load from .env
            load_dotenv(dotenv_path=env_path) if env_path else load_dotenv()
            self.app_type = os.getenv('APPTYPE', self.app_type)
            self.app_name = os.getenv('APPNAME', self.app_name)
            self.port = int(os.getenv('PORT', self.port))
            self.host = os.getenv('HOST', self.host)

        logger.info(f"Loaded configuration: PORT={self.port}, APPTYPE={self.app_type}, APPNAME={self.app_name}")
        
    def validate(self):
        if self.app_type != "dash":
            logger.error("APPTYPE must be set to 'dash' in the .env file or YAML file")
            raise ValueError("APPTYPE must be set to 'dash' in the .env file or YAML file")
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
        serve_locally: bool = True,
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
        self.params = DashConfig(env_path)
        self.params.validate()

        if url_base_pathname is None:
            url_base_pathname = f'/{self.params.app_name}/'
        
        self.serve_locally = serve_locally
        
        logger.info(f"Using URL base pathname: {url_base_pathname}")

        super().__init__(name, 
                         url_base_pathname=url_base_pathname, 
                         serve_locally=serve_locally,
                         routes_pathname_prefix=url_base_pathname,
                         **kwargs)
        logger.info("Dash app initialized successfully")

    def run(self, debug: bool = False, **kwargs) -> None:
        host = self.params.host
        port = self.params.port
        app_name = self.params.app_name
        url = f"http://{host}:{port}/{app_name}"
        logger.info(f"Starting Dash app on {url}")
        print(f"Running app on {url}")
        try:
            super().run(debug=debug, host=host, port=port, **kwargs)
        except Exception as e:
            logger.error(f"Error running Dash app: {str(e)}")
            raise
        
if __name__ == "__main__":
    app = Dash(__name__)
    app.run(debug=True)