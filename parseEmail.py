#!/usr/bin/env python
## Code to process Enron mail corpus (get sender, receipient and time)
## modified from Balasubramanian Narasimhan
## Takes about 6 min of time on a decent computer to process...
##
import time, dircache, os, os.path, email, itertools
from email.Utils import getaddresses

def getSender(filename):
	fp = open(filename, "r")
	msg = email.message_from_file(fp)
	fp.close()
	return msg.get("from")

def getSenderAndRecipientsAndDate(filename):
    fp = open(filename, "r")
    msg = email.message_from_file(fp)
    sender = msg.get("from")
    date = email.utils.parsedate(msg.get("Date"))
    tos = msg.get_all("to", [])
    ccs = msg.get_all("cc", [])
    fp.close()
    recipients = [elem[1] for elem in getaddresses(tos)]
    recipients.extend([elem[1] for elem in getaddresses(ccs)])
    result = {}
    result['sender'] = sender
    result['recipients'] = recipients
    result['date'] = date
    return result

def emitEdges(senderAndRecipientsAndDate):
    sender = senderAndRecipientsAndDate['sender']
    recipients = senderAndRecipientsAndDate['recipients']
    try:
        originator = canonicalName[sender]
        for recipient in recipients:
            try:
                target = canonicalName[recipient]
                if originator != target :
                    date = senderAndRecipientsAndDate['date']
                    print originator + "," + target + "," + time.strftime("%Y/%m/%d,%H:%M:%S", date)
            except KeyError:
                continue
    except KeyError:
        pass

datadir = "/home/stat290/public/data/enron/maildir/" ## Example: "./enron_mail_20110402/maildir"

#get all userids
userids = dircache.listdir(datadir)

#map all aliases to userid
userAliases = {}
for userid in userids:
#    print userid
    aliases = set()
    for folder in ['sent', 'sent_items', '_sent_mail']:
        dirName = os.path.join(datadir, userid, folder)
        if os.path.exists(dirName):
            filename = dircache.listdir(dirName)
            for fname in filename:
                fullname=os.path.join(dirName, fname)
                #print fullname
                if os.path.isfile(fullname):
                    w = getSender(fullname)
                    aliases.add(w)
    userAliases[userid] = aliases


#find userids with 2 or more aliases
problemSenders = set()
for x, y in itertools.combinations(userAliases.keys(), 2):
    w = userAliases[x].intersection(userAliases[y])
    if len(w) > 0:
 #       print x, y
        problemSenders = problemSenders.union(w)
        userAliases[x] = userAliases[x].difference(w)
        userAliases[y] = userAliases[y].difference(w)

		
#select canonical name from multiple aliases
canonicalName = {}
for x in userAliases.keys():
    for y in userAliases[x]:
        canonicalName[y] = x

##
## Now go through all email messages to find out the sender
##
for root, dirs, files in os.walk(datadir):
    for name in files:
        fullname = os.path.join(root, name)
        w = getSenderAndRecipientsAndDate(fullname)
        emitEdges(w)


