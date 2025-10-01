// server.js remains mostly the same, but we'll update to handle DELETE as well.

const express = require('express');
const axios = require('axios');
const app = express();
const PORT = 3000;
const API_URL = process.env.API_URL || 'http://backend:5000';

app.use(express.static('public'));
app.use(express.json());

// Proxy to backend for products
app.get('/products', async (req, res) => {
    try {
        const response = await axios.get(`${API_URL}/products`);
        res.json(response.data);
    } catch (error) {
        res.status(500).json({ error: 'API error' });
    }
});

app.post('/products', async (req, res) => {
    try {
        const response = await axios.post(`${API_URL}/products`, req.body);
        res.json(response.data);
    } catch (error) {
        res.status(500).json({ error: 'API error' });
    }
});

app.delete('/products/:id', async (req, res) => {
    try {
        const response = await axios.delete(`${API_URL}/products/${req.params.id}`);
        res.json(response.data);
    } catch (error) {
        res.status(500).json({ error: 'API error' });
    }
});

app.listen(PORT, () => console.log(`Frontend running on ${PORT}`));
