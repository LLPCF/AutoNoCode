const express = require('express');
const app = express();
const port = 80; // Porta 80 dentro do contêiner

app.get('/', (req, res) => {
  res.send('Hello from Service 2!');
});

app.listen(port, () => {
  console.log(`Service 2 running at http://localhost:${port}`);
});
