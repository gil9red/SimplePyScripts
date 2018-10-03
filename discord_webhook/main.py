__author__="ev-ev"
__licence__="MIT license"

import requests
import json

WEBHOOK_LINK = 'YOUR-LINK-HERE'

def send_message(message): #send a message via the webhook
    r = requests.post(WEBHOOK_LINK, json={"content": message})
    return None

def main(): #Code should be self-explanatory
    try:
        while True:
            message = input('Input message to send:')
            print('Sending message {}...'.format(message))
            send_message(message)
            print('Message sent.')
    except KeyboardInterrupt:
        print('\nUser requested shutdown...')
        return None
 
if __name__ == "__main__":
    main()