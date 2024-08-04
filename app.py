from flask import Flask, request, jsonify, render_template
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from collections import defaultdict
import string

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')

app = Flask(__name__)


def summarize(text, num_sentences=3):
    # Tokenize the text into sentences
    sentences = sent_tokenize(text)

    # Tokenize the text into words
    words = word_tokenize(text.lower())

    # Filter out stopwords and punctuation
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words and word not in string.punctuation]

    # Calculate word frequencies
    word_frequencies = defaultdict(int)
    for word in words:
        word_frequencies[word] += 1

    # Calculate sentence scores based on word frequencies
    sentence_scores = defaultdict(int)
    for sentence in sentences:
        for word in word_tokenize(sentence.lower()):
            if word in word_frequencies:
                sentence_scores[sentence] += word_frequencies[word]

    # Select the top sentences
    sorted_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)
    summary = ' '.join(sorted_sentences[:num_sentences])

    return summary


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/summarize', methods=['POST'])
def summarize_text():
    text = request.form['text']
    num_sentences = int(request.form.get('num_sentences', 3))
    summary = summarize(text, num_sentences)
    return jsonify({'summary': summary})


if __name__ == '__main__':
    app.run(debug=True)
