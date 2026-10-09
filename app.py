import os
import requests
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
def send_to_telegram(text):
    if not BOT_TOKEN or not CHAT_ID:
        return False
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}
        r = requests.post(url, data=data, timeout=10)
        return r.status_code == 200
    except:
        return False
@app.route("/")
def index():
    return render_template("index.html")
@app.route("/order", methods=["POST"])
def order():
    d = request.get_json()
    msg = f"🛒 <b>ФАРМОИШИ НАВ - Алмаз Shop!</b>\n\n📦 {d.get('product')}\n👤 {d.get('name')}\n📞 {d.get('phone')}\n📍 {d.get('address')}"
    ok = send_to_telegram(msg)
    if ok:
        return jsonify({"status":"ok"})
    else:
        return jsonify({"status":"error"}), 500
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
