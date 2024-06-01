
import cv2, imutils, socket
import numpy as np
import time
import base64

BUFF_SIZE = 65536
server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
#host_ip = "192.168.0.178"
print(host_ip)
port = 9999
socket_address = (host_ip,port)
#server_socket.bind(socket_address)
#print('Listening at:',socket_address)
#mediator_address = "192.168.0.178"
#mediator_address = "34.47.151.112"
mediator_address = "34.100.142.237"

mediator = (mediator_address, 6969)
vid = cv2.VideoCapture(2)
fps,st,frames_to_count,cnt = (0,0,20,0)

messageACK = "heyy".encode()
server_socket.sendto(messageACK, mediator) 
print("Message sent btw")


while True:
    WIDTH=1500
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 10]
    while(vid.isOpened()):
        _,frame = vid.read()
        frame = imutils.resize(frame,width=WIDTH)
        encoded,buffer = cv2.imencode('.jpeg',frame,encode_param)
        message = base64.b64encode(buffer)
        print(len(message))
        server_socket.sendto(message,mediator)
        frame = cv2.putText(frame,'FPS: '+str(fps),(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
        #cv2.imshow('TRANSMITTING VIDEO',frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            server_socket.close()
            break
        if cnt == frames_to_count:
            try:
                fps = round(frames_to_count/(time.time()-st))
                st=time.time()
                cnt=0
            except:
                pass
        cnt+=1


