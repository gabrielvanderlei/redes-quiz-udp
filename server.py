import time
import collections
import pprint
import threading
import socket
import random

POINTS_WINNING = +25
POINTS_LOSING = -5
POINTS_NONE_ANSWER = -1
MAX_ROUNDS = 5
MAX_ROUND_TIME = 10000

localIP = "127.0.0.1"
localPort = 20001
bufferSize = 1024
questions = []
userPoints = {}
quizzStartedFlag = False
atualQuestion = 0
commands = ['start', 'register']
listOfClientsConnected = []
maxNumberOfClients = 5
address = 0
waitingResponse = False
waitingResponseTimer = 0

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
    global waitingResponse
    
    if questionId < MAX_ROUNDS:
        sendMessageToAllClients("Question {0}: {1}".format(questionId + 1, questions[questionId][0]))
    else:
        waitingResponse = False
        sendMessageToAllClients("End of the quiz.")
        sendMessageToAllClients("The final pontuation was:")
        
        for userAddress in collections.OrderedDict(sorted(userPoints.items())):
            points = userPoints[userAddress]
            sendMessageToAllClients("{0}: {1}".format(userAddress, points))
        
        quizzStartedFlag = False

    return questionId

def serverCycle(): 
    global POINTS_WINNING
    global POINTS_LOSING
    global MAX_ROUNDS
    global MAX_ROUND_TIME
    
    global bufferSize
    global questions
    global userPoints
    global quizzStartedFlag
    global atualQuestion
    global commands
    global listOfClientsConnected
    global maxNumberOfClients
    global address
    global waitingResponse
    global waitingResponseTimer

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
                sendMessageToClient( "There's a Quizz match running right now!")
                
            if (len(listOfClientsConnected) < maxNumberOfClients):
                if message == 'register':
                    if not (address in listOfClientsConnected):
                        listOfClientsConnected.append(address)
                        userPoints[address] = 0
                        sendMessageToClient("Client successfully registered!")
                        sendMessageToClient("\n")
                        sendMessageToClient("Wellcome!")
                        sendMessageToClient("Correct answers will add to your pontuaction will be changed by {0}".format(POINTS_WINNING))
                        sendMessageToClient("Wrong answers will add to your pontuaction will be changed by  {0}".format(POINTS_LOSING))
                        sendMessageToClient("If any correct response has been sent in 10 seconds, all players will have the pontuaction changed by {0}".format(POINTS_NONE_ANSWER))
                        sendMessageToClient("Message 'start' to close room and begin the quiz")
                        sendMessageToClient("\n")
                        print('Client {} registred in the Database'.format(address))
                    else:
                        sendMessageToClient("Client already registred!")
            else:
                sendMessageToClient("The Database is currently full!")
            
            if (message == 'start'):
                waitingResponse = True
                waitingResponseTimer = int(round(time.time() * 1000))
                questions = getQuestions()
                atualQuestion = runNextQuestion(atualQuestion)
                quizzStartedFlag = True

        else:
            if questions[atualQuestion][1] == message:
                waitingResponse = True
                waitingResponseTimer = int(round(time.time() * 1000))
                userPoints[address] += POINTS_WINNING
                sendMessageToAllClients("Correct! {0} has the right answer: {1}".format(address, message))
                sendMessageToClient("Pontuaction changed: {0}. New pontuation: {1}".format(POINTS_WINNING, userPoints[address]))
                atualQuestion = runNextQuestion(atualQuestion + 1)
            else:
                userPoints[address] += POINTS_LOSING
                sendMessageToClient("Wrong... Try again")
                sendMessageToClient("Pontuaction changed: {0}. New pontuation: {1}".format(POINTS_LOSING, userPoints[address]))

def timerCycle():
    global POINTS_NONE_ANSWER
    
    global userPoints
    global quizzStartedFlag
    global atualQuestion
    global address
    global waitingResponse
    global waitingResponseTimer
    
    while True:        
        atualMilliseconds = int(round(time.time() * 1000))
        pastMilliseconds = (atualMilliseconds - waitingResponseTimer)
        
        if waitingResponse and (pastMilliseconds > MAX_ROUND_TIME):
            waitingResponse = False
            
            for addressOfEachClientConected in listOfClientsConnected:
                address = addressOfEachClientConected
                userPoints[address] += POINTS_NONE_ANSWER
                sendMessageToClient("Any correct response in 10 seconds.")
                sendMessageToClient("Pontuaction changed: {0}. New pontuation: {1}".format(POINTS_NONE_ANSWER, userPoints[address]))
            
            waitingResponse = True
            waitingResponseTimer = int(round(time.time() * 1000))
            atualQuestion = runNextQuestion(atualQuestion + 1)

serverThread = threading.Thread(target=serverCycle, args=[])
serverThread.start()

timerThread = threading.Thread(target=timerCycle, args=[])
timerThread.start()