
from api.v2.Input.run import RunInput
from flask import Flask, send_from_directory
from api.v2.Module.main import Main
from api.v2.Input.target import Target
from api.v2.Module.recon import ManageRecon
from api.v2.Module.exploit import Exploit  
from api.v2.Module.ToolManager import ToolManager
from api.v2.Module.pocmanager import POCManager
from api.v2.Module.shell import RunShell
from api.v2.Module.input import Input
import os

#from Database.database import connect as connect_DB
import requests
from Application.Function.Connect_Database import connect

def create_app():
    app = Flask(__name__, static_url_path="")

    #--
    @app.route('/public/<path:path>')
    def send_js(path):
        return send_from_directory('PUBLIC', path)

    #connect_DB()
    connect()

    app.register_blueprint(Target, url_prefix='/api/v2/target')
    app.register_blueprint(RunInput,url_prefix='/api/v2/input')
    app.register_blueprint(Main,url_prefix='/api/v2/module')
    app.register_blueprint(ManageRecon, url_prefix='/api/v2/managerecon')
    app.register_blueprint(Exploit, url_prefix="/api/v2/exploit")
    app.register_blueprint(ToolManager, url_prefix="/api/v2/managetool")
    app.register_blueprint(POCManager, url_prefix="/api/v2/managepoc")
    app.register_blueprint(RunShell, url_prefix="/api/v2/shell")
    app.register_blueprint(Input, url_prefix="/api/v2/input")
    return app


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=8089, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port
    if os.geteuid() != 0:
        exit("You need to have root privileges to run this script.\nPlease try again, this time using 'sudo'. Exiting.")
    app = create_app()
    app.run(host='0.0.0.0', port=port, debug=False)