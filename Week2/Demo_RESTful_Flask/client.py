import requests

r = requests.get("http://127.0.0.1:5000/health")
print(r.json())
m = requests.get("http://127.0.0.1:5000/users")
print(m.json())
n = requests.get("http://127.0.0.1:5000/users/1")
print(n.json())
o = requests.post("http://127.0.0.1:5000/sum", json={"a": 3, "b": 5})
print(o.json())
p = requests.post("http://127.0.0.1:5000/sum", json={"a": 10, "b": 20})
print(p.json())
