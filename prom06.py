#! /bin/bash
# PROM06 - Research Project.
# By Glenn Tam, bi40fi@student.sunderland.ac.uk
import re
import nltk
import string
import sqlite3
import sys
import warnings
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Initialiase startup variables
app = Flask(__name__)
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)


# Web app routes
@app.route("/")
def index():
    session["corpus"] = ""
    return render_template('index.html')


@app.route("/bot", methods=['POST', 'GET'])
def get_bot_response():
    if request.method == 'GET':
        userText = request.args.get('msg')
        state = int(userText[0])
        if state < 2:  # parent chatbot
            return str(append_to_corpus(userText[1:]))
        elif state == 2:  # create new chatbot
            return str(create_new_chatbot())
        elif state > 2:  # child chatbot
            return str(generate_response(userText[1:]))
        else:
            pass
    if request.method == 'POST':  # user submits feedback survey
        sane_data = (int(request.form.get('q1')),
                     int(request.form.get('q2')),
                     int(request.form.get('q3')),
                     int(request.form.get('q4')),
                     int(request.form.get('q5')),
                     int(request.form.get('q6')),
                     int(request.form.get('q7')),
                     int(request.form.get('q8')),
                     int(request.form.get('q9')),
                     int(request.form.get('q10')),
                     str(request.form.get('feedbackBox')),
                     str(session['corpus']))
        conn = get_db_connection()
        conn.cursor().execute("INSERT INTO survey(q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, feedback, corpus) \
                               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", sane_data)
        conn.commit()
        conn.close ()
        print(sane_data)
        session.clear()
        return redirect('thankyou')


@app.route("/thankyou")
def thankyou():
    return render_template('thankyou.html')


# Helper functions
def append_to_corpus(user_input):
    """Add user input to corpus."""
    user_input += ". "
    session['corpus'] += user_input
    return "Got it. You can still input more training data. Otherwise, click the red button below to train your new AI."


def create_new_chatbot():
    """Create chatbot based on user-given corpus."""
    text = session['corpus']
    text = text.lower()
    text = re.sub(r'\[[0-9]*\]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    sentences = nltk.sent_tokenize(text)
    words = nltk.word_tokenize(text)
    warnings.filterwarnings("ignore")
    session['sentences'] = sentences
    return "Hi! I'm your new chatbot. I've been created to answer things from your training data. Try to ask me something now."


def get_db_connection():
    """Establish database connection."""
    conn = None
    try:
        conn = sqlite3.connect('prom06.db')
    except Error as e:
        print(e)
    return conn


def generate_response(user_input):
    """Return a response given some input based on the first chatbot conversation."""
    new_chatbot_response = ''
    sentences = session['sentences']
    sentences.append(user_input)
    def perform_lemmatisation(tokens):
        """Lemmatise a list of tokens."""
        wnlemmatizer = nltk.stem.WordNetLemmatizer()
        return [wnlemmatizer.lemmatize(token) for token in tokens]
    def get_processed_text(document):
        """Process a list of lemmatised tokens."""
        punctuation_removal = dict((ord(punctuation), None) for punctuation in string.punctuation)
        return perform_lemmatisation(nltk.word_tokenize(document.lower().translate(punctuation_removal)))
    word_vectorizer = TfidfVectorizer(tokenizer=get_processed_text, stop_words='english')
    try:
        all_word_vectors = word_vectorizer.fit_transform(sentences)
    except ValueError:  # if vocab list is empty
        return (str(ValueError))
    similar_vector_values = cosine_similarity(all_word_vectors[-1], all_word_vectors)
    try:
        similar_sentence_number = similar_vector_values.argsort()[0][-2]
    except IndexError:
        return (str(IndexError))
    matched_vector = similar_vector_values.flatten()
    matched_vector.sort()
    vector_matched = matched_vector[-2]
    if vector_matched == 0:
        new_chatbot_response += "I'm not sure what you mean, you might have to train me on more data. But I can tell you that, " + sentences[similar_sentence_number]
    else:
        new_chatbot_response = new_chatbot_response + sentences[similar_sentence_number]
    sentences.remove(user_input)
    return new_chatbot_response


# Start web app
if __name__ == "__main__":
    """Start web app."""
    if sys.version_info[0:2] != (3, 11):
        raise Exception('This software requires Python 3.10')
    app.run(debug=False)
