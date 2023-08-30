from flask import Flask, request, jsonify
import json

app = Flask(__name__)


@app.route("/stats", methods=["GET"])
def yo_momma():
    return "<p>Shut Up Nerd</p>"


@app.route("/stats/submit", methods=["POST"])
def lil_staty():
    staty = request.json

    print("$$$$$$$$$$$$$$$$$$$$$$$$$$ /stats $$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print(staty)

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

@app.route("/playersinfo", methods=["POST"])
def player_info():
    ur_garbage_kd = request.json

    print("$$$$$$$$$$$$$$$$$$$$$$$$$$ /playersinfo $$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print(ur_garbage_kd)

    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)