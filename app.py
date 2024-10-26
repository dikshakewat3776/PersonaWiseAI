from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from db import store_conversation, get_conversations
import random
from genai_model.genai_model import FinancialAdvisor, FinancialPersonaCollector
import json
from genai_model.score import compute_score_data, calculate_financial_score

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key


@app.route('/test')
def test():
    return "Flask is working!"


@app.route('/')
def index():
    session['progress'] = 0
    return render_template('index.html')


# @app.route('/submit', methods=['POST'])
# def submit():
#     if 'data' not in session:
#         session['data'] = {}
#
#     # Get user data from form
#     user_data = request.form
#     session['data'].update(user_data)
#
#     # Calculate progress based on filled fields
#     total_fields = 5  # Adjust based on total fields you want to capture
#     filled_fields = sum(1 for value in session['data'].values() if value)
#     session['progress'] = (filled_fields / total_fields) * 100
#
#     return redirect(url_for('report'))
#
# @app.route('/report')
# def report():
#     return render_template('report.html', data=session.get('data'), progress=session.get('progress', 0))


# Define prompts
prompts = [
    "Hello! I’m PersonaWiseAI, your personal financial assistant. To help you build a tailored financial profile, please share your financial and demographic information.",
    "What’s your monthly income?",
    "What are your monthly expenses?",
    "Do you have any assets? (e.g., property, savings)",
    "What are your liabilities? (e.g., loans, debts)",
    "What’s your employment status?",
    "How many people are in your family?",
    "What is your educational background?",
    "Do you pay utility bills regularly?",
    "Are you currently investing? If so, what types of investments do you have?",
    "What is your preferred method of tracking expenses? (e.g., app, spreadsheet, mental)",
    "What types of financial products are you familiar with? (e.g., stocks, bonds, mutual funds)",
    "Have you ever declared bankruptcy? If yes, what led to that decision?",
    "How do you feel about credit cards? Are they a helpful tool or a burden?",
    "What’s the largest purchase you’ve ever made?",
    "Is there any financial information you feel is missing or incomplete?"
]

# Track conversation state
conversation_state = {}


def validate_input(prompt_index, user_input):
    if prompt_index:
        return len(user_input) > 0
    return True  # Default case


@app.route('/conversation', methods=['POST'])
def conversation():
    user_id = request.json.get('user_id')
    user_input = request.json.get('message')

    if user_id not in conversation_state:
        conversation_state[user_id] = {'current_prompt': 0, 'responses': {}}

    current_prompt_index = conversation_state[user_id]['current_prompt']

    # Validate user input
    if user_input and not validate_input(current_prompt_index, user_input):
        return jsonify({"error": "Invalid input. Please try again."})

    # Store user response
    conversation_state[user_id]['responses'][prompts[current_prompt_index]] = user_input
    conversation_state[user_id]['current_prompt'] += 1

    # print("here`````````")
    store_conversation(user_id, prompts[current_prompt_index], conversation_state[user_id]['responses'])

    # Check if we reached the end of the prompts
    if conversation_state[user_id]['current_prompt'] >= len(prompts):
        response = {"message": "Thank you for providing your information!"}
        del conversation_state[user_id]  # Clear the state for this user
    else:
        response = {"next_prompt": prompts[conversation_state[user_id]['current_prompt']]}
    # print(response)
    return jsonify(response)


# @app.route('/conversation', methods=['POST'])
# def conversation():
#     user_id = request.json.get('user_id')
#     user_input = request.json.get('message')
#     collecting_data = True
#
#     if user_id not in conversation_state:
#         # Prompt user for input
#         conversation_state[user_id] = {'current_prompt': 0, 'responses': {}}
#         current_prompt_index = conversation_state[user_id]['current_prompt']
#         response = {"message": prompts[current_prompt_index]}
#         return jsonify(response)
#
#     while collecting_data:
#         print("here1------------" + str(user_input))
#         # Parse the user input with LLaMA
#         financial_persona_collect = FinancialPersonaCollector()
#         parsed_data = financial_persona_collect.parse_with_llama(user_input)
#         print("here2------------" + str(parsed_data))
#         # Update user data with parsed information
#         financial_persona_collect.update_user_data(parsed_data)
#         store_conversation(user_id, user_input, parsed_data)
#         if len(financial_persona_collect.user_data) > 5:
#             response = {"message": "Thank you for providing your information!"}
#             del conversation_state[user_id]  # Clear the state for this user
#         else:
#             response = {"message": parsed_data}
#         return jsonify(response)


@app.route('/score', methods=['GET'])
def get_score():
    # Generate a random score between 0 and 100
    score = random.randint(0, 100)
    return jsonify({'score': score})

#
# @app.route('/score', methods=['POST'])
# def get_score():
#     # # Generate a random score between 0 and 100
#     # score = random.randint(0, 100)
#     user_id = request.json.get('user_id')
#     print('Generating score for User Id: ' + str(user_id))
#     user_conversation = get_conversations(user_id=user_id)
#     if not user_conversation:
#         return jsonify({'score': 0})
#     if not user_conversation[0].get('bot_response'):
#         return jsonify({'score': 0})
#     bot_data = user_conversation[0].get('bot_response')
#     if bot_data:
#         first_key = list(bot_data.keys())[0]
#         del bot_data[first_key]  # Delete the first key-value pair
#     print('Generating score with bot data: ' + str(bot_data))
#     score_data = compute_score_data(bot_data)
#     score_response = calculate_financial_score(score_data)
#     print('Generated score data: ' + str(score_response))
#     store_conversation(user_id, '', score_data)
#     return jsonify({'score': score_response.get('Score')})


@app.route('/verify', methods=['GET'])
def verify_user():
    # Generate a random score between 0 and 100
    score = random.randint(0, 100)
    return jsonify({'score': score})


@app.route('/advice', methods=['POST'])
def advice_user():
    user_id = request.json.get('user_id')
    print('Generating advice for User Id: ' + str(user_id))
    user_conversation = get_conversations(user_id=user_id)
    if not user_conversation:
        return jsonify({"error": "Could not generate advice. Please try again."})
    if not user_conversation[0].get('bot_response'):
        return jsonify({"error": "Could not generate advice. Please try again."})
    bot_data = user_conversation[0].get('bot_response')
    if bot_data:
        first_key = list(bot_data.keys())[0]
        del bot_data[first_key]  # Delete the first key-value pair
    print('Generating advice with bot data: ' + str(bot_data))
    data = FinancialAdvisor().parse_with_llama(content=bot_data)
    store_conversation(user_id, '', data)
    print('Generated advice data type: ' + str(type(data)))
    print('Generated advice data: ' + str(data))
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
