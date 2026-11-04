from flask import Flask
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    html = """
    <html>
    <body style="font-family: Arial; text-align: center; padding: 50px;">
        <h1 style="color: #0E4C92;">🐳 Привет из Docker!</h1>
        <p style="font-size: 20px;">
            <strong>Меня зовут:</strong> Kubepsychoctl
        </p>
        <p style="color: gray;">
            Время на сервере: {}
        </p>
        <hr>
        <p style="font-size: 14px;">
            Этот сервер работает в Docker контейнере ✅
        </p>
    </body>
    </html>
    """
    return html.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
