const fs = require('fs');
const jsonFilePath = './FetchDataBMKG/output.json';

function getCurrentDateInYYYYMMDD() {
    const today = new Date();
    const year = today.getFullYear().toString();
    const month = (today.getMonth() + 1).toString().padStart(2, '0'); // Month is zero-based, so add 1
    const day = today.getDate().toString().padStart(2, '0');
    const hours = today.getHours().toString().padStart(2, '0');
    const minutes = today.getMinutes().toString().padStart(2, '0');
    return year + month + day + hours + minutes;
}
  
const formattedDate = getCurrentDateInYYYYMMDD();


//MQTT
var mqtt = require('mqtt'); //https://www.npmjs.com/package/mqtt
var Topic = 'hafidzganteng'; //subscribe to all topics pakai '#'
var Broker_URL = 'mqtt://broker.mqtt-dashboard.com';
var options = {
    clientId: 'MyMQTT',
    port: 1883,
   //  username: 'hafidz',
   //  password: '123456', 
    keepalive : 60
};

var client  = mqtt.connect(Broker_URL, options);
client.on('connect', mqtt_connect);
client.on('reconnect', mqtt_reconnect);
client.on('error', mqtt_error);
client.on('message', mqtt_messsageReceived);
client.on('close', mqtt_close);

  
// Read the JSON file


function mqtt_connect() {
    //console.log("Connecting MQTT");
    client.subscribe(Topic, mqtt_subscribe);
};


function mqtt_subscribe(err, granted) {
    console.log("Subscribed to " + Topic);
    if (err) {console.log(err);}
    if(!err){
        fs.readFile(jsonFilePath, 'utf8', (err, data) => {
            if (err) {
              console.error('Error reading JSON file:', err);
              return;
            }
          
            // Parse the JSON data
            try {
                let i = 0;
                const jsonData = JSON.parse(data);
                while(parseInt(formattedDate, 10) > parseInt(jsonData.timerange[i]['$'].datetime, 10)){
                    i++;
                }
                console.log(parseInt(jsonData.timerange[i-1]['$'].datetime, 10));
                client.publish(Topic, jsonData.timerange[i-1].value[0]._)
          
              // You can now work with the JSON data in your code.
            } catch (parseError) {
              console.error('Error parsing JSON:', parseError);
            }
          });
    }
};

function mqtt_reconnect(err) {
    //console.log("Reconnect MQTT");
    //if (err) {console.log(err);}
 client  = mqtt.connect(Broker_URL, options);
};

function mqtt_error(err) {
    //console.log("Error!");
 //if (err) {console.log(err);}
};

function after_publish() {
 //do nothing
};

//receive a message from MQTT broker
function mqtt_messsageReceived(topic, message, packet) {
 var message_str = message.toString(); //convert byte array to string
 console.log(message_str);
};

function mqtt_close() {
 //console.log("Close MQTT");
};

