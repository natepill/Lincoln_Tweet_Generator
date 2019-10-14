from flask import Flask, render_template
from markov import MarkovChain, generate_lincoln_tweet

app = Flask(__name__)

# Art of War
# Confusious text
# How to Win Friends or Influence People
# Any Robert Greene book, ie: 48 laws of Power


@app.route('/')
def index():
    """ Render page with Markov generated tweet """
    generated_tweet = generate_lincoln_tweet('Harry_Potter_ALL_TEXT.txt')
    return render_template('index.html', generated_tweet=generated_tweet)



if __name__ == "__main__":
    app.run(debug=True, port=5000)
