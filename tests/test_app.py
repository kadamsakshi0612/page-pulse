from app import app, parse_html

def test_parse_html_happy_path():
    html = """
    <html>
    <head>
        <title>My Page</title>
        <meta name="description" content="Test Description">
    </head>
    <body>
        <h1>Hello</h1>
        <img src="image1.jpg" alt="Image">
        <img src="image2.jpg">
        <p>This is testing page</p>
    </body>
    </html>
    """

    result = parse_html(html)

    assert result["title"] == "My Page"
    assert result["meta"] == "Test Description"
    assert result["h1"] == 1
    assert result["missing_alt"] == 1


def test_parse_html_missing_title():
    html = """
    <html>
    <body>
        <h1>Hello</h1>
    </body>
    </html>
    """

    result = parse_html(html)

    assert result["title"] == "Not Found"


def test_parse_html_missing_meta():
    html = """
    <html>
    <head>
        <title>Test</title>
    </head>
    <body>
        Content
    </body>
    </html>
    """

    result = parse_html(html)

    assert result["meta"] == "Not Found"


def test_home():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200