const express = require('express')
const app = express()

app.use(express.json())

let users = [
    {
        id: 1, name: 'Alice', email: 'alice@example.com'
    },
    {
        id: 2, name: 'Bob', email: 'bob@example.com'
    },
    {
        id: 3, name: 'Charlie', email: 'charlie@example.com'
    }
]
let nextId = 4

//Th1 Lấy danh sách người dùng
app.get('/users', (req, res) => {
    res.json(users)
})

//Th2 Thêm người dùng mới
app.post('/users', (req, res) => {
    const { name, email } = req.body
    if (!name || !email) {
        return res.status(400).json({ error: 'Name and email are required' })
    }
    const newUser = { id: nextId++, name, email }
    users.push(newUser)
    res.status(201).json(newUser)
})

//Th3 : Tìm thông tin theo id
app.get('/users/:id', (req, res) => {
    const userId = parseInt(req.params.id)
    const user = users.find(u => u.id === userId)
    if (!user) {
        return res.status(404).json({ error: 'User not found' })
    }
    res.json(user)
})

//Th4 : Cập nhật thông tin người dùng
app.put('/users/:id', (req, res) => {
    const userId = parseInt(req.params.id)
    const user = users.find(u => u.id === userId)
    if (!user) {
        return res.status(404).json({ error: 'User not found' })
    }
    const { name, email } = req.body
    if (!name || !email) {
        return res.status(400).json({ error: 'Name and email are required' })
    }
    user.name = name
    user.email = email
    res.json(user)
})

//Th5 : Xóa người dùng
app.delete('/users/:id', (req, res) => {
    const userId = parseInt(req.params.id)
    const userIndex = users.findIndex(u => u.id === userId)
    if (userIndex === -1) {
        return res.status(404).json({ error: 'User not found' })
    }  
    users.splice(userIndex, 1)
    res.status(204).send()
})
