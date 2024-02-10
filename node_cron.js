// Import required modules
const cron = require('node-cron');
const { exec } = require('child_process');

// Define the cron schedule (every 10 minutes)
const schedule = '*/10 * * * *';

// Array of Python script paths
const pythonScripts = [
    'correiobraziliense.py',
    'poder360.py',
    'metropoles.py',
    'gazeta.py',
    'folha.py'
    // Add more paths as needed
  ];
  
  // Loop through each Python script and schedule its execution
  pythonScripts.forEach((pythonScriptPath, index) => {
    const command = `py ${pythonScriptPath}`;
  
    cron.schedule(schedule, () => {
      console.log(`Executing Python script ${pythonScriptPath}...`);
      exec(command, (error, stdout, stderr) => {
        if (error) {
          console.error(`Error executing Python script ${pythonScriptPath}: ${error.message}`);
          return;
        }
        console.log(`Python script ${pythonScriptPath} executed successfully.`);
        console.log('Output:', stdout);
        console.error('Error:', stderr);
      });
    });
  });
  
  console.log('node_cron.js script is running...');