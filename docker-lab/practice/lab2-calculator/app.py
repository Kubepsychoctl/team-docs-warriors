from flask import Flask, render_template_string, request

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>🧮 Калькулятор</title>
  <style>
    body {
      font-family: Arial;
      text-align: center;
      padding: 50px;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .calculator {
      background: white;
      padding: 40px;
      border-radius: 15px;
      max-width: 400px;
      margin: 0 auto;
      box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    input {
      width: 80px;
      padding: 10px;
      font-size: 20px;
      margin: 10px;
      border: 2px solid #667eea;
      border-radius: 5px;
    }
    button {
      padding: 10px 20px;
      font-size: 18px;
      margin: 5px;
      background: #667eea;
      color: white;
      border: none;
      border-radius: 5px;
      cursor: pointer;
    }
    button:hover { background: #5568d3; }
    .result {
      font-size: 32px;
      color: #667eea;
      margin-top: 20px;
      font-weight: bold;
    }
  </style>
</head>
<body>
  <div class="calculator">
    <h1>🧮 Калькулятор</h1>
    <form method="POST">
      <input type="number" name="num1" step="any" placeholder="0" required>
      <select name="operation" style="padding:10px; font-size:18px;">
        <option value="add">+</option>
        <option value="subtract">-</option>
        <option value="multiply">×</option>
        <option value="divide">÷</option>
      </select>
      <input type="number" name="num2" step="any" placeholder="0" required>
      <br>
      <button type="submit">Вычислить</button>
    </form>
    {% if result is not none %}
      <div class="result">Результат: {{ result }}</div>
    {% endif %}
  </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def calculator():
    result = None
    if request.method == "POST":
        num1 = float(request.form["num1"])
        num2 = float(request.form["num2"])
        operation = request.form["operation"]

        if operation == "add":
            result = num1 + num2
        elif operation == "subtract":
            result = num1 - num2
        elif operation == "multiply":
            result = num1 * num2
        elif operation == "divide":
            result = num1 / num2 if num2 != 0 else "Ошибка: деление на 0"

    return render_template_string(HTML, result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
