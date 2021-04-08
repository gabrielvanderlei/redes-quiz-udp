import socket

 
localIP     = "127.0.0.1"
localPort   = 20001
bufferSize  = 1024

listOfClientsConnected = []
maxNumberOfClients = 5

 
# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

 
# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

print("UDP server up and listening")


# Listen for incoming datagrams
while(True):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]

    # clientMsg = "Message from Client: {}".format(message)
    # clientIP  = "Client IP Address: {}".format(address)
    if len(listOfClientsConnected) < maxNumberOfClients:
        if message == 'register':
            if not (address in listOfClientsConnected):
                listOfClientsConnected.append(address)
                msgFromServer = "Client successfully registred!"
            else:
                msgFromServer = "Client already registred!"
    else:
        msgFromServer = "The Database is currently full!"
    # print(clientMsg)
    # print(clientIP)

    # Sending a reply to client
    bytesToSend         = str.encode(msgFromServer)
    UDPServerSocket.sendto(bytesToSend, address)