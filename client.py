
# This is client code to receive video frames over UDP
import cv2, imutils, socket
import numpy as np
import time
import base64
import struct

BUFF_SIZE = 65536

host_ip = "34.100.240.175"

client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)

#host_name = socket.gethostname()
#host_ip= socket.gethostbyname(host_name)

host_ip = "34.100.240.175"

print(host_ip)
port = 9696

client_socket.bind(("",port))
client_socket.sendto("heyyyyyyy".encode(),(host_ip,port))
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536)

client_socket.settimeout(5)
fps,st,frames_to_count,cnt = (0,0,20,0)

while True:
    try:

        packet,(add,pt) = client_socket.recvfrom(BUFF_SIZE)
        #print(f"add={add},pt={pt}")
        #if packet:
            #print("frame recieverd")
        data = base64.b64decode(packet,' /')
        npdata = np.fromstring(data,dtype=np.uint8)
        frame = cv2.imdecode(npdata,1)
        frame = cv2.putText(frame,'FPS: '+str(fps),(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
        cv2.imshow("RECEIVING VIDEO",frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            client_socket.close()
            break
        if cnt == frames_to_count:
            try:
                fps = round(frames_to_count/(time.time()-st))
                st=time.time()
                cnt=0
            except:
                pass
        cnt+=1
    except socket.timeout:
        pass
    except Exception as e:
        print(f"Exception occured. as {e}")


