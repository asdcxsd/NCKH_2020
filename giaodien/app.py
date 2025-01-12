from flask import Flask, render_template
from url.target.target import Target
from url.login.login import Login
from url.exploit.exploit import Exploit
from url.manager.pocmanager import POCManager
from url.manager.toolmanager import ToolManager
from url.recon.recon import Recon
from url.start.start import Start
from url.setting.setting import Setting
from url.Input.input import Input
from url.profile.profile import Profile
from flask_wtf.csrf import CSRFProtect
from os import urandom


app = Flask(__name__, template_folder='templates')
CSRFProtect(app)
app.config['SECRET_KEY'] = urandom(0x200)

app.register_blueprint(Start)
app.register_blueprint(Target)
app.register_blueprint(Input)
app.register_blueprint(Recon)
app.register_blueprint(Login)
app.register_blueprint(Exploit)
app.register_blueprint(POCManager)
app.register_blueprint(ToolManager)
app.register_blueprint(Setting)
app.register_blueprint(Profile)


if __name__ == "__main__": 
    app.run(host="0.0.0.0", port=5002)
