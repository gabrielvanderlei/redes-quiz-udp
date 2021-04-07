import socket

localIP             = "127.0.0.1"
localPort           = 20001
bufferSize          = 1024

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))
print("UDP server up and listening")

def sendCommand(clientAddress, command, message):
    UDPServerSocket.sendto(str.encode('{0} {1}'.format(command, message)), clientAddress)

# Listen for incoming datagrams
QUIZ_STATE = 'QUIZ_STATE_WAITING_P1'

def runServerCycle():
    while(True):
        messageAndClientAddress = UDPServerSocket.recvfrom(bufferSize)
        message = messageAndClientAddress[0]
        clientAddress = messageAndClientAddress[1]

        commandAndData = message.split(' ')
        command = message[0]
        data = message[1:]

        process(clientAddress, command, data)

def process(clientAddress, command, data):
    if(command == 'init'):
        sendCommand('message', 'Cliente {0} adicionado ao quiz'.format(clientAddress))
    if(command == 'message'):
        sendCommand('message', 'Cliente {0} enviou: {1}'.format(clientAddress, data))
    elif(command == 'end'):
        sendCommand('message', 'Cliente desconectado')

runServerCycle()