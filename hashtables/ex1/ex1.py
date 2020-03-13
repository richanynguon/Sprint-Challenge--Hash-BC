#  Hint:  You may not need all of these.  Remove the unused functions.
from hashtables import (HashTable,
                        hash_table_insert,
                        hash_table_remove,
                        hash_table_retrieve,
                        hash_table_resize)


def get_indices_of_item_weights(weights, length, limit):
    ht = HashTable(16)

    """
    YOUR CODE HERE
    """
    for idx in range(len(weights)):
        hash_table_insert(ht, weights[idx], idx)

    results = None
    for idx in range(len(weights)):
        #retrive the key that will add up to the limit
        find_entry = hash_table_retrieve(ht, limit-weights[idx])
        if find_entry is not None and find_entry != idx:
            if find_entry > idx:
                results = (find_entry, idx)
                break
            else:
                #returns the index and then none
                results = (idx, find_entry)

    return results

def print_answer(answer):
    if answer is not None:
        print(str(answer[0] + " " + answer[1]))
    else:
        print("None")
