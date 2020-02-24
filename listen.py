import os
import secrets

from datetime import datetime

from flask import Flask, request, session

# This port number must match the one in broadcast.py on the clients.
port = 5000

ips = dict()

app = Flask(__name__)


def report(ips):
    os.system("clear")

    print(79 * "=")
    print(
        "Broadcasted IPs - Last update: "
        + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    print(79 * "-")

    for ip in sorted(ips):
        if (datetime.now() - ips[ip]["datetime"]).seconds < 150:
            print(ips[ip]["datetime"].strftime("%Y-%m-%d %H:%M:%S"), end=": ")
            print(ip, end=", ")
            print(ips[ip].get("hostname", ""), end=", ")
            print(ips[ip].get("info", ""))

    print(79 * "-")
    print()


@app.route("/ip_listen", methods=["POST"])
def listen():
    json_ = request.get_json()

    if "ip" in json_:
        ip = json_["ip"]
        info = dict(
            hostname=json_.get("hostname", None),
            info=json_.get("info", None),
            datetime=datetime.now(),
        )

        ips[ip] = info

    report(ips)

    return "200"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=port)
