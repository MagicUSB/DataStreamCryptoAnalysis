from multiprocessing.pool import ThreadPool
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import matplotlib.pyplot as plt
from aux_coding_methods import *
from coder_methods_old import coder, decoder
import numpy as np
import concurrent.futures

# Точність обчислень для кодування (кількість знаків після коми)
# Якщо вона недостатня, то інформація не розкодується!
# TODO: обчислити залежність необхідної точності від довжини вхідних даних
getcontext().prec = 100


# TODO: поділити на окремі методи
def code_data_with_protection(*args):
    '''
    # Кодування з бакалаврської роботи
    value = int(matrix_size.get())
    coder.add_hash_to_message("Hello world!", value)
    mes, errors = decoder.get_message_and_errors(message_csv)
    showinfo(title="Test", message=mes)
    # Арифметичне кодування
    msg = csv_to_string(message_csv)
    ae, encoded_msg, original_msg = ae_encode(msg)
    pt = ae.probability_table
    ae1 = pyae.ArithmeticEncoding(frequency_table={}, save_stages=False)
    decoded_msg, ae_decoder = ae1.decode(encoded_msg=encoded_msg,
                                     msg_length=len(original_msg),
                                     probability_table=pt)
    decoded_msg = ''.join(decoded_msg)
    print("Decoded Message:  {msg}".format(msg=decoded_msg))
    print("Message Decoded Successfully? {result}".format(result=original_msg == decoded_msg))
    coded_mes = np.fromstring(decoded_msg, dtype=int, sep=' ')
    coded_mes_2d = np.reshape(coded_mes, (-1, 4))
    print(coded_mes_2d)
    final_mes, errors = decoder.decode(coded_mes_2d)
    print(final_mes)
    ae_output_file_name = 'readme.txt'
    ae_encode_write_to_file(ae.probability_table, ae_output_file_name, encoded_msg, original_msg)
    with open(ae_output_file_name) as f:
        lines = f.readlines()
        encoded_msg = decimal.Decimal(lines[0])
        length = int(lines[1])
        prob_table = json.loads(lines[2])
        print("\n\n\n")
        decoded_msg, ae_decoder = ae.decode(encoded_msg=encoded_msg,
                                            msg_length=length,
                                            probability_table=prob_table)
        decoded_msg = ''.join(decoded_msg)
        print("Decoded Message:  {msg}".format(msg=decoded_msg))
        print("Message Decoded Successfully? {result}".format(result=original_msg == decoded_msg))

    mes = "Hello"
    factor_list = list(set(factors(len(mes))))
    coder.add_hash_to_message(mes, factor_list[0])
    mes_out, errors = decoder.get_message_and_errors(message_csv)
    '''
    string_amount = 2048
    str_list = []
    for i in range(1, string_amount + 1, 20):
        str_list.append(get_random_string(N=i))
    print("Process has started!")
    result_list = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        #future_to_url = {executor.submit(check_prec, s): s for s in str_list}
        future_to_url = {executor.submit(find_min_prec, s): s for s in str_list}
        for future in concurrent.futures.as_completed(future_to_url):
            result_list.append(future.result())
            print(future.result())
    print("Process has finished!")
    result_list.sort()
    with open('for_plot.txt', 'w') as f:
        for i in result_list:
            f.write('{}\t{}\n'.format(i[0], i[1]))
    x = []
    y = []
    for i in result_list:
        x.append(i[0])
        y.append(i[1])
    plt.scatter(x, y)
    plt.xlabel('Input data size, bytes')
    #plt.ylabel('Encoding time, s')
    plt.ylabel('Decimal places')
    plt.show()


def select_file():
    global filename
    filetypes = (
        ('CSV files', '*.csv'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)

    showinfo(
        title='Selected File',
        message=filename
    )
    global message_csv
    message_csv = filename


root = Tk()
root.title("Магістерська робота")
style = ttk.Style(root)
available_styles = style.theme_names()
style.theme_use(available_styles[0])

message_csv = 'message.csv'

# TODO: додати органи управління на інтерфейс
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

ttk.Label(mainframe, text="Введіть розмірність матриці: ").grid(column=1, row=1, sticky=(W, E))
matrix_size = StringVar()
matrix_size_entry = ttk.Entry(mainframe, width=7, textvariable=matrix_size)
matrix_size_entry.grid(column=2, row=1, sticky=(W, E))

meters = StringVar()
ttk.Label(mainframe, textvariable=meters).grid(column=2, row=2, sticky=(W, E))

ttk.Button(mainframe, text="Calculate", command=code_data_with_protection) \
    .grid(column=2, row=3, sticky=W)

ttk.Label(mainframe, text="feet") \
    .grid(column=3, row=1, sticky=W)
ttk.Label(mainframe, text="is equivalent to") \
    .grid(column=1, row=2, sticky=E)

open_button = ttk.Button(mainframe, text='Open a File', command=select_file) \
    .grid(column=1, row=3, sticky=W)

for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)
file_input = ""
matrix_size_entry.focus()
root.bind("<Return>", code_data_with_protection)

root.mainloop()

# TODO: режими роботи програми:
# 1. Кодування одним методом
# 2. Кодування парою методів в різних комбінаціях
