import csv
import json
import random
import string
import math
import time

from coder_methods import pyae
from decimal import getcontext


'''
Тут зберігаються методи, які відповідають за кодування, і які використовуються інтерфейсом програми.
'''

def ae_encode_write_to_file(probability_table, ae_output_file_name, encoded_msg, original_msg):
    with open(ae_output_file_name, 'w') as f:
        f.write(str(encoded_msg) + '\n')
        f.write(str(len(original_msg)) + '\n')
        json.dump(probability_table, f)


def ae_encode(msg):
    freq_table = get_frequency_table(msg)
    ae = pyae.ArithmeticEncoding(frequency_table=freq_table,
                                 save_stages=False)
    original_msg = msg
    #print("Original Message: {msg}".format(msg=original_msg))
    #
    encoded_msg, encoder, interval_min_value, interval_max_value = ae.encode(msg=original_msg,
                                                                             probability_table=ae.probability_table)
    #print("Encoded Message: {msg}".format(msg=encoded_msg))
    return ae, encoded_msg, original_msg


def get_frequency_table(msg):
    freq_table = {}
    for element in msg:
        if element in freq_table:
            freq_table[element] += 1
        else:
            freq_table[element] = 1
    return freq_table


def csv_to_string(file_name):
    arr = []
    with open(file_name) as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            for i in row:
                arr.append(i)
    msg = ' '.join(arr)
    return msg


def factors(n):
    while n > 1:
        for i in range(2, n + 1):
            if n % i == 0:
                n //= i
                yield i
                break


def get_random_string(chars=string.ascii_uppercase + string.ascii_lowercase + string.digits, N=10):
    return ''.join(random.choice(chars) for _ in range(N))


def find_min_prec(s):
    cnt = int(1.5 * len(s))
    getcontext().prec = cnt
    result = False
    while not result:
        ae, encoded_msg, original_msg = ae_encode(s)
        pt = ae.probability_table
        ae1 = pyae.ArithmeticEncoding(frequency_table={}, save_stages=False)
        decoded_msg, ae_decoder = ae1.decode(encoded_msg=encoded_msg,
                                             msg_length=len(original_msg),
                                             probability_table=pt)
        decoded_msg = ''.join(decoded_msg)
        result = decoded_msg == original_msg
        cnt += 1
        getcontext().prec = cnt
    return len(s), cnt


def check_prec(s):
    cnt = int(math.ceil(1.71 * len(s)))
    getcontext().prec = cnt
    start = time.time()
    ae, encoded_msg, original_msg = ae_encode(s)
    pt = ae.probability_table
    ae1 = pyae.ArithmeticEncoding(frequency_table={}, save_stages=False)
    decoded_msg, ae_decoder = ae1.decode(encoded_msg=encoded_msg,
                                         msg_length=len(original_msg),
                                         probability_table=pt)
    _ = ''.join(decoded_msg)
    end = time.time()
    result = end - start
    return len(s), result