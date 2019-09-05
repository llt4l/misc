#!/usr/bin/python
import socket
import threading

# Temporary HTTP to HTTPS redirector server

class ThreadedServer(object):
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('', port))

    def listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            client.settimeout(60)
            threading.Thread(target = self.listenToClient,args = (client,address)).start()

    def listenToClient(self, client, address):
        while True:
            try:
                data = client.recv(1024)
                if data:
                    for line in data.split("\n"):
	    		if "Host" in line:
	                    requestedhost = str(line.split(" ")[1])
	                    break
		    print data, requestedhost
                    response = """\
HTTP/1.1 302 Found
Location: https://%s
""" % requestedhost
                    client.send(response)
		    client.close()
                else:
                    raise error('Client disconnected')
            except:
                client.close()
                return False

if __name__ == "__main__":
    port_num = 80
    ThreadedServer('',port_num).listen()
