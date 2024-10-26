from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from db import store_conversation, get_conversations
import random
from genai_model.genai_model import FinancialAdvisor
import json

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
    "How old are you?",
    "What’s your employment status?",
    "How many people are in your family?",
    "What is your educational background?",
    "What is your residential location?",
    "How long have you lived at your current address?",
    "Do you pay utility bills regularly?",
    "What percentage of your income do you save each month?",
    "What are your top three financial goals for the next year?",
    "Are you currently investing? If so, what types of investments do you have?",
    "How do you typically handle unexpected expenses?",
    "On a scale of 1-10, how would you rate your financial literacy?",
    "What is your preferred method of tracking expenses? (e.g., app, spreadsheet, mental)",
    "Do you have any financial advisors or mentors?",
    "What’s your biggest financial worry right now?",
    "How often do you review your financial statements?",
    "Do you have a budget? If yes, do you stick to it?",
    "Have you ever had to take out a loan? If yes, what for?",
    "What influences your spending habits the most?",
    "How do you prioritize your financial goals?",
    "What financial milestones have you achieved so far?",
    "Are you planning for retirement? If yes, what’s your strategy?",
    "How do you feel about taking financial risks?",
    "What types of financial products are you familiar with? (e.g., stocks, bonds, mutual funds)",
    "Have you ever declared bankruptcy? If yes, what led to that decision?",
    "How do you feel about credit cards? Are they a helpful tool or a burden?",
    "What’s the largest purchase you’ve ever made?",
    "If you could change one thing about your financial situation, what would it be?",
    "Is there any financial information you feel is missing or incomplete?"
]

# Track conversation state
conversation_state = {}


def validate_input(prompt_index, user_input):
    if prompt_index == 1:  # Monthly income
        return user_input.isdigit() and int(user_input) >= 0
    elif prompt_index == 2:  # Monthly expenses
        return user_input.isdigit() and int(user_input) >= 0
    elif prompt_index == 3:  # Assets
        return len(user_input) > 0  # Ensure user provides some response
    elif prompt_index == 4:  # Liabilities
        return len(user_input) > 0  # Ensure user provides some response
    elif prompt_index == 5:  # Age
        return user_input.isdigit() and 0 < int(user_input) < 65  # Valid age
    elif prompt_index == 6:  # Employment status
        return len(user_input) > 0  # Must not be empty
    elif prompt_index == 7:  # Family size
        return user_input.isdigit() and int(user_input) > 0  # Must be a positive number
    elif prompt_index == 8:  # Educational background
        return len(user_input) > 0  # Ensure user provides some response
    elif prompt_index == 9:  # Residential location
        return len(user_input) > 0  # Ensure user provides some response
    elif prompt_index == 10:  # Duration at current address
        return user_input.isdigit() and int(user_input) >= 0  # Must be a non-negative number
    elif prompt_index == 11:  # Utility bills
        return user_input.lower() in ['yes', 'no']  # Expecting yes or no
    elif prompt_index == 12:  # Savings percentage
        return user_input.isdigit() and 0 <= int(user_input) <= 100  # 0-100 percent
    elif prompt_index == 13:  # Financial goals
        return len(user_input) > 0  # Ensure user provides some response
    elif prompt_index == 14:  # Investments
        return len(user_input) > 0  # Ensure user provides some response
    elif prompt_index == 15:  # Handling unexpected expenses
        return len(user_input) > 0  # Ensure user provides some response
    elif prompt_index == 16:  # Financial literacy rating
        return user_input.isdigit() and 1 <= int(user_input) <= 10  # Scale of 1-10
    elif prompt_index == 17:  # Tracking expenses method
        return len(user_input) > 0  # Ensure user provides some response
    elif prompt_index == 18:  # Financial advisors
        return len(user_input) > 0  # Ensure user provides some response
    elif prompt_index == 19:  # Biggest financial worry
        return len(user_input) > 0  # Ensure user provides some response
    elif prompt_index == 20:  # Review frequency
        return len(user_input) > 0  # Ensure user provides some response
    elif prompt_index == 21:  # Budget
        return user_input.lower() in ['yes', 'no']  # Expecting yes or no
    elif prompt_index == 22:  # Loan history
        return len(user_input) > 0  # Ensure user provides some response
    elif prompt_index == 23:  # Spending habits influences
        return len(user_input) > 0  # Ensure user provides some response
    elif prompt_index == 24:  # Financial goals prioritization
        return len(user_input) > 0  # Ensure user provides some response
    elif prompt_index == 25:  # Financial milestones
        return len(user_input) > 0  # Ensure user provides some response
    elif prompt_index == 26:  # Retirement planning
        return len(user_input) > 0  # Ensure user provides some response
    elif prompt_index == 27:  # Financial risks attitude
        return len(user_input) > 0  # Ensure user provides some response
    elif prompt_index == 28:  # Financial products familiarity
        return len(user_input) > 0  # Ensure user provides some response
    elif prompt_index == 29:  # Bankruptcy
        return len(user_input) > 0  # Ensure user provides some response
    elif prompt_index == 30:  # Credit cards opinion
        return len(user_input) > 0  # Ensure user provides some response
    elif prompt_index == 31:  # Largest purchase
        return len(user_input) > 0  # Ensure user provides some response
    elif prompt_index == 32:  # Change in financial situation
        return len(user_input) > 0  # Ensure user provides some response
    elif prompt_index == 33:  # Missing financial information
        return len(user_input) > 0  # Ensure user provides some response

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

@app.route('/score', methods=['GET'])
def get_score():
    # Generate a random score between 0 and 100
    score = random.randint(0, 100)
    return jsonify({'score': score})


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
