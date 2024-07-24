const express = require("express");
const bodyParser = require("body-parser");
const fs = require("fs");
const path = require("path");

const app = express();
const port = 3000;

// Middleware to parse JSON payloads
app.use(bodyParser.json());

// Define the webhook endpoint
app.post("/webhook", (req, res) => {
  // Retrieve video metadata and download URL from the request body
  const { width, height, duration, size, url, project, id } = req.body;

  // Define the path to save the video
  const videoDirectory = path.join(__dirname, "../arquivos");
  const videoPath = path.join(videoDirectory, `${id}.mp4`);

  // Ensure the directory exists
  if (!fs.existsSync(videoDirectory)) {
    fs.mkdirSync(videoDirectory, { recursive: true });
  }

  // Download and save the video
  const https = require("https");
  const file = fs.createWriteStream(videoPath);
  https.get(url, (response) => {
    response.pipe(file);
    file.on("finish", () => {
      file.close(() => {
        console.log("Download complete.");
      });
    });
  }).on("error", (err) => {
    fs.unlink(videoPath);
    console.error("Error downloading video: ", err.message);
  });

  // Send a response
  res.status(200).send("Webhook received successfully!");
});

// Start the server
app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}/webhook`);
});
