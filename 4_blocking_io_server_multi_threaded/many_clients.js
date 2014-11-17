var net = require('net');
 
for (var i = 0; i < 4; i++) {
    sendStuff(new net.Socket(), '1', 10);
}

function sendStuff(client, character, size) {
    client.connect(8080, '127.0.0.1', function() {
        var str = '';

        console.log('Connected...');

        for (var i = 0; i < size; i++) {
            str += character; 
        }

        client.write(str);
    });

    client.on('data', function(data) {
        console.log('Received: ' + data);
        client.destroy(); // kill client after server's response
    });
     
    client.on('close', function() {
        console.log('Connection closed');
    });
}

