
    #!/bin/bash
    # Generator of random files
    for value in {1..10000}
    do
    head -c $value </dev/urandom >$value.txt
    done
    echo All done
    # Record time of arithmetic coding
    truncate -s 0 times_x.txt
    truncate -s 0 times_y.txt
    TIMEFORMAT=%R
    for value in {1..1000}
    do
    echo $value >>times_x.txt
    (time ./ArithmeticCompress $value.txt $value.dat 2>sleep.stderr) 2>>times_y.txt
    done
    echo All done
    unset TIMEFORMAT

