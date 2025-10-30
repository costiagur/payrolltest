from ollama import Client
import re

def llmquery(myrequest,reqtype='timesheet'):
    client = Client(
    host='http://localhost:11434',
    #headers={'x-some-header': 'some-value'}
    )

    response = client.chat(model='timegemma' if reqtype == 'timesheet' else 'hazutigemma',stream=False, messages=[
    {
        'role': 'user',
        'content': myrequest
    },
    ])

    print(response.message.content)
    
    msg = response.message.content

    msg = msg.replace('sqlite','')
    msg = re.sub(r'`+','',msg)
    msg = re.sub(r'\n','',msg)

    return msg
#
