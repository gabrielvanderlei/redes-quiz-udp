import socket

# Create a UDP socket at client side
serverAddressPort = ("127.0.0.1", 20001)
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

IN_LOOP = True

def sendMessage(command, message):
    bytesToSend = str.encode('{0} {1}'.format(command, message))
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)

def receiveMessage():
    bufferSize = 1024
    receivedMessage = UDPClientSocket.recvfrom(bufferSize)

    commandAndData = receiveMessage[0].split(' ')
    command = commandAndData[0]
    data = commandAndData[1:]

    process(command, data)

def process(command, data):
    if(command == 'message'):
        print(data)
    elif(command == 'end'):
        IN_LOOP = False

def waitCommand():
    userCommandAndData = input('Command: ')
    command = userCommandAndData[0]
    data = userCommandAndData[1:]
    sendMessage(command, data)

while(IN_LOOP):
    receiveMessage()
    waitCommand()