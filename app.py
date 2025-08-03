from flask import Flask, request, redirect
import base64

app = Flask(__name__)

@app.route('/')
def index():
    encoded_url = request.args.get('u')
    if not encoded_url:
        return 'No URL provided!', 400
    try:
        decoded_url = base64.urlsafe_b64decode(encoded_url.encode()).decode()
        return redirect(decoded_url)
    except Exception as e:
        return f'Error decoding URL: {e}', 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
