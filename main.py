from flask import Flask, request, Response, jsonify
import requests

app = Flask(__name__)

# this will have a map of all the SERVICES and ports
registry = {}

"""
NOTES:
    - don't forget to run it with the compiler that the IDE has
TODOS:
    - remove service route
    - remove node api
    - improve documentation
"""


@app.route('/')  # test route
def home_route():
    return "Hello world!"


@app.route('/registry')
def registry_route():
    return jsonify(registry)


@app.route('/new_service')
def new_service():
    name = request.headers.get('service_name')
    port = request.headers.get('service_port')
    res = Response()
    if name == "" or name is None or port is None:
        res.status_code = 300
        return res
    registry[name] = int(port)
    res.status_code = 200
    return res


@app.route('/new_node')
def new_node():
    name = request.headers.get('node_name')
    rs = request.headers.get('resources')
    ns = request.headers.get('how_many')
    service = request.headers.get('service_name')

    port = registry[service]

    if port is None:
        res = Response()
        res.status_code = 300
        return res
    headers = {
        "node_name": name,
        "resources": rs,
        "how_many": ns
    }
    r = requests.get("http://localhost:" + str(port)+"/new_node", headers=headers)

    return jsonify(r.json())


app.run(port=4444)
