#!/usr/bin/env python3
import requests
from sys import argv
from local_storage import LocalStorage
storage = LocalStorage("app-test.json")
storage.caching()
# storage.save({'x':5, 'y':50})
# storage.commit()
HP = 'http://127.0.01:5005'

def request_0():
    response = requests.get(HP + "/about")
    if response.status_code == 200:
     print(f"re =>  {response.content}")

    else:
        print(f"\n\nstatus code 0 => : {response.status_code}")


def request_1():
    import requests
    response = requests.get(HP + '/about__api__')

    if response.status_code == 200:
        print(f"json response {response.json()}")
        print(f"json .cookies {response.cookies.__dict__}")
    else:
        print(f"\n\nstatus code 1 => : {response.status_code}")


def request_2():
    URL = HP + '/useless'
    # Define the parameters as a dictionary
    payload = {'number': 'str', 'key2': 'value', 'tag':'h1', 'sprt_tag':'hr'}

    # Make a GET request with the parameters
    response = requests.get(URL, params=payload)

    if response.status_code == 200:
        # Print the final URL with parameters encoded
        print(response.url)

        # Save the response content if needed
        storage.save(response.json())  # or response.content or response.text depending on your need
        storage.commit()
    else:
        print(f"\n\nstatus code 2 => : {response.status_code}")



if __name__ == "__main__":
    if len(argv) > 1:
        for arg in argv:
            if arg == "0":
                print("x")

                request_0()
            if arg == "1":
                request_1()
            if arg == "2":
                request_2()
