#! /bin/bash
# PROM06 - Research Project.
# By Glenn Tam, bi40fi@student.sunderland.ac.uk

#############################################################################
#                                                                           #
#  PLEASE NOTE                                                              #
#                                                                           #
#  This is a strictly command line version of the PROM06 project.           #
#                                                                           #
#  This is an old, obsolete version, previously submitted for Assignment 1. #
#  It is saved here only for historical reference.                          #
#                                                                           #
#############################################################################

import random
import re
import nltk
import string
import warnings
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def perform_lemmatisation(tokens):
    """Lemmatise a list of tokens."""
    return [wnlemmatizer.lemmatize(token) for token in tokens]


def get_processed_text(document):
    """Process a list of lemmatised tokens."""
    return perform_lemmatisation(nltk.word_tokenize(document.lower().translate(punctuation_removal)))


def generate_response(user_input):
    """Return a response given some input based on the first chatbot conversation."""
    new_chatbot_response = ''
    sentences.append(user_input)

    word_vectorizer = TfidfVectorizer(tokenizer=get_processed_text, stop_words='english')
    all_word_vectors = word_vectorizer.fit_transform(sentences)
    similar_vector_values = cosine_similarity(all_word_vectors[-1], all_word_vectors)
    similar_sentence_number = similar_vector_values.argsort()[0][-2]

    matched_vector = similar_vector_values.flatten()
    matched_vector.sort()
    vector_matched = matched_vector[-2]

    if vector_matched == 0:
        new_chatbot_response += "I'm not sure what you mean, you might have to train me on more data. But I can tell you that, " + sentences[similar_sentence_number]
        return new_chatbot_response
    else:
        new_chatbot_response = new_chatbot_response + sentences[similar_sentence_number]
        return new_chatbot_response


if __name__ == "__main__":
    """Begin the first chatbot that will create the second chatbot."""
    print("\n\n******************************\n")
    print("CHATBOT:\nHi, I'm a University of Sunderland research project on chatbots.")
    print("By continuing to use this chatbot you agree to the following: https://docs.google.com/document/d/1BH3eHY3PumeN4nPgzKRXf4iw7Omd7AMw0ZUlNqM3cCU/edit?usp=sharing")
    print("\nI can help create your own personalised chatbot. What do you want to call your new Chatbot?\n\nYOU:")
    name = input().upper()
    print(f"\nCHATBOT:\nYour new chatbot will be called {name}.")
    print(f"\nWhat are some of the things {name} should know about? You can tell me one line at a time, or copy and paste a block of text).\n\nYOU:")

    text = ""
    user_input = ""
    finished = {'no', 'nope', 'finished', 'done', 'next'}
    while True:
        user_input = input()
        if user_input.lower() in finished:
            break
        user_input += ". "
        text += user_input
        print("\n\nCHATBOT:\nAnything else? (type 'no' to exit).\n\nYOU:")

    print("\nCHATBOT:\nOk. Creating your new chatbot now...")
    text = text.lower()
    text = re.sub(r'\[[0-9]*\]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    sentences = nltk.sent_tokenize(text)
    words = nltk.word_tokenize(text)
    sentences = nltk.sent_tokenize(text)
    words = nltk.word_tokenize(text)
    wnlemmatizer = nltk.stem.WordNetLemmatizer()
    punctuation_removal = dict((ord(punctuation), None) for punctuation in string.punctuation)
    warnings.filterwarnings("ignore")
    print("...done!")

    # Second chatbot starts here
    print("\n\n******************************\n")
    print(f"{name}:\nHello, I'm {name}. What do you want to know about? Type 'bye' to quit.")
    goodbye = {'','bye', 'goodbye','exit','quit'}
    while True:
        print("\nYOU:")
        new_bot_input = input()
        if new_bot_input.lower() in goodbye:
            break
        print(f"\n{name}:")
        print(generate_response(new_bot_input) + " (Type 'bye' to quit)")
        sentences.remove(new_bot_input)
    print(f"\n{name}:\nGoodbye!")

    # Feedback research
    print("\n\n******************************\n")
    print("\nCHATBOT:\nThank you for participating in this chatbot research study. Would you like to participate in a quick survey?\n")
    print("\nYOU:")
    feedback = input()
    no_feedback = {'', 'n', 'no', 'nope', 'quit', 'exit'}
    if feedback.lower() not in no_feedback:
        print('')
        questions = ['"I think that I would like to use this system frequently."',
                     '"I found the system unnecessarily complex."',
                     '"I thought the system was easy to use."',
                     '"I think that I would need the support of a technical person to be able to use this system."',
                     '"I found the various functions in this system were well integrated."',
                     '"I thought there was too much inconsistency in this system."',
                     '"I would imagine that most people would learn to use this system very quickly."',
                     '"I found the system very cumbersome to use."',
                     '"I felt very confident using the system."',
                     '"I needed to learn a lot of things before I could get going with this system."']
        for q in questions:
            print(f"\n{q}\n")
            response = input("Please enter a number between 1 to 5 (1 is 'Strongly Disagree' and 5 is 'Strongly Agree'): ")
            # save responses for study later

        print("\nCHATBOT:\nFinal question. How likely is it that you would recommend this chatbot to a friend or colleague?")
        response = input("0 to 10. (0 is not at all likely. 10 is extremely likely): ")
        response = input("Why? (Feel free to elaborate): ")

    print("\nCHATBOT:\nOk. Thank you for participating in this chatbot research study. Goodbye!")
