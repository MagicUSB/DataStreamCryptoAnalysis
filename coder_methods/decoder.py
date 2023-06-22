import numpy as np
from aux_coding_methods import factors
from tqdm import tqdm


def get_message_and_errors(file_name):
    with open(file_name, mode="rb") as f:
        matrix_from_file = np.fromfile(f, dtype=np.uint8)
    return decode(matrix_from_file)


def decode(matrix_from_file):
    data, hashed_key = np.array_split(matrix_from_file, 2)
    hash_size_list = [i for i in factors(len(hashed_key))]
    hash_size = hash_size_list[0]
    hash_table = np.linalg.inv(np.eye(hash_size, dtype=np.uint8))
    etalon = np.array([np.dot(hashed_key[i:i + hash_size], hash_table) for i in tqdm(range(0, len(hashed_key), hash_size), desc="Decoding hashed data: ")])
    print(np.array_equal(data, etalon.reshape(len(data))))
    with open("decoded.dat", mode="wb") as f:
        if np.array_equal(data, etalon.reshape(len(data))):
            data.tofile(f)
        else:
            etalon.flatten().tofile(f)
    return None

