import threading
import socket

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    
def readServerDataCycle():
    while True:
        bufferSize = 1024
        msgFromServer = UDPClientSocket.recvfrom(bufferSize)
        msg = "> {0}".format(msgFromServer[0].decode("utf-8"))
        print(msg)
        
def waitingCommandCycle():
    print("Send messages writing below and pressing enter.")
    print("Send 'register' to enter in a server room.")
    print("A room only support 5 clients.")
    
    while True:
        msgFromClient = input("")
        bytesToSend = str.encode(msgFromClient)
        serverAddressPort = ("127.0.0.1", 20001)
        UDPClientSocket.sendto(bytesToSend, serverAddressPort)


readServerThread = threading.Thread(target=readServerDataCycle, args=[])
readServerThread.start()

waitingCommandThread = threading.Thread(target=waitingCommandCycle, args=[])
waitingCommandThread.start()