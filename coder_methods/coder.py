import numpy as np
from tqdm import tqdm # doesn't work on Windows 7, needs newer Python
from aux_coding_methods import factors


def add_hash_to_message(input_data):
    hash_size_list = []
    for i in factors(len(input_data)):
        hash_size_list.append(i)
    hash_size = hash_size_list[0]
    hash_table = np.eye(hash_size, dtype=np.uint8)
    with open('test.dat', 'wb') as f:
        input_data.tofile(f)
        np.array([np.dot(input_data[i:i + hash_size], hash_table) for i in tqdm(range(0, len(input_data), hash_size), desc="Adding hash to data: ")]).tofile(f)
