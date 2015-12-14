#importing necessary libraries
import socket
import random
import fnmatch
import getpass
import sys

#some default strings
defaultnick =
ownerhost =
fantasyletter =
#Does not work 
modes =

#prompt the user for some necessary variables
server = raw_input("Enter the server you would like your bot to connect to: ")
channel = raw_input("Enter the channel(s) you would like your bot to connect to: ")
botnick = raw_input("Enter . to use the default bot nick, or enter the nick you would like your bot to connect as: ")
password = getpass.getpass("Enter the NickServ password, or hit enter to not identify to NickServ: ")

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

def getArg(num,total,msg):
    returnString = ""
    foundColon = False
    foundFantasy = False
    char = False
    numSpaces = 0
    for i in msg:
        if char == True:
            if i == " " and not total:
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
    numSpaces = 0
    for i in msg:
        if char == True:
            returnString += i
        elif i == " ":
            numSpaces += 1
            if numSpaces == 2:
                char = True
    return returnString


def getChannel(msg,pm):
    numSpaces = 0
    returnString = ""
    char = False
    for i in msg:
        if i == " ":
            numSpaces += 1
            if numSpaces == 3:
                break
        elif char == True:
            returnString += i
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
        print "ERROR: Unexpected disconnect from server!"
        sys.exit(1)
    #reply to pings from the server
    if ircmsg.find("PING :") != -1:
        ping(ircmsg)


#define some random responses
wellResponses = [
                 "OMEGATYRANT?!?!?!?!?!?!?!?",
                 "IS DREAM LAND IN BRAWL-?!?!?!?!?!?!?",
                 "FEELS SO GOOD?!?!?!?!?!?!?!?",
                 "OMEGARUBY?!?!?!?!?!?!?!?",
                 "OMEGAWATCHES?!?!?!?!?!?!?!?",
                 "OMEGAFORM?!?!?!?!?!?!?!?",
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
           " goes :{O",
           " does not go goy and is therefore in serious trouble.",
           " is one of those things that you can throw overneath the bridge.",
           " has no hidden potential.",
           ": please start making sense.",
           " is a straight up jerk; I get the chance to go for a high score in All-Star Mode like twice a year and they corrupt my save data. So BM.",
           " is both Nintendo and Microsoft at the same time. Therefore, they not only have no tech skill, they have negative tech skill.",
           "'s crush will never respond to their emails.",
           " is a baka.",
           " goes intothetrash.bin.",
           " kicked the goyball overneath their own gol.",
           " likes Picturesque Matchstickable Messages From The Status Quo.",
           " is the Phantom Menace.",
           " quat. What a techless Nintendo.",
           ]

sources = [
           "<ecks>",
           "moi",
           "me",
           "<ecks> your mom",
           "<furry>",
           "\001ACTION \001",
           "https://ridley.fastlizard4.org/~fastlizard4/source.txt",
           "http://google.com/",
           "open",
           "<ecks> moi",
           "a laptop",
          ]

#connect the bot
#disconnect = False
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc.connect((server, 6667))

#set the user and nick
irc.send("USER " + botnick + " " + " " + botnick + " " + botnick + " :This bot is a fake bagel.\n")
changenick(botnick)

#stay connected and join channels when ready
while True:
    
    ircmsg = irc.recv(2048)
    ircmsg = ircmsg.strip('\n\r')
    
    stayConnected()
    
    #join once connected and break to the next loop
    if ircmsg.find("MODE " + botnick) != -1:
        joinchan(channel)
        if password != "":
           sendmsg("NickServ","identify " + password)
           print "Identifying..."
        if modes != "":
           irc.send("MODE " + botnick + " " + modes + "\n") 
           print "Setting modes: " + modes
        break

#run commands as necessary
while True:
    
    ircmsg = irc.recv(2048)
    ircmsg = ircmsg.strip('\n\r')
    stayConnected()
    
    chanT = ""
    try:
        if getChannel(ircmsg,True)[0] == "#":
            chanT == getChannel(ircmsg,True)
        else:
            chanT == botnick
    except:
        continue
    
    #check to see if nick has changed and act accordingly
    if (ircmsg.find("NICK ") != -1) and (ircmsg.find(":" + botnick) != -1):
        botnick = getNewNick(ircmsg)
    
    #owner only commands
    if fnmatch.fnmatch(getHost(ircmsg).lower(),ownerhost):
        
        #@die
        if (ircmsg.find(chanT + " :" + fantasyletter + "die") != -1):
            irc.send("QUIT :" + fantasyletter + "ded\n")
            print "QUIT :" +fantasyletter + "ded"
            break
        
        #@join and @part
        if (ircmsg.find(chanT + " :" + fantasyletter + "join ") != -1):
            joinchan(getArg(1,False,ircmsg))
        
        if (ircmsg.find(chanT + " :" + fantasyletter + "part") != -1):
            if getArg(1,False,ircmsg) == "":
                partchan(getChannel(ircmsg,False))
            else:
                partchan(getArg(1,False,ircmsg))
        
        #@nick
        if (ircmsg.find(chanT + " :" + fantasyletter + "nick ") != -1):
            changenick(getArg(1,False,ircmsg))
        
        #@say and @do
        if (ircmsg.find(chanT + " :" + fantasyletter + "say ") != -1):
            sendmsg(getArg(1,False,ircmsg),getArg(2,True,ircmsg))
        
        if (ircmsg.find(chanT + " :" + fantasyletter + "do ") != -1):
            sendmsg(getArg(1,False,ircmsg),"\001ACTION " + getArg(2,True,ircmsg) + "\001")
    
    
    #@wake
    if ircmsg.find(chanT + " :" + fantasyletter + "wake ") != -1:
        chan = getArg(2,False,ircmsg)
        nick = getArg(1,False,ircmsg)
        myNick = getNick(ircmsg)
        if chan == "":
            chan = getChannel(ircmsg,True)
        if nick.lower() != botnick.lower():
            sendmsg(chan,nick + ": WAKE UP?!?!?!?!?!?!?!?")
            if (nick.lower() == myNick.lower()) or (nick == ""):
                sendmsg(chan,myNick + ": Also, stop sleep-talking, you techless Nintendo.")
        else:
            sendmsg(chan,myNick + ": I am awake, you techless Nintendo.")

    if ircmsg.find(chanT + " :" + fantasyletter + "sleep ") != -1:
        chan = getArg(2,False,ircmsg)
        nick = getArg(1,False,ircmsg)
        myNick = getNick(ircmsg)
        if chan == "":
            chan = getChannel(ircmsg,True)
        if nick.lower() != botnick.lower():
            sendmsg(chan,nick + ": START DREAMING YOU FREAK?!?!?!?!?!?!?!?")
        else:
            sendmsg(chan,myNick + ": no u")
    
    if ircmsg.find(chanT + " :" + fantasyletter + "thank ") != -1:
        chan = getArg(2,False,ircmsg)
        nick = getArg(1,False,ircmsg)
        myNick = getNick(ircmsg)
        if chan == "":
            chan = getChannel(ircmsg,True)
        if nick.lower() != botnick.lower():
            sendmsg(chan,nick + ": https://www.youtube.com/watch?v=5VL_5MX7z94")
            if (nick.lower() == myNick.lower()) or (nick == ""):
                sendmsg(chan,"</sarcasm>")
        else:
            sendmsg(chan,myNick + ": I thank myself for being the most awesome being ever to exist. :)")
    
    if ircmsg.find(chanT + " :" + fantasyletter + "test") != -1:
        sendmsg(getChannel(ircmsg,True),"I'M IN CLASS?!?!?!?!?!? TAKING A TEST?!?!?!?!?!?!?")
    
    if ircmsg.find(chanT + " :" + fantasyletter + "help") != -1:
        sendmsg(getChannel(ircmsg,True),"Do you seriously think I'm going to HELP you?!?!?!? Go bother my programmer.")
    
    if ircmsg.find(chanT + " :" + fantasyletter + "insult") != -1:
        nick = getArg(1,False,ircmsg)
        if nick.lower() == botnick.lower():
            sendmsg(getChannel(ircmsg,True),getNick(ircmsg) + ": What a techless Nintendo. Did you really think I was going to insult myself?")
        else:
            append = getArg(2,False,ircmsg)
            i = 2
            while append:
                if append.lower() == botnick.lower():
                    sendmsg(getChannel(ircmsg,True),getNick(ircmsg) + ": What a really techless Nintendo. Did you really think I was going to insult a group containing myself?")
                nick = nick + " " + append
                i += 1
                append = getArg(i, False, ircmsg)
            sendmsg(getChannel(ircmsg,True),nick + random.choice(insults))
    

    if ircmsg.lower().find(chanT + " :" + botnick.lower() + ": source?") != -1:
         sendmsg(getChannel(ircmsg,True),random.choice(sources))

    #say hello!
    if ircmsg.lower().find(chanT + " :hello " + botnick.lower()) != -1:
        hello(getChannel(ircmsg,True))
    
    #OMEGATYRANT?!?!?!?!?!?!?!?
    if ircmsg.find(chanT + " :WELL") != -1:
        sendmsg(getChannel(ircmsg,True),random.choice(wellResponses))
    
    if ircmsg.lower().find(chanT + " :stupid bot") != -1:
        sendmsg(getChannel(ircmsg,True),getNick(ircmsg) + ": Source?")

    if ircmsg.lower().find(chanT + " :sup ") != -1:
        sendmsg(getChannel(ircmsg,True),"sup is an unknown command.")
    
    if ircmsg.find(chanT + " :TWO ") != -1:
        sendmsg(getChannel(ircmsg,True),"IS THAT POSSIBLE?!?!?!?!?!?!?!")

    if ircmsg.find(chanT + " :THREE ") != -1:
        sendmsg(getChannel(ircmsg,True),"WHAT IS HAPPENING?!?!?!?!?!?!?!")

    if ircmsg.find(chanT + " :FOUR ") != -1:
        sendmsg(getChannel(ircmsg,True),"or something")

    if ircmsg.find(chanT + " :FIVE ") != -1:
        sendmsg(getChannel(ircmsg,True),"YOU CAN'T EXPLAIN THAT?!?!?!?!?!?!?!")

# (c) basically everyone, except not Conny
