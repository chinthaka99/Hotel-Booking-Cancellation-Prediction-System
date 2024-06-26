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

// // Define a new route named "predict" this is the working code
// app.post('/predict', (req, res) => {
//   // Execute the Python script
//   console.log(req.body);
//   exec('python new.py', (error, stdout, stderr) => {
//     if (error) {
//       console.error(`Error executing Python script: ${error}`);
//       return res.status(500).send('Internal Server Error');
//     }
//     if (stderr) {
//       console.error(`Python script stderr: ${stderr}`);
//     }
//     // Send the output of the Python script as the response
//     res.send(stdout);
//   });
// });

const fs = require('fs');



// Start the server
const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
