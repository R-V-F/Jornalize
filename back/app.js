// server.js
const express = require('express');
const mysql = require('mysql2');
const cors = require('cors');

const app = express();
const port = 3000;

app.use(cors());

const connection = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: 'renan123',
  database: 'db_projn',
});

connection.connect();

app.get('/v1/search/:term', (req, res) => {
    const term = req.params.term;
    console.log(`got it!\n${term}`)
    const queryString = `SELECT * FROM db_projn.noticias WHERE titulo LIKE '%${term}%' ORDER BY data DESC;`;
    connection.query(queryString, (error, results, fields) => {
        if (error) throw error;
        console.log(results);
        res.json(results);
    });
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});