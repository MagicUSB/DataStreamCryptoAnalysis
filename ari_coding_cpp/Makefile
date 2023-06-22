arithmetic_encoding.so: ArithmeticCoder.o BitIoStream.o FrequencyTable.o arithmetic_encoding.o
    g++ -shared -o example.so neat.o network.o nnode.o link.o trait.o gene.o innovation.o organism.o species.o genome.o population.o example.o

ArithmeticCoder.o: ArithmeticCoder.cpp ArithmeticCoder.hpp
    g++ -c -O3 -Wall -fPIC ArithmeticCoder.cpp

BitIoStream.o: BitIoStream.cpp BitIoStream.hpp
    g++ -c -O3 -Wall -fPIC BitIoStream.cpp

FrequencyTable.o: FrequencyTable.cpp FrequencyTable.hpp
    g++ -c -O3 -Wall -fPIC FrequencyTable.cpp

arithmetic_encoding:
    g++ -O3 -Wall -std=c++11 -fopenmp `python3 -m pybind11 --includes` -fPIC -c arithmetic_encoding.cpp

clean:
    rm *.o *.so
