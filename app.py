from flask import Flask, request, render_template

app = Flask(__name__)

def count_english_words(text):
    words = text.split()
    english_words = [w for w in words if w.isascii()]
    return len(english_words)

@app.route("/", methods=["GET", "POST"])
def index():
    word_count = None
    text = ""

    if request.method == "POST":
        if "text" in request.form and request.form["text"]:
            text = request.form["text"]
            word_count = count_english_words(text)

    return render_template("index.html", text=text, word_count=word_count)

if __name__ == "__main__":
    app.run()
