import os
#import sendsms
import subprocess
import venmopush
import sendsms
import time
file = open('response.json','r')

line1 = file.readline()
data = eval(line1)

text = data["text"][0]
##charge 1 14085042986
#text = '#billpay 20 15106485141 14085042986 14088939075'
sender = data["msisdn"][0]
command = text.split(" ")

all_functions = ['#charge', '#split', '#billpay']
function, amount, users, message_array, reason = '', '', [], [], ''

new_data = []
venmo_database = {"andy": 15103585981, "rohan": 14085042986, "ritik": 14088939075, "sahil": 15106485141}

possible_functions = {'#charge': ['owe', 'pay', 'send', 'venmo', 'give', 'spot', 'request'], '#split': ['divide', 'split'], '#billpay': []}


def parse_NLU():
    global new_data, function, users, amount, reason
    #Change 1st Line
    parameter = open('parameters.json', 'r')
    cur = parameter.readlines()
    #print(cur[1])
    cur[1] = cur[1][:13] + data["text"][0] + '",' + "\n"
    #print(cur[1])
    parameter.close()

    #Update ResponseJson
    parameter = open('parameters.json', 'w')
    parameter.writelines(cur)
    parameter.close()

    command = 'curl -X POST \
    -H "Content-Type: application/json" \
    -u "apikey:a3jHgMchnTE0W1ZIH3IemDKNUZpuqq6D3_4345HXkLVZ" \
    -d @parameters.json \
    "https://gateway.watsonplatform.net/natural-language-understanding/api/v1/analyze?version=2018-03-19"'
    output = subprocess.check_output(command, shell=True)
    output = eval(output)
    print("Output: " + str(output))
    #user = output["entities"][0]["text"]

    for element in output.get("entities", {'type': ''}):
        if element["type"] == "Name":
            users.append(element["text"])
        elif element["type"] == "Function":
            function = element["text"]
        elif element["type"] == "Amount":
            amount = element["text"]
        elif element["type"] == "Reason":
            reason = element["text"]


    #user = output.get("entities", -1)

    for i in range(len(users)):
        users[i] = users[i].lower()
        users[i] = venmo_database.get(users[i], 0)
    #function = output["entities"][1]["text"]
    #function = output.get("entities", -1)

    for fn in possible_functions:
        for possible_fn in possible_functions[fn]:
            if function == possible_fn:
                function = fn

    # if function == "owe":
    #     function = "#charge"
    # elif function == "pay":
    #     function = "#charge"
    # elif function == "send":
    #     function = "#charge"
    #amount = output["entities"][2]["text"]

    if not amount or not function or not users:
        return sendAll(sender,text)

    if amount[:1] == "$":
        amount = amount[1:]
    #reason = output["entities"][3]["text"]
    #print("Reason: " + str(reason))

    if not reason:
        reason = "default"

    new_data = [function, amount, users, reason]

def sendAll(sender,message):
    sndr_name = ''
    for name in venmo_database:
        if venmo_database[name] == int(sender):
            sndr_name = name
    for name in venmo_database:
        if venmo_database[name] != int(sender):
            msg = sndr_name.capitalize() + ': ' + message
            sendsms.send(venmo_database[name], msg)
            time.sleep(0.5)


parse_NLU()
print("Parsed: " + str(new_data))

# parses through code, splits into the function, amount, users, and an optional message
"""def parse(command_array):
    global function, amount, message
    if command_array[0] in all_functions: #see if fn is not one of our pre-defined functions
        function = command_array[0]
    try:
        amount = (str(int(command_array[1])))
    except ValueError:
        print('error') #fix this
        #exit the function - display 'invalid amt'
    #amount = command_array[1] #see if this is a valid number - do try/catch later
    for elem in command_array[2:]:
        try:
            users.append(str(int(elem))) #make sure they are in order as well
        except ValueError:
            message_array.append(elem)
    for message_part in message_array:
        message += message_part + ' '
    if message == '':
        message = 'default'"""

#parse(new_data)
#print(message)
command = [function, amount, users, reason, sender]

print("Executing:" + str(command))
venmopush.maketransaction(function, amount, users, reason, sender)

file.close()
