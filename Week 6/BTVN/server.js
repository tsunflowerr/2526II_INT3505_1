const express = require("express");
const jwt = require("jsonwebtoken");

const app = express();
app.use(express.json());

const SECRET = "secret-key";
const users = [
  { id: 1, username: "admin", password: "123456", role: "admin" },
  { id: 2, username: "bob", password: "123456", role: "user" }
];
const tokens = new Set();

function genAccessToken(user) {
  return jwt.sign({ userId: user.id, username: user.username, role: user.role }, SECRET, { expiresIn: "15m" });
}

function genRefreshToken(user) {
  return jwt.sign({ userId: user.id }, SECRET, { expiresIn: "7d" });
}

function verify(req, res, next) {
  const auth = req.headers.authorization;
  if (!auth || !auth.startsWith("Bearer ")) return res.status(401).json({ error: "Unauthorized" });
  try {
    req.user = jwt.verify(auth.split(" ")[1], SECRET);
    next();
  } catch (e) {
    res.status(401).json({ error: "Token invalid" });
  }
}

app.get("/", (req, res) => {
  res.json({ endpoints: ["POST /login", "GET /profile", "GET /admin", "POST /refresh", "POST /logout"] });
});

app.post("/login", (req, res) => {
  const { username, password } = req.body;
  const user = users.find((u) => u.username === username && u.password === password);
  if (!user) return res.status(401).json({ error: "Invalid credentials" });
  
  const accessToken = genAccessToken(user);
  const refreshToken = genRefreshToken(user);
  tokens.add(refreshToken);
  res.json({ accessToken, refreshToken });
});

app.get("/profile", verify, (req, res) => {
  res.json({ user: req.user });
});

app.get("/admin", verify, (req, res) => {
  if (req.user.role !== "admin") return res.status(403).json({ error: "Forbidden" });
  res.json({ message: "Admin only data" });
});

app.post("/refresh", (req, res) => {
  const { refreshToken } = req.body;
  if (!tokens.has(refreshToken)) return res.status(401).json({ error: "Invalid token" });
  
  try {
    const decoded = jwt.verify(refreshToken, SECRET);
    const user = users.find((u) => u.id === decoded.userId);
    res.json({ accessToken: genAccessToken(user) });
  } catch (e) {
    res.status(401).json({ error: "Token expired" });
  }
});

app.post("/logout", (req, res) => {
  tokens.delete(req.body.refreshToken);
  res.json({ message: "Logged out" });
});

app.listen(3000, () => console.log("JWT server: http://localhost:3000"));
