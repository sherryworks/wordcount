from flask import Flask, request, render_template
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

def count_english_words(text):
    words = text.split()
    english_words = [w for w in words if w.isascii()]
    return len(english_words)

def count_words_from_url(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()
        return count_english_words(text)
    except Exception as e:
        return f"❌ URL取得に失敗しました：{str(e)}"

@app.route("/", methods=["GET", "POST"])
def index():
    word_count = None
    url_word_count = None
    text = ""
    url_input = ""

    if request.method == "POST":
        if "text" in request.form and request.form["text"]:
            text = request.form["text"]
            word_count = count_english_words(text)

        if "url" in request.form and request.form["url"]:
            url_input = request.form["url"]
            result = count_words_from_url(url_input)
            url_word_count = result if isinstance(result, int) else result  # エラーメッセージ or 数値

    return render_template("index.html",
                           text=text,
                           word_count=word_count,
                           url=url_input,
                           url_word_count=url_word_count)

if __name__ == "__main__":
    app.run()
