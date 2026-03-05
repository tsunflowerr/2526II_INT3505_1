const express = require("express");
const app = express();

app.get("/api/data", (req, res) => {
  res.json({ name: "Laptop", price: 15000000 });
});

app.get("/api/code", (req, res) => {
  res.type("application/javascript");
  res.send(`function discount(price) { return price * 0.8; }`);
});

app.listen(3000, () => console.log("Server: http://localhost:3000"));
