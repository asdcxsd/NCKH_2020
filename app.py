from flask import Flask
from api.v1.target import Target
from api.v1.reconnaissance import Recon
from api.v1.poc import Poc
from database import connect as connect_DB
FOLDER_ROOT = ""
def create_app():
    app = Flask(__name__)
    global FOLDER_ROOT
    #--
    connect_DB()

    app.register_blueprint(Target, url_prefix='/api/v1/target')
    app.register_blueprint(Recon, url_prefix='/api/v1/reconnaissance')
    app.register_blueprint(Poc, url_prefix='/api/v1/pocs')
    return app


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port
    app = create_app()
    
    app.run(host='0.0.0.0', port=port)