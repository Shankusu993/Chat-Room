import socket
import select
from thread import *
import sys


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
"""
the first argument AF_INET is the address domain of the socket. This is used when we have an Internet Domain
with any two hosts
The second argument is the type of socket. SOCK_STREAM means that data or characters are read in a continuous flow
"""
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
if len(sys.argv) != 2:
    print "Correct usage: script, port number"
    exit()
Port = int(sys.argv[1])
server.bind(('', Port)) 
# binds the server  at the specified port number. The client must be aware of this parameter
server.listen(100)
print "server started and is listening"
# listens for 100 active connections. This number can be increased as per convenience
list_of_clients = []
list_of_questions = ["Question1?", "Question2?", "Question3?", "Question4?", "Question5?", ]

def clientthread(conn, addr):
    ind=0
    conn.send("Server: Welcome to this chatroom!\n")
    print "welcome message sent to ","<" + addr[0] + "> "

    conn.send(("Server: " + list_of_questions[ind]))
    # sends a message to the client whose user object is conn
    while True:
            try:

                if ind != 4:
                    ind+=1
                else:
                    ind=0         
                message = conn.recv(2048)    
                if message:
                    print "<" + addr[0] + "> " + message
                    message_to_send = "<" + addr[0] + "> " + message
                    broadcast(message_to_send + "\n" + ("Server: " + list_of_questions[ind]), conn)
                    #prints the message and address of the user who just sent the message on the server terminal



                else:
                    remove(conn)
            except:
                continue

def broadcast(message,connection):
    for clients in list_of_clients:
        if clients!=connection:
            try:
                clients.send(message)
            except:
                clients.close()
                print clients + " was removed"
                remove(clients)

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

while True:
    conn, addr = server.accept()
    """
    Accepts a connection request and stores two parameters, conn which is a socket object for that user, and addr which contains
    the IP address of the client that just connected
    """
    list_of_clients.append(conn)
    print addr[0] + " connected"
    #maintains a list of clients for ease of broadcasting a message to all available people in the chatroom
    #Prints the address of the person who just connected
    start_new_thread(clientthread,(conn,addr))
    #creates and individual thread for every user that connects

conn.close()
server.close()