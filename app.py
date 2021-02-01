from flask import Flask, send_from_directory
from api.v1.target import Target
from api.v1.reconnaissance import Recon
from api.v1.poc import Poc
from api.v1.uploadfile import Upload
from database import connect as connect_DB
FOLDER_ROOT = ""


def create_app():
    app = Flask(__name__, static_url_path="")
    global FOLDER_ROOT
    #--
    @app.route('/public/<path:path>')
    def send_js(path):
        return send_from_directory('public', path)

    connect_DB()

    app.register_blueprint(Target, url_prefix='/api/v1/target')
    app.register_blueprint(Recon, url_prefix='/api/v1/reconnaissance')
    app.register_blueprint(Poc, url_prefix='/api/v1/pocs')
    app.register_blueprint(Upload, url_prefix='/api/v1/reconnaissance')
    return app


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port
    app = create_app()
    
    app.run(host='0.0.0.0', port=port)