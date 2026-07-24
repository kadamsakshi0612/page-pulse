from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import time

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    report = None
    error = None

    if request.method == "POST":
        url = request.form.get("url", "").strip()

        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://" + url

        try:
            start = time.time()

            response = requests.get(
                url,
                timeout=10,
                headers={
                    "User-Agent": "Mozilla/5.0"
                }
            )

            end = time.time()

            content_type = response.headers.get("Content-Type", "")
            if "text/html" not in content_type:
                error = "The URL does not contain an HTML page."
                return render_template("index.html", report=None, error=error)

            soup = BeautifulSoup(response.text, "html.parser")

            title = soup.title.string.strip() if soup.title and soup.title.string else "Not Found"

            meta = soup.find("meta", attrs={"name": "description"})
            meta_description = (
                meta.get("content").strip()
                if meta and meta.get("content")
                else "Not Found"
            )

            h1_count = len(soup.find_all("h1"))

            images = soup.find_all("img")
            missing_alt = sum(1 for img in images if not img.get("alt"))

            words = len(soup.get_text(separator=" ").split())

            report = {
                "status": response.status_code,
                "response_time": round(end - start, 2),
                "title": title,
                "meta": meta_description,
                "h1": h1_count,
                "missing_alt": missing_alt,
                "word_count": words,
            }

        except requests.exceptions.MissingSchema:
            error = "Please enter a valid URL."

        except requests.exceptions.ConnectionError:
            error = "Could not connect to the website."

        except requests.exceptions.Timeout:
            error = "Request timed out."

        except requests.exceptions.InvalidURL:
            error = "Invalid URL."

        except Exception as e:
            error = f"Error: {e}"

    return render_template("index.html", report=report, error=error)


if __name__ == "__main__":
    app.run(debug=True)