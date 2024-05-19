import pandas as pd
from textblob import TextBlob
from flask import Flask, render_template, request

# Load the dataset
df = pd.read_csv('data/tweets.csv/training.1600000.processed.noemoticon.csv', encoding='ISO-8859-1', names=["target", "ids", "date", "flag", "user", "text"])

# Set up Flask
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    analyzed_tweets = []

    if request.method == 'POST':
        keyword = request.form['keyword'].lower()
        matching_tweets = df[df['text'].str.contains(keyword, case=False, na=False)]

        for _, tweet in matching_tweets.iterrows():
            analysis = TextBlob(tweet['text'])
            sentiment = 'Positive' if analysis.sentiment.polarity > 0 else 'Negative' if analysis.sentiment.polarity < 0 else 'Neutral'
            analyzed_tweets.append({
                'text': tweet['text'],
                'sentiment': sentiment
            })

    return render_template('index.html', tweets=analyzed_tweets)

if __name__ == '__main__':
    app.run(debug=True)
