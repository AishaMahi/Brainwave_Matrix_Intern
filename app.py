from flask import Flask, render_template, request

app = Flask(__name__)

# Function to extract URL features
def extract_url_features(url):
    from urllib.parse import urlparse
    import re
    try:
        parsed_url = urlparse(url)
        features = {
            "length": len(url),
            "special_chars": len(re.findall(r"[!@#$%^&*()_+=<>?;]", url)),
            "subdomain_count": len(parsed_url.netloc.split('.')) - 2,
            "has_at_symbol": "@" in url,
            "suspicious_words": check_suspicious_words(url),
        }
        return features
    except Exception as e:
        return None

# Function to check for suspicious words in the URL
def check_suspicious_words(url):
    suspicious_words = [
        "update", "login", "secure", "verify", "account", "password", 
        "banking", "free", "gift", "offer", "win", "claim", "urgent"
    ]
    return any(word in url.lower() for word in suspicious_words)

# Function to determine if a URL is suspicious
def is_suspicious(url):
    features = extract_url_features(url)
    if not features:
        return None
    
    # Simple heuristic logic
    if (
        features['length'] > 75 or 
        features['special_chars'] > 5 or 
        features['has_at_symbol'] or 
        features['suspicious_words']
    ):
        return True
    return False

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", result=None)

@app.route("/check", methods=["POST"])
def check():
    url = request.form.get("url")
    if not url:
        return render_template("index.html", result=None, message="Invalid URL.")
    
    result = is_suspicious(url)
    if result is None:
        message = "Invalid URL format."
    elif result:
        message = "The URL is potentially suspicious or phishing."
    else:
        message = "The URL seems legitimate."
    
    return render_template("index.html", result=result, message=message)

if __name__ == "__main__":
    app.run(debug=True)
