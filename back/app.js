console.log('teste')
async function connect(mysql){
  if(global.connection && global.connection.state !== 'disconnected') return global.connection;
  const connection = await mysql.createConnection({
    host: 'database-1.cve8wekscbc9.us-east-2.rds.amazonaws.com',
    user: 'admin',
    password: 'renan123',
    database: 'db_projn',
  });
  console.log("Conectou no MySQL!");
  global.connection = connection;
  return connection;
}
async function main() {
  const mysql = require("mysql2");
  const express = require("express");
  var cors = require('cors');
  console.log('oi');
  const app = express();
  app.use(cors());

  const port = 3000;

  const connection = await connect(mysql);

  app.get('/v1/search/:term', (req, res) => {
    const term = req.params.term;
    console.log(`got it!\n${term}`)
    const queryString = `SELECT * FROM db_projn.noticias WHERE titulo LIKE '%${term}%' ORDER BY data DESC LIMIT 30;`;
    connection.query(queryString, (error, results, fields) => {
        if (error) throw error;
        console.log(results);
        res.json(results);
    });
  });

  app.listen(port, async function () {
    console.log(`Example app listening on port ${port}!`);
    
  });
}

main();
