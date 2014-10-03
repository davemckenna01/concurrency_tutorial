"""
Not only can a server block a thread by IO with the kernel, it can block
by looping over an IO call, for eg. to build a request or response and
determine it's start and end.

Below we call recv() repeatedly until our criteria for a complete request
is met. This blocks the thread in 2 ways.


"""

import socket

TERMINATOR = "@"
response = "Got it, thanks."

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
        print "about to block thread while a) looping over recv() and b) waiting for recv()"

        request = "" 

        while TERMINATOR not in request:
            chunk = connectiontoclient.recv(10)
            print "got some data: %s" % chunk
            request += chunk

        print "got a complete request, terminated properly: %s" % request

        connectiontoclient.send(response)
        connectiontoclient.close()

        reqs_handled += 1
        print "                 requests handled: %d" % reqs_handled
finally:
    serversocket.close()