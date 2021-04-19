import pprint
import threading
import socket
import random

POINTS_WINNING = +25
POINTS_LOSING = -5
POINTS_NONE_ANSWER = -1
MAX_ROUNDS = 5

localIP = "127.0.0.1"
localPort = 20001
bufferSize = 1024
questions = []
userPoints = {}

print("Reading question list.")

questionList = []
with open('ask-and-questions.txt') as file:
    questionList = [tuple(line.replace('\n', '').split(" /// ")) for line in file]

print("Question list successfully loaded.")

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))
print("UDP Server is running at port {}".format(localPort))

def serverCycle(): 
    atualQuestion = 0
    commands = ['start', 'register']
    quizzStartedFlag = False
    listOfClientsConnected = []
    maxNumberOfClients = 5
    address = 0

    def getQuestions():
        print("Loading questions to quiz.")
        allNotSelectedQuestions = questionList
        questions = []
        
        for questionId in range(0, MAX_ROUNDS):
            numberOfQuestions = len(allNotSelectedQuestions)
            questionChoosed = random.randint(0, numberOfQuestions - 1)
            questions.append(allNotSelectedQuestions.pop(questionChoosed))
        
        print("Questions successfully loaded.")
        return questions
        
        

    def sendMessageToClient(msgFromServer):
        bytesToSend = str.encode(msgFromServer)
        print('Sending to {0}: {1}'.format(address, msgFromServer))
        UDPServerSocket.sendto(bytesToSend, address)

    def sendMessageToAllClients(msgFromServer):
        for addressOfEachClientConected in listOfClientsConnected:
            address = addressOfEachClientConected
            sendMessageToClient(msgFromServer)

    def runNextQuestion(questionId, correctMessage=False):
        if questionId < MAX_ROUNDS:
            if not correctMessage:
                sendMessageToAllClients("Question {0}: {1}".format(questionId + 1, questions[questionId][0]))
            else:
                sendMessageToAllClients("{0} \n Question {1}: {2}".format(correctMessage, questionId + 1, questions[questionId][0]))
        else:
            message = "End of the quiz. \n"
            message += "The final pontuation was: \n"
            
            for userAddress in userPoints:
                points = userPoints[userAddress]
                message += "{0}: {1}".format(userAddress, points)
            
            sendMessageToAllClients(message)
            quizzStartedFlag = False
    
        return questionId

    # Listen for incoming datagrams
    while(True):
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        message = bytesAddressPair[0].decode("utf-8")
        address = bytesAddressPair[1]

        print('Received from client: {0} / {1}'.format(message, address))

        if not quizzStartedFlag:
            # When the user try to enter an aleatory command
            if not (message in commands):
                sendMessageToClient("Enter a correct Command \n")
            
            # When the user try to join in a current match
            if (message == 'register' or message == 'start') and (quizzStartedFlag):
                sendMessageToClient( "There's a Quizz match running right now! \n")
                
            if (len(listOfClientsConnected) < maxNumberOfClients):
                if message == 'register':
                    if not (address in listOfClientsConnected):
                        listOfClientsConnected.append(address)
                        userPoints[address] = 0
                        sendMessageToClient("Client successfully registred! \n")
                        print('Client {} registred in the Database'.format(address))
                    else:
                        sendMessageToClient("Client already registred! \n")
            else:
                sendMessageToClient("The Database is currently full! \n")
            
            if (message == 'start'):
                questions = getQuestions()
                atualQuestion = runNextQuestion(atualQuestion)
                quizzStartedFlag = True

        else:
            if questions[atualQuestion][1] == message:
                userPoints[address] += POINTS_WINNING
                atualQuestion = runNextQuestion(atualQuestion + 1, "Correct! {0} has the right answer: {1}".format(address, message))
            else:
                userPoints[address] += POINTS_LOSING
                sendMessageToClient("Wrong... Try again")



serverThread = threading.Thread(target=serverCycle, args=[])
serverThread.start()