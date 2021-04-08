import socket

 
localIP     = "127.0.0.1"
localPort   = 20001
bufferSize  = 1024

commands = ['start', 'register']
quizzStartedFlag = False
listOfClientsConnected = []
maxNumberOfClients = 5

 
# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

 
# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

print("UDP Server is running at port {}".format(localPort))


# Listen for incoming datagrams
while(True):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]

    if not (message in commands):
        msgFromServer = "Enter a correct Command \n"
    
    if (message == 'register' or message == 'start') and (quizzStartedFlag):
        msgFromServer = "There's a Quizz match running right now! \n"

    if (message == 'start') and not (quizzStartedFlag):
        msgFromServer = "Quizz started! \n"
        quizzStartedFlag = True

    if not quizzStartedFlag:
        if (len(listOfClientsConnected) < maxNumberOfClients):
            if message == 'register':
                if not (address in listOfClientsConnected):
                    listOfClientsConnected.append(address)
                    msgFromServer = "Client successfully registred! \n"
                    print('Client {} registred in the Database'.format(address))
                else:
                    msgFromServer = "Client already registred! \n"
        else:
            msgFromServer = "The Database is currently full! \n"


    # Sending a reply to client
    bytesToSend         = str.encode(msgFromServer)
    UDPServerSocket.sendto(bytesToSend, address)