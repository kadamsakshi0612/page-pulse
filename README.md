# Page Pulse

## Overview
Page Pulse is a web application built using Python Flask that analyzes a website and displays useful information.

## Features
- HTTP Status
- Response Time
- Page Title
- Meta Description
- H1 Count
- Images Missing Alt Text
- Approximate Word Count
- Invalid URL Handling
- JSON API Support
- Timeout Handling
- Non-HTML Page Detection

## Technologies Used
- Python
- Flask
- Requests
- BeautifulSoup4
- HTML
- CSS
- JavaScript

## Installation

pip install -r requirements.txt
python app.py


Open:

http://127.0.0.1:5000

## API Contract

1) Endpoint
  POST /analyze


2) Request Format

  - Content-Type:
    application/json

  - Request body:
    JSON
    {
      "url": "https://example.com"
     }

3) Successful Response
   JSON
{
  "status": 200,
  "response_time": 0.45,
  "title": "Example Domain",
  "meta": "Example description",
  "h1": 1,
  "missing_alt": 0,
  "word_count": 120
}

4) Error Response
  JSON
  {
    "error": "Could not connect to the website."
  }


## Design Decisions

1) Separate HTML Parsing Function :
The HTML parsing logic is kept inside a separate parse_html() function.

Reason:
This makes the code cleaner and allows easy testing of parsing logic without depending on live websites.
 
2) JSON Based API:
The frontend communicates with the Flask backend using JSON requests and responses.

Reason:
It keeps frontend and backend independent and makes the tool easier to extend in the future.

3) Error Handling and Timeout :
The application handles invalid URLs, connection failures, and request timeouts.

Reason:
It improves reliability and prevents crashes when a website is unavailable.

## AI Usage
I used ChatGPT to understand the assignment requirements, get guidance while building the Flask application, improve the user interface, and debug some issues. The final implementation, testing, and verification were completed by me.

