"""
This server users asynchronous sockets to accept connections and read from
and write to sockets. This is non-blocking I/O, because the main process does
not wait for a read or write to finish before performing other tasks, such as
reading and writing to other sockets.

NOTE: epoll is Linux only. So this won't run on Mac.
"""

import socket, select
EOL1 = b'\n\n'
EOL2 = b'\n\r\n'
response  = b'HTTP/1.0 200 OK\r\nDate: Mon, 1 Jan 1996 01:01:01 GMT\r\n'
response += b'Content-Type: text/plain\r\nContent-Length: 13\r\n\r\n'
response += b'Hello, world!'
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind(('0.0.0.0', 8080))
serversocket.listen(1)
serversocket.setblocking(0)

epoll = select.epoll()
epoll.register(serversocket.fileno(), select.EPOLLIN)

try:
    connections = {}; requests = {}; responses = {}

    print "select.EPOLLIN", select.EPOLLIN
    print "select.EPOLLOUT", select.EPOLLOUT
    print "select.EPOLLHUP", select.EPOLLHUP

    while True:
        events = epoll.poll(1)
        print "---------"
        print "events", events
        for fileno, event in events:
            print "    fileno", fileno
            print "    event", event
            print "    serversocket.fileno()", serversocket.fileno()
            if fileno == serversocket.fileno():
                print "this is an event on the listener socket"

                print "getting communication socket info (fileno, etc)"
                connection, address = serversocket.accept()
                connection.setblocking(0)

                print "register for read readiness alerts on fileno", connection.fileno()
                epoll.register(connection.fileno(), select.EPOLLIN)

                connections[connection.fileno()] = connection

                requests[connection.fileno()] = b''
            elif event & select.EPOLLIN:
                print "fileno", fileno, "has stuff to read"

                print "reading 1024 bytes this round"
                # read 1024 chunks at a time
                requests[fileno] += connections[fileno].recv(1024)

                if EOL1 in requests[fileno] or EOL2 in requests[fileno]:
                    print "finished reading all of request from", fileno, ":"
                    print('-'*40 + '\n' + requests[fileno].decode()[:-2])

                    print "preparing response"
                    responses[fileno] = response # what if a DB call? can we
                                                 # make that async too?

                    print "response ready to send"

                    print "register for write readiness alerts on fileno", fileno
                    epoll.modify(fileno, select.EPOLLOUT)
            elif event & select.EPOLLOUT:
                print "fileno", fileno, "can be written to now"

                print "we have", len(responses[fileno]), "bytes to write"

                print "so we're gonna do it" 
                byteswritten = connections[fileno].send(responses[fileno])

                print "we wrote", byteswritten, "to", fileno

                responses[fileno] = responses[fileno][byteswritten:]

                if len(responses[fileno]) == 0:
                    print "finished writing to", fileno

                    print "unregister for alerts on fileno", fileno
                    epoll.modify(fileno, 0)

                    print "shut down connection to fileno", fileno
                    connections[fileno].shutdown(socket.SHUT_RDWR)
            elif event & select.EPOLLHUP:
                print "unregister for alerts on fileno (AGAIN?!)", fileno
                epoll.unregister(fileno)

                print "close connection to fileno", fileno
                connections[fileno].close()
                del connections[fileno]
finally:
    epoll.unregister(serversocket.fileno())
    epoll.close()
    serversocket.close()