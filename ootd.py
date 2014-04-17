#importing necessary libraries
import socket
import random

#prompt the user for some necessary variables
server = raw_input("Enter the server you would like your bot to connect to: ")
channel = raw_input("Enter the channel(s) you would like your bot to connect to: ")
botnick = raw_input("Enter the nick you would like your bot to connect as: ")

#some basic functions
def ping(msg):
   pingServer = ""
   servchar = False
   for i in msg:
      if servchar == True:
         pingServer += i
      elif i == ":":
         servchar = True
   irc.send("PONG " + pingServer + "\n")
   print "PONG " + pingServer

def sendmsg(chan, msg):
   irc.send("PRIVMSG " + chan + " :" + msg + "\n")

def changenick(nick):
   botnick = nick
   irc.send("NICK " + botnick + "\n")

def joinchan(chan):
   irc.send("JOIN " + chan + "\n")

def hello(chan):
   sendmsg(chan, "Hello. :|O")

def getChannel(msg):
        chanchar = False
        channel = ""					
	for i in msg:
           if i == "#":
              chanchar = True
              channel += "#"
           elif chanchar == True:
             if i == " ":
               break
             else:
              channel += i
	return channel

def getNick(msg):
        nick = ""					
	for i in msg:
           if i == "!":
              break
           elif i != ":":
              nick += i
	return nick


#define some random responses
wellResponses = [
   "OMEGATYRANT?!?!?!?!?!?!?!?",
   "IS DREAM LAND IN BRAWL-?!?!?!?!?!?!?"
]

#connect the bot
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc.connect((server, 6667))

#set the user and nick
irc.send("USER " + botnick + " " + " " + botnick + " " + botnick + " :This bot doesn't do shit.\n")
changenick(botnick)

#join channel(s)
joinchan(channel)   

#receive data from the server
while (True):
   ircmsg = irc.recv(2048)
   ircmsg = ircmsg.strip('\n\r')

   #print messages to console
   if (ircmsg != ""):
      print(ircmsg)

   #terminate on disconnects
   else:
      break

   #reply to pings from the server
   if ircmsg.find("PING :") != -1:
      ping(ircmsg)
   
   #say hello!
   if ircmsg.lower().find(":hello " + botnick.lower()) != -1:
      hello(getChannel(ircmsg))

   #OMEGATYRANT?!?!?!?!?!?!?!?
   if ircmsg.lower().find(":well") != -1:
      sendmsg(getChannel(ircmsg),random.choice(wellResponses))

   if ircmsg.lower().find(":stupid bot") != -1:
      sendmsg(getChannel(ircmsg),getNick(ircmsg) + ": Source?")

   if ircmsg.find(":TWO") != -1:
      sendmsg(getChannel(ircmsg),"IS THAT POSSIBLE?!?!?!?!?!?!?!")

# (c) basically everyone, except not Conny
