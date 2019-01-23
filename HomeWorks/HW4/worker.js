const { Client, Variables, logger } = require('camunda-external-task-client-js');

// configuration for the Client:
//  - 'baseUrl': url to the Process Engine
//  - 'logger': utility to automatically log important events
const config = { baseUrl: 'http://localhost:8080/engine-rest', use: logger, maxTasks:1};

// create a Client instance with custom configuration
const client = new Client(config);

const FISH_PROB = 0.4;
const RICE_PROB = 0.6;
const AVAILABLE = "available";
const NON_AVAILABLE = "non_available";

const FISH_COST = 5;
const RICE_COST = 3;
const SALAD_COST = 2;

// susbscribe to the topic: 'FightTribe'
client.subscribe('MenuTask', async function(params) {
    task = params['task']
    callback = params['taskService']

    // Business Logic
    const processVariables = new Variables();

    // FISH
    var fish_status = NON_AVAILABLE;
    if(Math.random() <= FISH_PROB) {
        console.log("Fish available")
        fish_status = AVAILABLE
    } else {
        console.log("Fish not available")
    }
    processVariables.set("fish", fish_status)

    // RICE
    var rice_status = NON_AVAILABLE;
    if(Math.random() <= RICE_PROB) {
        console.log("Rice available")
        rice_status = AVAILABLE
    } else {
        console.log("Rice not available")
    }
    processVariables.set("rice", rice_status)

    // SALAD
    // var salad_status = NON_AVAILABLE;
    if(fish_status == NON_AVAILABLE && rice_status == NON_AVAILABLE) {
        console.log("Salad available")
        // salad_status = AVAILABLE
    } else {
        console.log("Salad not available")
    }
    // processVariables.set("salad", salad_status)

    // Callback - Complete
    await callback.complete(task, processVariables, null);
  
});

// susbscribe to the topic: 'FightTribe'
client.subscribe('BillTask', async function(params) {
    task = params['task']
    callback = params['taskService']
    
    // Business Logic
    const processVariables = new Variables();

    var fishTaken = task.variables.get('fishTaken') || 0;
    var riceTaken = task.variables.get('riceTaken') || 0;
    var saladTaken = task.variables.get('saladTaken') || 0;
    var total = fishTaken * FISH_COST + riceTaken * RICE_COST + saladTaken * SALAD_COST;

    processVariables.set("fishTaken", fishTaken);
    processVariables.set("riceTaken", riceTaken);
    processVariables.set("saladTaken", saladTaken);
    processVariables.set("total", total);

    // Callback - Complete
    await callback.complete(task, processVariables, null);
  
});