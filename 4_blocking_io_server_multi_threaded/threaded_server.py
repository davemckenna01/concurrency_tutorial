"""
This server uses a blocking socket to interact with clients like in example 1,
but will pass handling of the request and response to a thread so that the
main thread is free to immediately accept another connection. accept() is still
blocking, but there is much less blocking now that most of the processing per 
client is in its own thread.
"""

import socket
import thread

EOL1 = b'\n\n'
EOL2 = b'\n\r\n'
response = b'Got it, thanks.'

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind(('0.0.0.0', 8080))
serversocket.listen(1)

reqs_handled = 0

def client_handler(connectiontoclient, address):
    global reqs_handled

    # socket "connectiontoclient" is blocking (the default socket behaviour)
    print "about to block thread while waiting for recv()"

    while True:
        chunk = connectiontoclient.recv(20)
        print "got some data of len: %d" % len(chunk)
        break

    connectiontoclient.send(response)
    connectiontoclient.close()

    reqs_handled += 1
    print "                 requests handled: %d" % reqs_handled


try:
    while True:
        connectiontoclient, address = serversocket.accept()
        print "accepted a connection from"
        print address
        print "moving it to a new thread"
        thread.start_new_thread(client_handler, (connectiontoclient, address))
finally:
    serversocket.close()