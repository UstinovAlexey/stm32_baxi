
import network
import time

eth=network.LAN()
eth.active(1)
for i in range (5):
    
    print(eth.ifconfig())
    print ("Hello!",i,eth.isconnected())
    
    time.sleep(3)
    
import socket
  
if __name__ == '__main__': 
    # Defining Socket 
    host = '127.0.0.1'
    port = 8080
    totalclient = int(input('Enter number of clients: ')) 
  
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("befor bind")
    sock.bind((host, port))
    print("befor listen")
    sock.listen(totalclient) 
    print("after listen")

# Establishing Connections 
    connections = [] 
    print('Initiating clients') 
    for i in range(totalclient): 
        conn = sock.accept() 
        connections.append(conn) 
        print('Connected with client', i+1) 
  
    fileno = 0
    idx = 0
    for conn in connections: 
        # Receiving File Data 
        idx += 1
        data = conn[0].recv(1024).decode() 
  
        if not data: 
            continue
    # Creating a new file at server end and writing the data 
        filename = 'output'+str(fileno)+'.txt'
        fileno = fileno+1
        fo = open(filename, "w") 
        while data: 
            if not data: 
                break
            else: 
                fo.write(data) 
                data = conn[0].recv(1024).decode() 
  
        print() 
        print('Receiving file from client', idx) 
        print() 
        print('Received successfully! New filename is:', filename) 
        fo.close() 
    # Closing all Connections 
    for conn in connections: 
        conn[0].close() 