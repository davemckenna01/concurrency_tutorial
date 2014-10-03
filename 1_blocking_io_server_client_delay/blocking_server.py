"""
This server uses a blocking socket to interact with clients.
recv() will block the thread while reading data from kernel space.
send() will block as well when writing data to kernel space.

recv(num bytes) where num_bytes is the amt of data requested from the kernel.
If there's < num_bytes available, it'll return with whatever's available.
"""


import socket

EOL1 = b'\n\n'
EOL2 = b'\n\r\n'
response = b'Got it, thanks.'

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind(('0.0.0.0', 8080))
serversocket.listen(1)

reqs_handled = 0

try:
    while True:
        connectiontoclient, address = serversocket.accept()
        print "accepted a connection"
        # socket "connectiontoclient" is blocking (the default socket behaviour)
        print "about to block thread while waiting for recv()"

        chunk = connectiontoclient.recv(20)
        print "got some data of len: %d" % len(chunk)

        connectiontoclient.send(response)
        connectiontoclient.close()

        reqs_handled += 1
        print "                 requests handled: %d" % reqs_handled
finally:
    serversocket.close()