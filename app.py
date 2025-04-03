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
        print(f"🔎 Fetching: {url}")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        response = requests.get(url, timeout=10, headers=headers)
        if response.status_code != 200:
            return f"❌ ステータスコード: {response.status_code}"
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()
        count = count_english_words(text)
        print(f"✅ Words counted: {count}")
        return count
    except Exception as e:
        print(f"❌ Error fetching URL: {e}")
        return f"❌ URL取得に失敗しました：{str(e)}"


@app.route("/", methods=["GET", "POST"])
def index():
    word_count = None
    url_word_count = None
    text = ""
    url_input = ""

    if request.method == "POST":
        # テキスト入力がある場合
        if "text" in request.form and request.form["text"]:
            text = request.form["text"]
            word_count = count_english_words(text)

        # URL入力がある場合
        if "url" in request.form and request.form["url"]:
            url_input = request.form["url"]
            result = count_words_from_url(url_input)
            url_word_count = result if isinstance(result, int) else result  # 数値 or エラーメッセージ

    return render_template("index.html",
                           text=text,
                           word_count=word_count,
                           url=url_input,
                           url_word_count=url_word_count)

if __name__ == "__main__":
    app.run()
