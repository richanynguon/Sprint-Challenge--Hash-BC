#  Hint:  You may not need all of these.  Remove the unused functions.
from hashtables import (HashTable,
                        hash_table_insert,
                        hash_table_remove,
                        hash_table_retrieve,
                        hash_table_resize)


class Ticket:
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination


def reconstruct_trip(tickets, length):
    hashtable = HashTable(length)
    route = [None] * (length-1)

    """
    YOUR CODE HERE
    """
    for idx in range(length):
        hash_table_insert(hashtable, tickets[idx].source, tickets[idx].destination)
    key = "NONE"
    for idx in range(length):
        destination = hash_table_retrieve(hashtable, key)
        if key is not None and destination is not "NONE":
            route[idx]= destination
            key = destination
    
    return route
                

