import hashlib
import requests

import sys

from uuid import uuid4
from time import sleep
from threading import *
from timeit import default_timer as timer
import queue
import random


def proof_of_work(arg_queue):
    last_proof = arg_queue.get()
    proof = random.getrandbits(256)
    prev_proof = f'{last_proof}'.encode()
    prev_hash = hashlib.sha256(prev_proof).hexdigest()
    print("Searching for next proof")
    while not valid_proof(prev_hash, proof) and arg_queue.empty():
        proof = random.getrandbits(256)
    print("Proof found")
    if arg_queue.empty():
      return proof
    else:
      return False


def valid_proof(last_hash, proof):
    guess_string = f'{proof}'.encode()
    guess_hash = hashlib.sha256(guess_string).hexdigest()
    return last_hash[-6:] == guess_hash[:6]


if __name__ == '__main__':
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "https://lambda-coin.herokuapp.com/api"

    coins_mined = 0
    arg_queue = queue.Queue()
    f = open("my_id.txt", "r")
    id = f.read()
    print("ID is", id)
    f.close()

    if id == 'NONAME\n':
        print("ERROR: You must change your name in `my_id.txt`!")
        exit()

    r = requests.get(url=node + "/last_proof")
    data = r.json()
    arg_queue.put(data.get('proof'))

    def same_proof(arg_queue):
        prev = arg_queue.get()
        while True:
            r = requests.get(url=node + "/last_proof")
            data = r.json()
            if prev != data.get('proof'):
                prev = data.get('proof')
                arg_queue.put(data.get('proof'))
            sleep(1)

    def mine(arg_queue, coins_mined):
        while True:
          new_proof = proof_of_work(arg_queue)
          if new_proof:
            post_data = {"proof": new_proof,
                        "id": id}
            r = requests.post(url=node + "/mine", json=post_data)
            data = r.json()
            if data.get('message') == 'New Block Forged':
                coins_mined += 1
                print("Total coins mined: " + str(coins_mined))
            else:
                print(data.get('message'))
       

    poll = Thread(target=same_proof, args=(arg_queue,))
    miner = Thread(target=mine, args=(arg_queue,coins_mined))
    poll.start()
    miner.start()

  