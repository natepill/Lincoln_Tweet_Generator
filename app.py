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
    generated_tweet = generate_lincoln_tweet('lincoln-speeches.txt')
    return render_template('startbootstrap-freelancer/index.html', generated_tweet=generated_tweet)



if __name__ == "__main__":
    app.run(debug=True, port=4000)
