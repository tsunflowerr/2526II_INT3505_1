const express = require("express");
const swaggerJsdoc = require("swagger-jsdoc");
const swaggerUi = require("swagger-ui-express");

const app = express();
app.use(express.json());

// ============================================================
// Swagger Configuration
// ============================================================
const swaggerOptions = {
  definition: {
    openapi: "3.0.0",
    info: {
      title: "HTTP Methods & Status Codes Demo",
      version: "1.0.0",
      description:
        "Ví dụ đơn giản về các HTTP Methods (GET, POST, PUT, PATCH, DELETE) và các Status Codes phổ biến.",
    },
    servers: [{ url: "http://localhost:3000" }],
  },
  apis: [__filename],
};
const swaggerSpec = swaggerJsdoc(swaggerOptions);
app.use("/api-docs", swaggerUi.serve, swaggerUi.setup(swaggerSpec));

// ============================================================
// In-memory data store
// ============================================================
let items = [
  { id: 1, name: "Item A" },
  { id: 2, name: "Item B" },
  { id: 3, name: "Item C" },
];
let nextId = 4;

// ============================================================
// === HTTP METHODS ===
// ============================================================

/**
 * @swagger
 * components:
 *   schemas:
 *     Item:
 *       type: object
 *       properties:
 *         id:
 *           type: integer
 *         name:
 *           type: string
 */

// ---------- GET ----------
/**
 * @swagger
 * /items:
 *   get:
 *     tags: [HTTP Methods]
 *     summary: "GET – Lấy danh sách items"
 *     responses:
 *       200:
 *         description: Trả về danh sách items
 */
app.get("/items", (req, res) => {
  res.status(200).json(items);
});

/**
 * @swagger
 * /items/{id}:
 *   get:
 *     tags: [HTTP Methods]
 *     summary: "GET – Lấy 1 item theo id"
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: integer
 *     responses:
 *       200:
 *         description: Trả về item
 *       404:
 *         description: Không tìm thấy item
 */
app.get("/items/:id", (req, res) => {
  const item = items.find((i) => i.id === parseInt(req.params.id));
  if (!item) return res.status(404).json({ error: "Item not found" });
  res.status(200).json(item);
});

// ---------- POST ----------
/**
 * @swagger
 * /items:
 *   post:
 *     tags: [HTTP Methods]
 *     summary: "POST – Tạo item mới"
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               name:
 *                 type: string
 *                 example: "New Item"
 *     responses:
 *       201:
 *         description: Tạo thành công
 */
app.post("/items", (req, res) => {
  const item = { id: nextId++, name: req.body.name || "Unnamed" };
  items.push(item);
  res.status(201).json(item);
});

// ---------- PUT ----------
/**
 * @swagger
 * /items/{id}:
 *   put:
 *     tags: [HTTP Methods]
 *     summary: "PUT – Thay thế toàn bộ item"
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: integer
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               name:
 *                 type: string
 *                 example: "Replaced Item"
 *     responses:
 *       200:
 *         description: Cập nhật thành công
 *       404:
 *         description: Không tìm thấy
 */
app.put("/items/:id", (req, res) => {
  const idx = items.findIndex((i) => i.id === parseInt(req.params.id));
  if (idx === -1) return res.status(404).json({ error: "Item not found" });
  items[idx] = { id: items[idx].id, name: req.body.name || "Unnamed" };
  res.status(200).json(items[idx]);
});

// ---------- PATCH ----------
/**
 * @swagger
 * /items/{id}:
 *   patch:
 *     tags: [HTTP Methods]
 *     summary: "PATCH – Cập nhật 1 phần item"
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: integer
 *     requestBody:
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               name:
 *                 type: string
 *                 example: "Patched Name"
 *     responses:
 *       200:
 *         description: Cập nhật thành công
 *       404:
 *         description: Không tìm thấy
 */
app.patch("/items/:id", (req, res) => {
  const item = items.find((i) => i.id === parseInt(req.params.id));
  if (!item) return res.status(404).json({ error: "Item not found" });
  if (req.body.name) item.name = req.body.name;
  res.status(200).json(item);
});

// ---------- DELETE ----------
/**
 * @swagger
 * /items/{id}:
 *   delete:
 *     tags: [HTTP Methods]
 *     summary: "DELETE – Xoá item"
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: integer
 *     responses:
 *       204:
 *         description: Xoá thành công (No Content)
 *       404:
 *         description: Không tìm thấy
 */
app.delete("/items/:id", (req, res) => {
  const idx = items.findIndex((i) => i.id === parseInt(req.params.id));
  if (idx === -1) return res.status(404).json({ error: "Item not found" });
  items.splice(idx, 1);
  res.status(204).send();
});

// ============================================================
// === STATUS CODES DEMO ===
// ============================================================

// ---------- 1xx Informational ----------

/**
 * @swagger
 * /status/100:
 *   get:
 *     tags: [Status Codes - 1xx Informational]
 *     summary: "100 Continue – Server sẵn sàng nhận body"
 *     description: "Client gửi header Expect: 100-continue, server phản hồi 100 rồi mới nhận body."
 *     responses:
 *       100:
 *         description: Continue
 */
app.get("/status/100", (req, res) => {
  // Trình duyệt thường không hiển thị 100, nên trả JSON mô tả
  res.status(200).json({
    status: 100,
    name: "Continue",
    description:
      "Server đã nhận request header và client nên tiếp tục gửi body. Thường dùng với header Expect: 100-continue.",
    example: 'Client gửi POST lớn với header "Expect: 100-continue" → Server trả 100 → Client gửi body.',
  });
});

/**
 * @swagger
 * /status/101:
 *   get:
 *     tags: [Status Codes - 1xx Informational]
 *     summary: "101 Switching Protocols – Chuyển đổi giao thức"
 *     description: "Server đồng ý chuyển sang giao thức khác (VD: WebSocket)."
 *     responses:
 *       101:
 *         description: Switching Protocols
 */
app.get("/status/101", (req, res) => {
  res.status(200).json({
    status: 101,
    name: "Switching Protocols",
    description:
      "Server đồng ý chuyển sang giao thức khác theo yêu cầu của client.",
    example:
      'Client gửi header "Upgrade: websocket" → Server trả 101 và chuyển sang WebSocket.',
  });
});

/**
 * @swagger
 * /status/102:
 *   get:
 *     tags: [Status Codes - 1xx Informational]
 *     summary: "102 Processing – Đang xử lý (WebDAV)"
 *     description: "Server đã nhận request và đang xử lý, chưa có response."
 *     responses:
 *       102:
 *         description: Processing
 */
app.get("/status/102", (req, res) => {
  res.status(200).json({
    status: 102,
    name: "Processing",
    description:
      "Server đã nhận và đang xử lý request nhưng chưa có response (WebDAV). Tránh client timeout.",
    example: "Client gửi request phức tạp → Server trả 102 để báo đang xử lý → Sau đó trả kết quả thật.",
  });
});

// ---------- 2xx Success ----------

/**
 * @swagger
 * /status/200:
 *   get:
 *     tags: [Status Codes - 2xx Success]
 *     summary: "200 OK – Thành công"
 *     responses:
 *       200:
 *         description: OK
 */
app.get("/status/200", (req, res) => {
  res.status(200).json({
    status: 200,
    name: "OK",
    description: "Request thành công. Đây là status code phổ biến nhất.",
    example: "GET /items → 200 OK + danh sách items",
  });
});

/**
 * @swagger
 * /status/201:
 *   post:
 *     tags: [Status Codes - 2xx Success]
 *     summary: "201 Created – Tạo mới thành công"
 *     responses:
 *       201:
 *         description: Created
 */
app.post("/status/201", (req, res) => {
  res.status(201).json({
    status: 201,
    name: "Created",
    description: "Tạo resource mới thành công.",
    example: "POST /items → 201 Created + item vừa tạo",
    created: { id: 999, name: "Demo Item" },
  });
});

/**
 * @swagger
 * /status/202:
 *   post:
 *     tags: [Status Codes - 2xx Success]
 *     summary: "202 Accepted – Đã nhận, đang xử lý"
 *     responses:
 *       202:
 *         description: Accepted
 */
app.post("/status/202", (req, res) => {
  res.status(202).json({
    status: 202,
    name: "Accepted",
    description:
      "Request đã được nhận nhưng chưa xử lý xong. Dùng cho async tasks.",
    example:
      "POST /reports/generate → 202 Accepted + jobId để kiểm tra tiến độ sau.",
    jobId: "abc-123",
  });
});

/**
 * @swagger
 * /status/204:
 *   delete:
 *     tags: [Status Codes - 2xx Success]
 *     summary: "204 No Content – Thành công, không có body"
 *     responses:
 *       204:
 *         description: No Content
 */
app.delete("/status/204", (req, res) => {
  // 204 = thành công nhưng không trả body
  res.status(204).send();
});

// ---------- 3xx Redirection ----------

/**
 * @swagger
 * /status/301:
 *   get:
 *     tags: [Status Codes - 3xx Redirection]
 *     summary: "301 Moved Permanently – Chuyển hướng vĩnh viễn"
 *     responses:
 *       301:
 *         description: Moved Permanently
 */
app.get("/status/301", (req, res) => {
  // Redirect vĩnh viễn đến /items
  res.redirect(301, "/items");
});

/**
 * @swagger
 * /status/302:
 *   get:
 *     tags: [Status Codes - 3xx Redirection]
 *     summary: "302 Found – Chuyển hướng tạm thời"
 *     responses:
 *       302:
 *         description: Found (Temporary Redirect)
 */
app.get("/status/302", (req, res) => {
  // Redirect tạm thời đến /items
  res.redirect(302, "/items");
});

/**
 * @swagger
 * /status/304:
 *   get:
 *     tags: [Status Codes - 3xx Redirection]
 *     summary: "304 Not Modified – Dùng cache"
 *     description: "Resource chưa thay đổi, client nên dùng bản cache."
 *     responses:
 *       304:
 *         description: Not Modified
 */
app.get("/status/304", (req, res) => {
  // Giả lập: nếu client gửi If-None-Match khớp → 304
  const etag = '"v1"';
  res.set("ETag", etag);
  if (req.headers["if-none-match"] === etag) {
    return res.status(304).send();
  }
  res.status(200).json({
    status: 304,
    name: "Not Modified",
    description:
      'Resource chưa thay đổi. Gửi lại request với header If-None-Match: "v1" để nhận 304.',
    hint: 'Thêm header "If-None-Match": "\\"v1\\"" để test.',
  });
});

// ---------- 4xx Client Error ----------

/**
 * @swagger
 * /status/400:
 *   post:
 *     tags: [Status Codes - 4xx Client Error]
 *     summary: "400 Bad Request – Request không hợp lệ"
 *     requestBody:
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               name:
 *                 type: string
 *             example: {}
 *     responses:
 *       400:
 *         description: Bad Request
 */
app.post("/status/400", (req, res) => {
  res.status(400).json({
    status: 400,
    name: "Bad Request",
    description: "Request không đúng format hoặc thiếu dữ liệu bắt buộc.",
    example: 'POST /items với body thiếu field "name" → 400 Bad Request.',
  });
});

/**
 * @swagger
 * /status/401:
 *   get:
 *     tags: [Status Codes - 4xx Client Error]
 *     summary: "401 Unauthorized – Chưa xác thực"
 *     responses:
 *       401:
 *         description: Unauthorized
 */
app.get("/status/401", (req, res) => {
  res.status(401).json({
    status: 401,
    name: "Unauthorized",
    description: "Client chưa xác thực (chưa đăng nhập / thiếu token).",
    example: "GET /admin mà không gửi token → 401 Unauthorized.",
  });
});

/**
 * @swagger
 * /status/403:
 *   get:
 *     tags: [Status Codes - 4xx Client Error]
 *     summary: "403 Forbidden – Không có quyền"
 *     responses:
 *       403:
 *         description: Forbidden
 */
app.get("/status/403", (req, res) => {
  res.status(403).json({
    status: 403,
    name: "Forbidden",
    description:
      "Client đã xác thực nhưng KHÔNG có quyền truy cập resource này.",
    example: "User thường truy cập /admin → 403 Forbidden.",
  });
});

/**
 * @swagger
 * /status/404:
 *   get:
 *     tags: [Status Codes - 4xx Client Error]
 *     summary: "404 Not Found – Không tìm thấy"
 *     responses:
 *       404:
 *         description: Not Found
 */
app.get("/status/404", (req, res) => {
  res.status(404).json({
    status: 404,
    name: "Not Found",
    description: "Resource không tồn tại.",
    example: "GET /items/999 (id không tồn tại) → 404 Not Found.",
  });
});

// ---------- 5xx Server Error ----------

/**
 * @swagger
 * /status/500:
 *   get:
 *     tags: [Status Codes - 5xx Server Error]
 *     summary: "500 Internal Server Error – Lỗi server"
 *     responses:
 *       500:
 *         description: Internal Server Error
 */
app.get("/status/500", (req, res) => {
  res.status(500).json({
    status: 500,
    name: "Internal Server Error",
    description: "Lỗi không xác định phía server.",
    example: "Server gặp exception không bắt được → 500.",
  });
});

/**
 * @swagger
 * /status/501:
 *   get:
 *     tags: [Status Codes - 5xx Server Error]
 *     summary: "501 Not Implemented – Chưa hỗ trợ"
 *     responses:
 *       501:
 *         description: Not Implemented
 */
app.get("/status/501", (req, res) => {
  res.status(501).json({
    status: 501,
    name: "Not Implemented",
    description: "Server chưa hỗ trợ chức năng được yêu cầu.",
    example: "PATCH /items (server chưa code) → 501 Not Implemented.",
  });
});

/**
 * @swagger
 * /status/502:
 *   get:
 *     tags: [Status Codes - 5xx Server Error]
 *     summary: "502 Bad Gateway – Proxy/gateway nhận response lỗi"
 *     responses:
 *       502:
 *         description: Bad Gateway
 */
app.get("/status/502", (req, res) => {
  res.status(502).json({
    status: 502,
    name: "Bad Gateway",
    description:
      "Server đóng vai trò gateway/proxy nhận được response không hợp lệ từ upstream server.",
    example: "Nginx proxy request đến Node server đã crash → 502 Bad Gateway.",
  });
});

// ============================================================
// Start server
// ============================================================
const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
  console.log(`Swagger UI:  http://localhost:${PORT}/api-docs`);
});
