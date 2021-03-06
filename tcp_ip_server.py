# import socket
import socketserver

from xmlcommands.interface import execute_command


class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        return_message = execute_command(self.data)
        self.request.sendall(return_message)


if __name__ == "__main__":
    # HOST, PORT = socket.gethostname(), 9999
    HOST, PORT = 'localhost', 9999
    # Create the server, binding to localhost on port 9999

    print("Starting socket server")
    print("HOST: {}".format(HOST))
    print("PORT: {}".format(PORT))
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
