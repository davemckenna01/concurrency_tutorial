var net = require('net');
 
var client1 = new net.Socket();

sendStuff(client1, '1', 20, 0);

function sendStuff(client, character, size, delay) {
    client.connect(8080, '127.0.0.1', function() {
        var str = '';
        var term = '@';

        console.log('Connected... ');

        for (var i = 0; i < size; i++) {
            str += character; 
        }

        client.write(str);

        console.log('sent', str);

        setTimeout(function() {
            var part_2 = str + term;
            client.write(part_2);

            console.log('sent', part_2);
        }, 3000);
    });

    client.on('data', function(data) {
        console.log('Received: ' + data);
        client.destroy(); // kill client after server's response
    });
     
    client.on('close', function() {
        console.log('Connection closed');
    });
}

