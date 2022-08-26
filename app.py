import sys
from subprocess import Popen
from contextlib import closing
from flask import Flask, jsonify, request, Response, send_from_directory
#from control  import forward, backward, rotate1, rotate2, cleanup, stop
from flask_jwt_extended import create_access_token, \
create_refresh_token, set_access_cookies, set_refresh_cookies

STREAMING = False

app = Flask(__name__)

# def find_free_port():
#     with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
#         s.bind(('', 0))
#         s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#         return s.getsockname()[1]

username="admin"
password="nimda"

@app.route('/login', methods=('POST',))
def login():
  data = request.get_json()
  uname = data['username']
  passwd = data['password']
  user = username == uname and password == passwd
  if user:
    access_token = create_access_token(identity=user.user_id)
    refresh_token = create_refresh_token(identity=user.user_id)

    response = jsonify()
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)
    return response, 201
  else:
    return jsonify(message="Unauthorized"), 401

@app.route("/", defaults=dict(filename=None))
@app.route("/<path:filename>", methods=["GET"])
def index(filename):
    """
        Serve static assets from public folder.
    """

    return send_from_directory("../client/public", filename or "index.html")


# @app.route("/port", methods=["POST"])
# def new_client():
#     port = find_free_port()
#     Popen(['python', 'src/worker.py', str(port)],
#           stdout=sys.stdout, stderr=sys.stderr)

#     # for line in process.stdout:
#     #     if line == "SUBPROCESS_READY" :
#     #         break
#     #     print(line)

#     sleep(10)

#     return {"port": port}

success_resp = Response("{'status':'success'}", status=200, mimetype='application/json')

# @app.route('/control', methods = ['GET'])
# def control():
#     arg = request.args.get("mov")
#     print(arg)
#     if arg:
#         if(arg == 'w'):
#             forward()
#             return success_resp
#         elif (arg == 's'):
#             backward()
#             return success_resp
#         elif (arg == 'a'):
#             rotate1()
#             return success_resp
#         elif (arg == 'd'):
#             rotate2()
#             return success_resp
#         elif(arg == 'br'):
#             stop()
#             return success_resp
#         else:
#             return Response("{'error':'Invalid command'}", status=400, mimetype='application/json')
#     else:
#         return Response("{'error':'Invalid command'}", status=400, mimetype='application/json')


if __name__ == "__main__":
    # Start the main server
    try:
        if STREAMING:
            web_proc = Popen(['python3', 'websocket_con.py', str(11324)],stdout=sys.stdout, stderr=sys.stderr)
        app.run(port=8080, host='0.0.0.0')

    finally:
        if STREAMING:
            web_proc.terminate()

