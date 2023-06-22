import numpy as np
import csv

def add_hash_to_message(msg, hash_size):
    hash_table = np.eye(hash_size).astype(int)
    if len(msg) % hash_size != 0:
        x = len(msg) % hash_size
        for i in range(hash_size - x):
            msg += " "
    blocks = []
    for i in range(0, len(msg), hash_size):
        blocks.append(msg[i:i + hash_size])
    char_blocks = []
    for i in range(len(blocks)):
        chrs = []
        for c in blocks[i]:
            chrs.append(ord(c))
        char_blocks.append(np.array(chrs).reshape(1, hash_size))
    hashes = calculate_hashes(char_blocks, hash_table)
    with open('message.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        output = char_blocks[0]
        for j in range(1, len(char_blocks)):
            output = np.append(output, char_blocks[j], axis=0)
        for j in range(len(hashes)):
            output = np.append(output, hashes[j], axis=0)
        writer.writerows(output)

def calculate_hashes(blocks, var_hash_table):
    hashes = []
    for i in range(len(blocks)):
        hashes.append(np.dot(blocks[i], var_hash_table))
    return hashes

