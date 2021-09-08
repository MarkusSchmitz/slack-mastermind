from flask import Flask, jsonify, request
from transformers import AutoModelForCausalLM, AutoTokenizer
import json
from loguru import logger
import sys

logger.add("log.txt", format="{time} {level} {message}", filter="my_module", level="INFO")


app = Flask(__name__)

tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-large")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-small")

@app.route("/")
def hello():
    new_user_input_ids = tokenizer.encode("How are you doing?" + tokenizer.eos_token, return_tensors='pt')

    # append the new user input tokens to the chat history
    bot_input_ids = new_user_input_ids

    # generated a response while limiting the total chat history to 1000 tokens, 
    chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)

    # pretty print last ouput tokens from bot
    answer = ("{}".format(tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)))

    logger.info("responding with {answer}")
    return jsonify(answer)



@app.route('/slack-endpoint', methods=['POST', "GET"])
def endpoint():

    logger.info("received event")
    logger.info('recieved data is: {request.data}')
    
    with open("log.txt", "ab") as f:
        f.write(request.data)


    answer = {
        "text" : "Random Text"
    }

    new_user_input_ids = tokenizer.encode(request.data["text"] + tokenizer.eos_token, return_tensors='pt')

    # append the new user input tokens to the chat history
    bot_input_ids = new_user_input_ids

    # generated a response while limiting the total chat history to 1000 tokens, 
    chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)

    # pretty print last ouput tokens from bot
    answer = ("{}".format(tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)))

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
    
