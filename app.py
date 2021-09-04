from flask import Flask
from flask import request
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello, Sebastian!"


@app.route('/slack-endpoint', methods=['POST', "GET"])
def endpoint():
    
    with open("log.txt", "ab") as f:
        f.write(request.data)

    return str(request.data)
        
    #else:
        # You probably don't have args at this route with GET
        # method, but if you do, you can access them like so:
    #    yourarg = flask.request.args.get('argname')
    #    your_register_template_rendering(yourarg)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
