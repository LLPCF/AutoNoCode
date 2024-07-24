const axios = require('axios');
const fs = require('fs');
const path = require('path');
const config = require('../config');

exports.uploadPhotos = async (req, res) => {
  try {
    const photoPaths = req.files.map(file => ({
      path: path.resolve(file.path),
      duration: 3
    }));

    const response = await axios.post('https://api.json2video.com/create', {
      apiKey: config.apiKey,
      resolution: '1080p',
      fps: 30,
      format: 'mp4',
      photos: photoPaths
    });

    const videoPath = path.join(config.uploadDir, 'video.mp4');
    fs.writeFileSync(videoPath, response.data);

    res.json({ videoPath: `/uploads/video.mp4` });
  } catch (error) {
    console.error('Error creating video:', error);
    res.status(500).json({ error: 'Failed to create video' });
  }
};
