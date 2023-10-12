from flask import Flask
import os
import socket

app = Flask(__name__)


@app.route("/whoareyou")
def whoareyou():
    hostname = os.getenv('HOSTNAME', '')
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 53))
    ip = s.getsockname()[0]
    s.close()
    name = '조수아'


    return name + " : " + hostname + " : " + ip + "\n"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)