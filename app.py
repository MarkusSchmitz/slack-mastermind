from flask import Flask, jsonify, request
from transformers import pipeline
import json
from loguru import logger
import sys

logger.add("log.txt", format="{time} {level} {message}", filter="my_module", level="INFO")


app = Flask(__name__)

pipe = pipeline('text-generation', model="dbmdz/german-gpt2",
                 tokenizer="dbmdz/german-gpt2")

@app.route("/")
def hello():
    logger.info("Returned static")
    return "Hello, Sebastian!"



@app.route('/slack-endpoint', methods=['POST', "GET"])
def endpoint():

    logger.info("received event")
    logger.info('recieved data is: {request.data}')
    
    with open("log.txt", "ab") as f:
        f.write(request.data)


    answer = {
        "text" : "Random Text"
    }

    logger.info("responding with {answer}")
    return jsonify(answer)
        
    #else:
        # You probably don't have args at this route with GET
        # method, but if you do, you can access them like so:
    #    yourarg = flask.request.args.get('argname')
    #    your_register_template_rendering(yourarg)

def predict(text):
    

    text = pipe("Der Sinn des Lebens ist es", max_length=100)[0]["generated_text"]
    return text


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
    
