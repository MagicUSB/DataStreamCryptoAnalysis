import numpy as np

def get_message_and_errors(file_name):
    matrix_from_file = np.loadtxt(file_name, delimiter=',')
    return decode(matrix_from_file)


def decode(matrix_from_file):
    data, key = np.vsplit(matrix_from_file, 2)
    hash_table = key
    # print(data)
    # print()
    # print(key)
    string_builder = ""
    errors = []
    for i in range(0, len(data)):
        test_hash = np.dot(data[i], key[i])
        if np.array_equal(test_hash, data[i]):
            errors.append(i)
            data[i] = np.dot(key[i], np.linalg.inv(hash_table))
        for item in data[i]:
            string_builder += chr(int(item))
    print(string_builder, errors)
    return string_builder, errors

