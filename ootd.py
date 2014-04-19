#importing necessary libraries
import socket
import random
import fnmatch

#some default strings
defaultnick = ""
ownerhost = ""
fantasyletter = ""

#prompt the user for some necessary variables
server = raw_input("Enter the server you would like your bot to connect to: ")
channel = raw_input("Enter the channel(s) you would like your bot to connect to: ")
botnick = raw_input("Enter . to use the default bot nick, or enter the nick you would like your bot to connect as: ")

if botnick == ".":
   botnick = defaultnick

#some basic functions
def ping(msg):
   pingServer = ""
   servchar = False
   for i in msg:
      if servchar == True:
         pingServer += i
      elif i == " ":
         servchar = True
   irc.send("PONG " + pingServer + "\n")
   print "PONG " + pingServer

def sendmsg(chan, msg):
   irc.send("PRIVMSG " + chan + " :" + msg + "\n")
   print "PRIVMSG " + chan + " :" + msg

def changenick(nick):
   irc.send("NICK " + nick + "\n")
   print "NICK " + nick 

def joinchan(chan):
   irc.send("JOIN " + chan + "\n")
   print "JOIN " + chan

def partchan(chan):
   irc.send("PART " + chan + " :You all have no tech skill because you are all Nintendo.\n")
   print "PART " + chan + " :You all have no tech skill because you are all Nintendo."

def hello(chan):
   sendmsg(chan, "Hello. :|O")

def get(begin,end,msg):
   returnString = ""
   char = False
   for i in msg:
      if char == True:
         if i == end:
            break
         else:
            returnString += i
      elif i == begin:
         char = True
   return returnString 

def getArg(num,msg):
   returnString = ""
   foundColon = False
   foundFantasy = False
   char = False
   numSpaces = 0
   for i in msg:
      if char == True:
         if i == " ":
            break
         else:
            returnString += i
      elif foundFantasy == True:
         if i == " ":
            numSpaces += 1
         if numSpaces == num:
            char = True
      elif foundColon == True:
         if i == fantasyletter:
            foundFantasy = True
         else:
            foundColon = False
      elif i == ":":
         foundColon = True
   return returnString

def getNewNick(msg):
   returnString = ""
   char = False
   numColons = 0
   for i in msg:
      if char == True:
         returnString += i
      elif i == ":":
         numColons += 1
         if numColons == 2:
            char == True
      return returnString
               

def getChannel(msg,pm):
   numColons = 0
   returnString = ""
   char = False
   for i in msg:
      if char == True:
         if i == " ":
            break
         else:
            returnString += i
      elif i == ":":
         numColons += 1
         if numColons == 2:
            break
      elif i == "#":
         returnString += "#"
         char = True
   if (returnString == "") and (pm == True):
      returnString = getNick(msg)
   return returnString 

def getNick(msg):
   return get(":","!",msg)

def getHost(msg):
   return get(":"," ",msg) 

def stayConnected():

   #print messages to console
   if (ircmsg != ""):
      print(ircmsg)

   #terminate on disconnects
   else:
      disconnect = True

   #reply to pings from the server
   if ircmsg.find("PING :") != -1:
      ping(ircmsg)


#define some random responses
wellResponses = [
   "OMEGATYRANT?!?!?!?!?!?!?!?",
   "IS DREAM LAND IN BRAWL-?!?!?!?!?!?!?"
]

insults = [
   " has no tech skill because they are Nintendo.",
   ": eck yourself.",
   " is fucking bad.",
   ": are you a furry, furry?",
   " paused. What an asshole.",
   "'s tech skill is so bad, they lost sets to famous smashers such as TheLegendaryKRB and Burger King.",
   ": STOP DREAMING YOU FREAK?!?!?!?!?!?",
   " goes :|O",
   ": In the words of Yoda, \"No tech skill you have, because Nintendo you are.\"",
   ": Thou hast no tech skill in thy soul!",
   ": MORTAL",
   ": " + fantasyletter + "die",
   " is an out of touch dinosaur that doesn't do shit.",
   ": Because of your lack of bagels, you have been blocked until January 1, 1970.",
   " has no skill whatsoever because they are Microsoft.",
]

#connect the bot
disconnect = False
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc.connect((server, 6667))

#set the user and nick
irc.send("USER " + botnick + " " + " " + botnick + " " + botnick + " :This bot doesn't do shit.\n")
changenick(botnick)

#stay connected and join channels when ready
while disconnect == False:

   ircmsg = irc.recv(2048)
   ircmsg = ircmsg.strip('\n\r')

   stayConnected()

   #join once connected and break to the next loop
   if ircmsg.find(botnick) != -1:
      joinchan(channel)
      break 
  
#run commands as necessary
while disconnect == False:

   ircmsg = irc.recv(2048)
   ircmsg = ircmsg.strip('\n\r')

   stayConnected()

   #check to see if nick has changed and act accordingly
   if (ircmsg.find("NICK :") != -1) and (ircmsg.find(":" + botnick) != -1):
      botnick = getNewNick(ircmsg)

   #owner only commands
   if fnmatch.fnmatch(getHost(ircmsg).lower(),ownerhost):

      #@die
      if (ircmsg.find(":" + fantasyletter + "die") != -1):
         irc.send("QUIT :" + fantasyletter + "ded\n")
         print "QUIT :" +fantasyletter + "ded"
         break

      #@join and @part
      if (ircmsg.find(":" + fantasyletter + "join ") != -1):
         joinchan(getArg(1,ircmsg))

      if (ircmsg.find(":" + fantasyletter + "part") != -1):
         if getArg(1,ircmsg) == "":
            partchan(getChannel(ircmsg,False))
         else:
            partchan(getArg(1,ircmsg))

      #@nick
      if (ircmsg.find(":" + fantasyletter + "nick ") != -1):
         changenick(getArg(1,ircmsg))

   #@wake
   if ircmsg.find(":" + fantasyletter + "wake ") != -1:
      chan = getArg(2,ircmsg)
      nick = getArg(1,ircmsg)
      myNick = getNick(ircmsg)
      if chan == "":
         chan = getChannel(ircmsg,True)
      if nick.lower() != botnick.lower():
         sendmsg(chan,nick + ": WAKE UP?!?!?!?!?!?!?!?")
         if (nick.lower() == myNick.lower()) or (nick == ""):
            sendmsg(chan,myNick + ": Also, stop sleep-talking, you techless Nintendo.")
      else:
         sendmsg(chan,myNick + ": I am awake, you techless Nintendo.")

   if ircmsg.find(":" + fantasyletter + "test") != -1:
      sendmsg(getChannel(ircmsg,True),"I'M IN CLASS?!?!?!?!?!? TAKING A TEST?!?!?!?!?!?!?")

   if ircmsg.find(":" + fantasyletter + "help") != -1:
      sendmsg(getChannel(ircmsg,True),"Do you seriously think I'm going to HELP you?!?!?!? Go bother my programmer.")

   if ircmsg.find(":" + fantasyletter + "insult") != -1:
      nick = getArg(1,ircmsg)
      if nick == botnick:
         sendmsg(getChannel(ircmsg,True),getNick(ircmsg) + ": What a techless Nintendo. Did you really think I was going to insult myself?")
      else:
         sendmsg(getChannel(ircmsg,True),nick + random.choice(insults))

   #say hello!
   if ircmsg.lower().find(":hello " + botnick.lower()) != -1:
      hello(getChannel(ircmsg,True))

   #OMEGATYRANT?!?!?!?!?!?!?!?
   if ircmsg.lower().find(":well") != -1:
      sendmsg(getChannel(ircmsg,True),random.choice(wellResponses))

   if ircmsg.lower().find(":stupid bot") != -1:
      sendmsg(getChannel(ircmsg,True),getNick(ircmsg) + ": Source?")

   if ircmsg.find(":TWO") != -1:
      sendmsg(getChannel(ircmsg,True),"IS THAT POSSIBLE?!?!?!?!?!?!?!")

# (c) basically everyone, except not Conny
