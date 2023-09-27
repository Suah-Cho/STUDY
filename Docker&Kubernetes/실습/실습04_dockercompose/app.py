from flask import *
import socket

app = Flask(__name__)

@app.route("/") 
def hello() :
    return  "<h1> Hello Docker !! and Flask!!! </h1>"

@app.route("/whoareyou")
def whoareyou() :
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()


    return "<h1>"+ip+"</h1>"


if __name__ == "__main__" :
    app.run()