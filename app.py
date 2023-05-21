from flask import Flask, render_template, request, session
from chatbot import response_generator

def process_user_input(msg):


app = Flask(__name__)
app.secret_key = 'chatwithbot'



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chatbot', methods=['POST'])
def chatbot():
    # Process the user's input and generate a response
    user_input = request.form['user_input']
    bot_response = process_user_input(user_input)  # Replace with your chatbot logic

    # Retrieve previous messages from the session or initialize an empty list
    messages = session.get('messages', [])

    # Add the new user input and bot response to the messages list
    messages.append({'sender': 'User', 'content': user_input})
    messages.append({'sender': 'Bot', 'content': bot_response})

    # Update the messages list in the session
    session['messages'] = messages

    # Return the response to the chatbot page
    return render_template('chatbot.html', messages=messages)


if __name__ == '__main__':
    app.run(debug=True)
