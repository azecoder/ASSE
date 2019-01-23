const { Client, Variables, logger } = require('camunda-external-task-client-js');

// configuration for the Client:
//  - 'baseUrl': url to the Process Engine
//  - 'logger': utility to automatically log important events
const config = { baseUrl: 'http://localhost:8080/engine-rest', use: logger, maxTasks:1};

// create a Client instance with custom configuration
const client = new Client(config);

// susbscribe to the topic: 'FightTribe'
client.subscribe('FightTribe', async function(params) {
  task = params['task']
  callback = params['taskService']
  
  // Business Logic
  const processVariables = new Variables();

  if(Math.random() > 0.9) {
  	console.log("AAA")
  	processVariables.set("legionStatus", "defeated")
  } else {
  	console.log("BBB")
  	processVariables.set("legionStatus", "vittorious")
  }
  
  // Callback - Complete
  await callback.complete(task, processVariables, null);
  
});
