// Client gọi server, nhận CODE về và thực thi

async function main() {
  
  const data = await fetch("http://localhost:3000/api/data").then(r => r.json());
  console.log("1. Dữ liệu nhận được:", data);

  const code = await fetch("http://localhost:3000/api/code").then(r => r.text());
  console.log("2. Code nhận được:", code);

  eval(code);
  const result = discount(data.price);
  console.log("3. Giá sau giảm:", result);
}

main();
