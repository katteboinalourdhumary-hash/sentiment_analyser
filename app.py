from flask import Flask, render_template, request
from textblob import TextBlob
import re

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():

    statement = ""
    polarity = 0
    sentiment = ""

    positive = 0
    negative = 0
    neutral = 0

    if request.method == "POST":

        statement = request.form["statement"]

        # Overall polarity
        analysis = TextBlob(statement)
        polarity = analysis.sentiment.polarity

        # Split the statement into parts
        parts = re.split(
            r",|\bbut\b|\bhowever\b|\balthough\b|\bthough\b|\band\b",
            statement,
            flags=re.IGNORECASE
        )

        parts = [part.strip() for part in parts if part.strip()]

        # Analyze each part
        for part in parts:

            part_analysis = TextBlob(part)
            score = part_analysis.sentiment.polarity

            if score > 0:
                positive += 1

            elif score < 0:
                negative += 1

            else:
                neutral += 1

        # Calculate percentages
        total = positive + negative + neutral

        if total > 0:
            positive = round((positive / total) * 100, 2)
            negative = round((negative / total) * 100, 2)
            neutral = round((neutral / total) * 100, 2)

        # Overall sentiment
        if polarity > 0:
            sentiment = "Positive"

        elif polarity < 0:
            sentiment = "Negative"

        else:
            sentiment = "Neutral"

    return render_template(
        "index.html",
        statement=statement,
        polarity=polarity,
        sentiment=sentiment,
        positive=positive,
        negative=negative,
        neutral=neutral
    )


if __name__ == "__main__":
    app.run(debug=True)