# ec2_dash.py
import os
from typing import Any, Callable
from dash import Dash as OriginalDash
import dotenv

class Dash(OriginalDash):
    """
    A custom Dash wrapper for auto EC2 deployment.
    
    **Note**: Ensure configured PORT is open in the EC2 security group.

    Requires the following environment variables to be set in the .env file:
    - PORT: The port to run the app on (default: 8050)
    - APPTYPE: Must be set to "dash". Other options ("flask", "streamlit") not supported.
    - APPNAME: The name of the app (default: "app")
    """

    def __init__(self, name, env_dir=None, dotenv_path=None, dotenv_dir=None, **kwargs):
        """
        Initialize the Dash instance.

        Args:
            name): The name of the Dash app.
            env_dir: The directory where the .env file is located.
            dotenv_path: The path to the .env file.
            dotenv_dir: The directory where the .env file is located.
            **kwargs: Additional keyword arguments to pass to the original Dash class.
        """
        if dotenv_path:
            dotenv.load_dotenv(dotenv_path=dotenv_path)
        elif dotenv_dir:
            dotenv.load_dotenv(dotenv_path=os.path.join(dotenv_dir, '.env'))
        elif env_dir:
            dotenv.load_dotenv(dotenv_path=os.path.join(env_dir, '.env'))
        else:
            dotenv.load_dotenv()

        APPNAME = os.getenv('APPNAME', 'app')
        super().__init__(name, url_base_pathname=f'/{APPNAME}/', **kwargs)

    def run(self, *args, **kwargs) -> None:
        """
        Run the Dash app.

        Args:
            *args, **kwargs: Args to pass to the O.G. run method.
        """
        debug = kwargs.pop('debug', False)
        host = kwargs.pop('host', '0.0.0.0')
        port = kwargs.pop('port', os.getenv('PORT', 8050))
        super().run(debug=debug, host=host, port=port, *args, **kwargs)

