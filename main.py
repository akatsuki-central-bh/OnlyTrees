from flask import Flask, render_template, request

app = Flask(__name__, static_folder='public')

@app.route('/')
def hello_world():
  return 'hello world'
