import random

import requests
import json
import string
import threading

number_threads = 200
spam_count = 200
print_frequency = 100

# replace with appropriate form url
req_url = 'https://docs.google.com/forms/u/0/d/e/1FAIpQLSfoGSBtFk3Vc8hLX0pZv0dd5ZXDKrZ0pYTJtU01cP1Z2hpJjA/formResponse'

# stuff for generating random entries
email_domains = ['gmail.com', 'cmail.carleton.ca', 'hotmail.com', 'yahoo.com',
                 'aol.com', 'hotmail.co.uk', 'live.com', 'outlook.com',
                 'carleton.ca', 'live.ca']
names = json.loads(open('names.json').read())
cities = json.loads(open('cities.json').read())
states = json.loads(open('states.json').read())

counter = 0


# generate n digit codes (for phone numbers)
def n_len_rand(len_, floor=1):
    top = 10 ** len_
    if floor > top:
        raise ValueError(
            f"Floor '{floor}' must be less than requested top '{top}'")
    return f'{random.randrange(floor, top):0{len_}}'


def send_responses():  # go my child
    # variable init
    first_name = random.choice(names)
    last_name = random.choice(names)
    phone_number = n_len_rand(10)
    address = str(random.randint(0, 9999)) + ' ' + random.choice(
        names) + ' ' + random.choice(
        ['St.', 'Ave.', 'Rd.', 'Boulevard', 'Lane'])
    city = random.choice(cities)
    state = random.choice(states)
    zip_code = n_len_rand(random.randint(5, 7))
    age = str(random.randint(5, 150))
    sex = random.choice(['Male', 'Female'])

    # randomization station
    if random.randint(0, 2) == 2:
        email = first_name + last_name + str(
            random.randint(0, 100)) + '@' + random.choice(email_domains)
    else:
        email = first_name + last_name + '@' + random.choice(email_domains)

    if random.randint(0, 3) == 2:
        first_name = first_name.capitalize()
        last_name = last_name.capitalize()

    if random.randint(0, 3) == 2:
        first_name = first_name.casefold()
        last_name = last_name.casefold()

    if random.randint(0, 2) == 2:
        for k in range(random.randint(1, 10)):
            first_name += random.choice(string.ascii_letters)
            last_name += random.choice(string.ascii_letters)
            email = random.choice(string.ascii_letters) + email

    if random.randint(0, 3) == 3:
        email = email.casefold()

    if random.randint(0, 1) == 1:
        city = city.casefold()

    if random.randint(0, 1) == 1:
        state = state.casefold()

    # submit generated response (replace entry.xxxxxxx as appropriate)
    requests.post(req_url, allow_redirects=False, data={
        'entry.1191934627': first_name,
        'entry.1846598913': last_name,
        'entry.1483284269': email,
        'entry.800811391': phone_number,
        'entry.154319033': address,
        'entry.1772095134': city,
        'entry.1688826498': state,
        'entry.1395544488': zip_code,
        'entry.1713719114': age,
        'entry.1836501031': sex
    })


def spam_responses(thread_num):
    for q in range(spam_count):
        send_responses()
        if q != 0 and (q + 1) % print_frequency == 0:
            print(f"Thread {thread_num} has successfully sent "
                  f"{q + 1} bogus responses so far")


if __name__ == "__main__":
    threads = []
    print("Sending responses - please wait")
    for i in range(number_threads):
        threads.append(threading.Thread(target=spam_responses, args=(i,)))
    for x in range(number_threads):
        threads[x].start()
    for y in range(number_threads):
        threads[x].join()
