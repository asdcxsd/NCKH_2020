from flask import Blueprint, request, Response
from api.v1.output import make_output

RunShell = Blueprint("RunShell", __name__)

# @RunShell.route("/run", methods=["POST"])
# def run_reverse_shell_poc(): 
