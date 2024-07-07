# custom_dash.py
import os
from dash import Dash as OriginalDash
import dotenv
dotenv.load_dotenv(dotenv_path='./app_config.env')

class Dash(OriginalDash):
    def __init__(self, name, **kwargs):
        APPNAME = os.getenv('APPNAME', 'dash-app')
        super().__init__(name, url_base_pathname=f'/{APPNAME}/', **kwargs)
    
    def run(self, debug=True, host='0.0.0.0', port=os.getenv('PORT', 8050)):
        super().run_server(debug=debug, host=host, port=port)