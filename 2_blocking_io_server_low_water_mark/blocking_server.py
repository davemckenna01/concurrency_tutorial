"""
This server uses a blocking socket to interact with clients.
recv() will block the thread while reading data from kernel space. We'll set
SO_RCVLOWAT to check out how it continues to block until it's read x amount
of data.

send() will block as well when writing data to kernel space.

from man setsockopt:

SO_RCVLOWAT is an option to set the minimum count for input operations.
In general, receive calls will block until any (non-zero) amount of data
is received, then return with the smaller of the amount available or the
amount requested.  The default value for SO_RCVLOWAT is 1.  If
SO_RCVLOWAT is set to a larger value, blocking receive calls normally
wait until they have received the smaller of the low-water mark value or
the requested amount.  Receive calls may still return less than the low-
water mark if an error occurs, a signal is caught, or the type of data
next in the receive queue is different than that returned.

The accompanying client script sends 20 bytes to this server, 10 at a time,
delayed by 3 secs.

Once the kernel has accumulated > SO_RCVLOWAT bytes for this socket,
recv() will return what's there, to a maximum of what was requested
in recv's first arg.

Note: OSX seemed to ignore SO_RCVLOWAT, but it worked in Linux.

A similar effect can be achieved by using MSG_WAITALL:

    connectiontoclient.recv(20, socket.MSG_WAITALL)

This forces recv to wait till 20 bytes are available before returning.

"""

import socket

EOL1 = b'\n\n'
EOL2 = b'\n\r\n'
response = b'Got it, thanks.'

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVLOWAT, 19)
serversocket.bind(('0.0.0.0', 8080))
serversocket.listen(1)

reqs_handled = 0

try:
    while True:
        connectiontoclient, address = serversocket.accept()
        print "accepted a connection"
        print "low water mark = %d" % serversocket.getsockopt(socket.SOL_SOCKET, socket.SO_RCVLOWAT)
        # socket "connectiontoclient" is blocking (the default socket behaviour)
        print "about to block thread while waiting for recv()"

        chunk = connectiontoclient.recv(21)
        print "got some data of len: %d" % len(chunk)

        connectiontoclient.send(response)
        connectiontoclient.close()

        reqs_handled += 1
        print "                 requests handled: %d" % reqs_handled
finally:
    serversocket.close()