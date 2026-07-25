from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
import time
import os

app = Flask(__name__)


def parse_html(html):
    soup = BeautifulSoup(html, "html.parser")

    title = (
        soup.title.string.strip()
        if soup.title and soup.title.string
        else "Not Found"
    )

    meta = soup.find("meta", attrs={"name": "description"})
    meta_description = (
        meta.get("content").strip()
        if meta and meta.get("content")
        else "Not Found"
    )

    h1_count = len(soup.find_all("h1"))

    images = soup.find_all("img")
    missing_alt = sum(1 for img in images if not img.get("alt"))

    word_count = len(soup.get_text(separator=" ").split())

    return {
        "title": title,
        "meta": meta_description,
        "h1": h1_count,
        "missing_alt": missing_alt,
        "word_count": word_count,
    }


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.get_json(silent=True)

        if data is None:
            return jsonify({"error": "Invalid JSON received."}), 400

        url = data.get("url", "").strip()

        if not url:
            return jsonify({"error": "Please enter a URL."}), 400

        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        start = time.time()

        response = requests.get(
            url,
            timeout=10,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        end = time.time()

        if "text/html" not in response.headers.get("Content-Type", ""):
            return jsonify({"error": "The URL does not contain an HTML page."}), 400

        report = parse_html(response.text)
        report["status"] = response.status_code
        report["response_time"] = round(end - start, 2)

        return jsonify(report), 200

    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Could not connect to the website."}), 400

    except requests.exceptions.Timeout:
        return jsonify({"error": "Request timed out."}), 400

    except requests.exceptions.InvalidURL:
        return jsonify({"error": "Invalid URL."}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5002))
    app.run(host="0.0.0.0", port=port, debug=True)