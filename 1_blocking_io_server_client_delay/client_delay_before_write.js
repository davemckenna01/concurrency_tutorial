var net = require('net');
 
var client1 = new net.Socket();

sendStuff(client1, '1', 10, 3000);

function sendStuff(client, character, size, delay) {
    client.connect(8080, '127.0.0.1', function() {
        var str = '';

        console.log('Connected... will send soon...');

        for (var i = 0; i < size; i++) {
            str += character; 
        }

        setTimeout(function() {
            client.write(str);
        }, delay)
    });

    client.on('data', function(data) {
        console.log('Received: ' + data);
        client.destroy(); // kill client after server's response
    });
     
    client.on('close', function() {
        console.log('Connection closed');
    });
}

