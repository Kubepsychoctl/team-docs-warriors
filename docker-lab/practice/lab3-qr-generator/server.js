const express = require("express");
const QRCode = require("qrcode");

const app = express();
const PORT = 3000;

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

const HTML = `
<!DOCTYPE html>
<html>
<head>
  <title>QR Generator</title>
  <style>
    body {
      font-family: Arial;
      text-align: center;
      padding: 50px;
      background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    .container {
      background: white;
      padding: 40px;
      border-radius: 15px;
      max-width: 500px;
      margin: 0 auto;
      box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    input {
      width: 80%;
      padding: 15px;
      font-size: 16px;
      border: 2px solid #f5576c;
      border-radius: 5px;
      margin: 20px 0;
    }
    button {
      padding: 15px 40px;
      font-size: 18px;
      background: #f5576c;
      color: white;
      border: none;
      border-radius: 5px;
      cursor: pointer;
    }
    button:hover { background: #e04758; }
    #qrcode { margin-top: 30px; }
  </style>
</head>
<body>
  <div class="container">
    <h1>📱 QR Code Generator</h1>
    <p>Введите текст для генерации QR-кода</p>
    <form action="/generate" method="POST">
      <input type="text" name="text" placeholder="Введите текст или URL" required>
      <br>
      <button type="submit">Генерировать QR</button>
    </form>
    <div id="qrcode"></div>
  </div>
</body>
</html>
`;

app.get("/", (req, res) => {
  res.send(HTML);
});

app.post("/generate", async (req, res) => {
  const text = req.body.text;
  try {
    const qrCode = await QRCode.toDataURL(text);
    res.send(`
    ${HTML.replace("</div>", `<img src="${qrCode}" style="margin-top:20px;"><br>
      <a href="${qrCode}" download="qrcode.png">
      <button type="button">Скачать QR-код</button></a></div>`)}
    `);
  } catch (err) {
    res.status(500).send("Ошибка генерации QR-кода");
  }
});

app.listen(PORT, () => {
  console.log(`Сервер запущен на http://localhost:${PORT}`);
});
