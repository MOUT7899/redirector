from flask import Flask, request, redirect
import base64

app = Flask(name)

@app.route("/")
def cloak():
    encoded_url = request.args.get('u')
    if not encoded_url:
        return "Missing URL", 400
    try:
        url = base64.urlsafe_b64decode(encoded_url.encode()).decode()
        return redirect(url, code=302)
    except:
        return "Invalid URL", 400

if name == "main":
    app.run()
