from flask import Flask, send_from_directory
from api.v1.target import Target
from api.v1.Reconnai.reconnaissance import Recon
from api.v1.Exploit.poc import Poc
from api.v1.Exploit.shell import Shell
from api.v1.Reconnai.report import Report
from Database.database import connect as connect_DB



def create_app():
    app = Flask(__name__, static_url_path="")

    #--
    @app.route('/public/<path:path>')
    def send_js(path):
        return send_from_directory('PUBLIC', path)

    connect_DB()

    app.register_blueprint(Target, url_prefix='/api/v1/target')
    app.register_blueprint(Recon, url_prefix='/api/v1/reconnaissance')
    app.register_blueprint(Poc, url_prefix='/api/v1/pocs')
    app.register_blueprint(Shell, url_prefix='/api/v1/pocs')
    app.register_blueprint(Report, url_prefix='/api/v1/reconnaissance')
    return app


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=8089, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port
    app = create_app()
    
    app.run(host='0.0.0.0', port=port)