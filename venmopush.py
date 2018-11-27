import os
import sendsms
import subprocess
import time

venmo_database = {"andy": 15103585981, "rohan": 14085042986, "ritik": 14088939075, "sahil": 15106485141}

#calls functions in venmopush
def maketransaction(function, amount, users, message, sender):
    if function == '#charge' and len(users) == 1:
        charge(amount, users[0], message,sender)
    elif function == '#charge' and len(users) > 1:
        chargemultiple(amount, users, message,sender)
    elif function == '#split':
        split(amount, users, message,sender)
    elif function == '#billpay':
        periodicpay(amount, users, message,sender)

# format of command: '#charge 5 15106485141'
def charge(amount, user, message,sender):
    query = 'venmo charge ' + str(user) + ' ' + amount + ' "' + message + '"'
    output = subprocess.check_output(query, shell=True)
    print(query)
    sendsms.send(sender, output)

# format of command: '#charge 20 15106485141 14085042986 14088939075'
def chargemultiple(amount, users, message,sender):
    for user in users:
        charge(amount, user, message,sender)

# format of a command: '#split 40 15106485141 14085042986 14088939075'
def split(amount, users, message,sender):
    chargemultiple(str(round(int(amount)/(len(users)+1), 2)), users, message,sender)
    # for user in users:
    #     msg = 'venmo charge ' + user + ' ' + str(round(int(amount)/(len(users)+1), 2)) + " 'for beers brooo'" #switch to manual message later
    #     print(msg)
    #     os.system(msg)

# format of a command: '#billpay 20 15106485141 14085042986 14088939075
def periodicpay(amount, users, message,sender):
    for _ in range(3):
        chargemultiple(amount, users, message,sender)
        time.sleep(15)
