import concurrent.futures

import time

from coder_methods import pyae
import base64
import aux_coding_methods

# Example for encoding a simple text message using the PyAE module.
# This example only returns the floating-point value that encodes the message.
# Check the example_binary.py to return the binary code of the floating-point value.

def code_plus_decode_string(ix, st):
    pyae.prec = 2 * len(st)
    frequency_table = aux_coding_methods.get_frequency_table(st)
    AE = pyae.ArithmeticEncoding(frequency_table=frequency_table,
                                 save_stages=False)
    # print("Original Message: {msg}".format(msg=s))
    encoded_msg, encoder, interval_min_value, interval_max_value = AE.encode(msg=st,
                                                                             probability_table=AE.probability_table)
    # print("Encoded Message: {msg}".format(msg=s))
    #encoded_data_list.append((encoded_msg, len(st), AE.probability_table))
    decoded_part, decoder = AE.decode(encoded_msg=encoded_msg,
                                      msg_length=len(st),
                                      probability_table=AE.probability_table)
    # print("Decoded Message: {msg}".format(msg=decoded_msg))
    print(ix)
    return ix, "".join(decoded_part)


with open("4.png", mode="rb") as bin_file:
    original_msg = base64.b64encode(bin_file.read()).decode(encoding='utf-8')

    chunk_size = 256
    list_of_chunks = []
    step = chunk_size
    i = 0
    while i < len(original_msg):
        list_of_chunks.append(original_msg[i:i + step])
        i += step
        #step += 50
    print(len(list_of_chunks))

    t_start = time.time()
    result_list = []
    cnt = 0
    for s in list_of_chunks:
        result_list.append(code_plus_decode_string(cnt, s)[1])
        cnt += 1

    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     future_to_url = {executor.submit(code_plus_decode_string, i, list_of_chunks[i]): i for i in range(0, len(list_of_chunks))}
    #     for future in concurrent.futures.as_completed(future_to_url):
    #         result_list.append(future.result())
    #         #print(future.result())
    # result_list.sort()


    #for i in range(0, len(list_of_chunks)):
        #result_list.append(code_plus_decode_string(i, list_of_chunks[i]))

    encoded_data_list = []


    #print("Decoded Message: {msg}".format(msg=decoded_total))

    '''
    with open('test_pack.dat', mode='w') as bin_data:
        getcontext().prec = 2 * len(original_msg)
        frequency_table = aux_coding_methods.get_frequency_table(original_msg)
        AE = pyae.ArithmeticEncoding(frequency_table=frequency_table,
                                     save_stages=False)

        encoded_msg, _, _, _ = AE.encode(msg=original_msg,
                                        probability_table=AE.probability_table)
        bin_data.write(json.dumps(encoded_msg))
        bin_data.write(str(len(original_msg)))
        bin_data.write(json.dumps(frequency_table))
    '''
    t_finish = time.time()

    print("Elapsed time: {}".format(t_finish - t_start))
    decoded_total = ""
    for elem in result_list:
        decoded_total += elem[1]
    with open('4_decoded.png', 'wb') as bin_write:
        bin_write.write(base64.b64decode(decoded_total.encode(encoding='utf-8')))
    print("Message Decoded Successfully? {result}".format(result=original_msg == decoded_total))
    #print(str(AE.probability_table))
