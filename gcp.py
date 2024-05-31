import cv2, imutils, socket
import numpy as np
import time
import base64

BUFF_SIZE = 65536


host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
host_ip = "192.168.0.178"
#host_ip = ("192.168.0.178", "6969")
print(host_ip)

sender_available = False
reciever_available = False
sender_port = 6969
sender_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sender_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
sender_socket_address = (host_ip,sender_port)
sender_socket.bind(sender_socket_address)
sender_socket.settimeout(10)

print('Listening at:',sender_socket_address)
    
    
reciever_port = 9696
reciever_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
reciever_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
reciever_socket_address = (host_ip,reciever_port)
reciever_socket.bind(reciever_socket_address)
reciever_socket.settimeout(10)
    
    
try:
    msg,sender_addr = sender_socket.recvfrom(BUFF_SIZE)
    print('GOT connection from ',sender_addr)
    sender_available = True
    
    msg,reciever_addr = reciever_socket.recvfrom(BUFF_SIZE)
    print('GOT connection from ',reciever_addr)
    reciever_available = True

except socket.timeout:
    print("First initialization failed on it's face, running the loop now")
except Exception as e:
    print("Initialization time failed, running new loop" + " " + e)

while True:
    if sender_available == True and reciever_available == True:
        #print("I got both")
        packet,_ = sender_socket.recvfrom(BUFF_SIZE)
        #print("I recieved the frame")
        reciever_socket.sendto(packet,reciever_socket_address)
        #print("I sent the frame")
    elif sender_available:
        print("Sender available but reciever not available!")
        try:
            msg,reciever_addr = reciever_socket.recvfrom(BUFF_SIZE)
            print('GOT connection from ',reciever_addr)
            reciever_available = True
        except socket.timeout:
            print("Socket for Reciever Timedout")
        except Exception as e:
            print(f"Exception occured as {e}")
    elif reciever_available:
        print("Reciever available but not data recieved.")
        try:
            msg,sender_addr = sender_socket.recvfrom(BUFF_SIZE)
            print('GOT connection from ',sender_addr)
            sender_available = True
        except socket.timeout:
            print("Socket for sender Timedout")
        except Exception as e:
            print(f"Exception occured as {e}")
    else:
        try:
            msg,reciever_addr = reciever_socket.recvfrom(BUFF_SIZE)
            print('GOT connection from ',reciever_addr)
            reciever_available = True
        except socket.timeout:
            print("Socket for Reciever Timedout")
        except Exception as e:
            print(f"Exception occured as {e}")
        try:
            msg,sender_addr = sender_socket.recvfrom(BUFF_SIZE)
            print('GOT connection from ',sender_addr)
            sender_available = True
        except socket.timeout:
            print("Socket for sender Timedout")
        except Exception as e:
            print(f"Exception occured as {e}")
        print("BOTH AINT AVAILABLE")

