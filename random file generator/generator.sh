#!/bin/bash
# Generator of random files
for value in {1..1000001..50}; do
    head -c $value </dev/urandom >$value.txt
done
echo "All done"
# Record time of arithmetic coding
truncate -s 0 times_x.txt
truncate -s 0 times_y_cpp.txt
truncate -s 0 times_y_python.txt
TIMEFORMAT=%R
for value in {1..1000001..50}; do
    echo $value >>times_x.txt
    (time ./ArithmeticCompress $value.txt $value.dat 2>sleep.stderr) 2>>times_y_cpp.txt
    (time python3.10 arithmetic-compress.py $value.txt $value.dat 2>sleep.stderr) 2>>times_y_python.txt
    rm $value.txt $value.dat
done
echo "All done"
unset TIMEFORMAT
