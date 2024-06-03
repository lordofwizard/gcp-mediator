# This is a RigBetel Labs LLP Product.
# This Script is a Mediator server which allows you 
# Send / transmit the data over the internet to your 
# client devices. Uses OpenCV and imutils with udp
# Tunnels to achieve this.
# 
# Author - lordofwizard 
# Aka - Advait Pandharpurkar

import cv2, imutils, socket
import numpy as np
import time
import base64
import time
import threading

# Fixed Maximum Buffer Size
BUFF_SIZE = 65536
SOCKET_TIMEOUT_SEC = 10
SOCKET_CHECK_ITERATION = 30

# All client object array
CONNECTIONS = []

# Sender global bool
sender_available = False

mediator_hostname = socket.gethostname()
mediator_ip_tuple = socket.gethostbyname(mediator_hostname)
mediator_ip = mediator_ip_tuple[0]

# Sender Socket Initialization
sender_port = 6969
sender_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sender_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
sender_socket_address = (mediator_ip_tuple,sender_port)
sender_socket.bind(sender_socket_address)
sender_socket.settimeout(SOCKET_TIMEOUT_SEC)
sender_credentails = ("",0)


# Client Global Object
class Client:
    ip = ""
    port = ""
    ack_time = "" # LAST ACK TIME

    def __init__(self):
        self.ip = ""
        self.port = ""
        self.ack_time = ""
        print("Client Initialized")

def sender_thread_func(robot_name : str):
    """
    This Function is used as thread function, which
    will check iteration after iteration, if we are getting
    the Video feed or not. 
    """
    global sender_credentails
    global sender_socket
    global sender_available

    print(f"Starting a process for {robot_name}")
    while True:
        try:
            msg,sender_credentails = sender_socket.recvfrom(BUFF_SIZE)
            print('Recieved Video Stream Connection from',sender_credentails,"for",robot_name)
            sender_available = True
        except socket.timeout:
            sender_available = False
            pass
        except Exception as e:
            sender_available = False
            print("Error : Stream Recieve Error",e)
        time.sleep(SOCKET_CHECK_ITERATION)

reciever_port = 9696
reciever_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
reciever_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, BUFF_SIZE)
reciever_socket_address = (mediator_ip_tuple,reciever_port)
#reciever_socket.bind(reciever_socket_address)
reciever_socket.settimeout(SOCKET_TIMEOUT_SEC)

def request_thread(robot_name : str):
    global reciever_socket, reciever_port
    global mediator_ip_tuple
    global CONNECTIONS

    reciever_socket.bind((mediator_ip_tuple,reciever_port))

    while True:
        data, addr = reciever_socket.recvfrom(BUFF_SIZE)
        print("Received message:", data.decode(), "from", addr)
        current_time = int(time.time())
        new_client = Client(ip=addr[0], port=addr[1], ack_time=current_time)
        CONNECTIONS.append(new_client) 
        time.sleep(1)


def reciever_thread_func(robot_name : str):
    global reciever_socket
    global sender_available
    global sender_socket
    global reciever_port
    global reciever_socket_address
    print(reciever_socket_address, "reciever socket address")
    """
    This Function is used as thread function, which
    will check iteration after iteration, if we are sending
    the Video feed or not. 
    """
    while True:
        if sender_available == True:
            frame,(sender_ip_at_recv,sender_port_at_recv) = sender_socket.recvfrom(BUFF_SIZE)
            #reciever_socket.sendto(frame,reciever_socket_address)
            for item in CONNECTIONS:
                reciever_socket.sendto(frame,(item.ip,item.port))
            print("frame sent")
        else:
            time.sleep(1)

sender = threading.Thread(target=sender_thread_func, args=["TortoiseBot"])
sender.start()

reciever = threading.Thread(target=reciever_thread_func, args=["TortoiseBot"])
reciever.start()

request = threading.Thread(target=request_thread, args=["TortoiseBot"])
request.start()