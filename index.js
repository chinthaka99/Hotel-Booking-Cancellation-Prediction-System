const express = require('express');
const path = require('path');
const { exec } = require('child_process');
const bodyParser = require('body-parser');

const app = express();

// Set the directory where your static HTML files are located
const staticFilesDirectory = path.join(__dirname, 'public');

// Serve static files from the specified directory
app.use(express.static(staticFilesDirectory));

// Use body-parser middleware
app.use(bodyParser.urlencoded({ extended: true }));
const fs = require('fs');

// Start the server
const port = process.env.PORT || 5000;
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
