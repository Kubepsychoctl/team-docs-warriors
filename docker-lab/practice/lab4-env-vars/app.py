from flask import Flask, jsonify
from config import Config
import psycopg2

# Валидация env vars при старте
Config.validate()

app = Flask(__name__)
app.config.from_object(Config)

@app.route("/")
def home():
    return jsonify({
        "message": "Config API",
        "environment": Config.APP_ENV,
        "debug": Config.DEBUG,
        "database_host": Config.DB_HOST
        # НЕ показываем секреты!
    })

@app.route("/db-test")
def db_test():
    try:
        conn = psycopg2.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            database=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD
        )
        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()[0]
        cur.close()
        conn.close()
        return jsonify({"status": "success", "database": version})
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=Config.DEBUG)
