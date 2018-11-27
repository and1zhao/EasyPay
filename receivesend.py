import receivesms
import sendsms

def do(str):
    print(str)
    if str == 'send':
        sendsms.send('14088939075','hi')
    elif str == 'receive':
        receivesms.do()
