import random
import requests
import json
import string
import threading

numberThreads = 200

#replace with appropriate form url 
reqUrl='https://docs.google.com/forms/u/0/d/e/1FAIpQLSfoGSBtFk3Vc8hLX0pZv0dd5ZXDKrZ0pYTJtU01cP1Z2hpJjA/formResponse'


#stuff for generating random entries
emailDomains = ['gmail.com','cmail.carleton.ca','hotmail.com','yahoo.com','aol.com','hotmail.co.uk','live.com','outlook.com']
names = json.loads(open('names.json').read())
cities = json.loads(open('cities.json').read())
states = json.loads(open('states.json').read())

counter = 0

#generate n digit codes (for phone numbers)
def n_len_rand(len_, floor=1):
    top = 10**len_
    if floor > top:
        raise ValueError(f"Floor '{floor}' must be less than requested top '{top}'")
    return f'{random.randrange(floor, top):0{len_}}'

def sendResponses(): #go my child
    #variable init
    firstName = random.choice(names)
    lastName = random.choice(names)
    phoneNumber = n_len_rand(10)
    address = str(random.randint(0,9999)) + ' ' + random.choice(names) + ' ' + random.choice(['St.','Ave.','Rd.','Boulevard','Lane'])
    city = random.choice(cities)
    state = random.choice(states)
    zipCode = n_len_rand(random.randint(5,7))
    age = str(random.randint(5,150))
    sex = random.choice(['Male','Female'])

    #randomization station
    if(random.randint(0,2)==2): 
        email = firstName+lastName+str(random.randint(0,100))+'@'+random.choice(emailDomains)
    else:
        email = firstName+lastName+'@'+random.choice(emailDomains)
    if(random.randint(0,3)==2):
        firstname = firstName.capitalize()
        lastName = lastName.capitalize()
    if(random.randint(0,3) == 2):
        firstName = firstName.casefold()
        lastName = lastName.casefold()
    if(random.randint(0,2) == 2):
        for i in range(random.randint(1,10)):
            firstName+=random.choice(string.ascii_letters)
            lastName+=random.choice(string.ascii_letters)
            email = random.choice(string.ascii_letters) + email
    if(random.randint(0,3) == 3):
        email = email.casefold()
    if(random.randint(0,1) == 1):
        city = city.casefold()
    if(random.randint(0,1) == 1):
        state = state.casefold()

    #submit generated response (replace entry.xxxxxxx as appopriate)
    requests.post(reqUrl, allow_redirects=False,data={ 
        'entry.1191934627': firstName,
        'entry.1846598913': lastName,
        'entry.1483284269': email,
        'entry.800811391': phoneNumber,
        'entry.154319033': address,
        'entry.1772095134': city,
        'entry.1688826498': state,
        'entry.1395544488': zipCode,
        'entry.1713719114': age,
        'entry.1836501031': sex
    })

def spamResponses():
    while True:
        sendResponses()

threads = []
for i in range(numberThreads):
    threads.append(threading.Thread(target=spamResponses))
for i in range(numberThreads):
    threads[i].start()
