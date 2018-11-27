import nexmo

client = nexmo.Client(key='6b2a6370', secret='mfN15VZwqx00mDUy')

def send(number, message):
    print(number)
    client.send_message({
        'from': '14085029847',
        'to': number,
        'text': message
    })
