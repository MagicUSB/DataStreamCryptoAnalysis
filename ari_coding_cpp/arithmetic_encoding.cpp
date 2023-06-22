#include <pybind11/pybind11.h>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
#include "ArithmeticCoder.hpp"
#include "BitIoStream.hpp"
#include "FrequencyTable.hpp"

namespace py = pybind11;

using std::uint32_t;

int add(int i, int j) {
    return i + j;
}

int encode(char* inputFile, char* outputFile) {
    // Read input file once to compute symbol frequencies
	std::ifstream in(inputFile, std::ios::binary);
	SimpleFrequencyTable freqs(std::vector<uint32_t>(257, 0));
	freqs.increment(256);  // EOF symbol gets a frequency of 1
	while (true) {
		int b = in.get();
		if (b == std::char_traits<char>::eof())
			break;
		if (b < 0 || b > 255)
			throw std::logic_error("Assertion error");
		freqs.increment(static_cast<uint32_t>(b));
	}

	// Read input file again, compress with arithmetic coding, and write output file
	in.clear();
	in.seekg(0);
	std::ofstream out(outputFile, std::ios::binary);
	BitOutputStream bout(out);
	try {

		// Write frequency table
		for (uint32_t i = 0; i < 256; i++) {
			uint32_t freq = freqs.get(i);
			for (int j = 31; j >= 0; j--)
				bout.write(static_cast<int>((freq >> j) & 1));  // Big endian
		}

		ArithmeticEncoder enc(32, bout);
		while (true) {
			// Read and encode one byte
			int symbol = in.get();
			if (symbol == std::char_traits<char>::eof())
				break;
			if (!(0 <= symbol && symbol <= 255))
				throw std::logic_error("Assertion error");
			enc.write(freqs, static_cast<uint32_t>(symbol));
		}

		enc.write(freqs, 256);  // EOF
		enc.finish();  // Flush remaining code bits
		bout.finish();
        std::cout << "Encoding has finished!" << std::endl;
		return EXIT_SUCCESS;

	} catch (const char *msg) {
		std::cerr << msg << std::endl;
		return EXIT_FAILURE;
	}
}

int decode(char* inputFile, char* outputFile) {
	// Perform file decompression
	std::ifstream in(inputFile, std::ios::binary);
	std::ofstream out(outputFile, std::ios::binary);
	BitInputStream bin(in);
	try {

		// Read frequency table
		SimpleFrequencyTable freqs(std::vector<uint32_t>(257, 0));
		for (uint32_t i = 0; i < 256; i++) {
			uint32_t freq = 0;
			for (int j = 0; j < 32; j++)
				freq = (freq << 1) | bin.readNoEof();  // Big endian
			freqs.set(i, freq);
		}
		freqs.increment(256);  // EOF symbol

		ArithmeticDecoder dec(32, bin);
		while (true) {
			uint32_t symbol = dec.read(freqs);
			if (symbol == 256)  // EOF symbol
				break;
			int b = static_cast<int>(symbol);
			if (std::numeric_limits<char>::is_signed)
				b -= (b >> 7) << 8;
			out.put(static_cast<char>(b));
		}
		return EXIT_SUCCESS;

	} catch (const char *msg) {
		std::cerr << msg << std::endl;
		return EXIT_FAILURE;
	}
}


PYBIND11_MODULE(arithmetic_encoding, m) {
    m.doc() = "pybind11 example plugin"; // optional module docstring

    m.def("add", &add, "A function that adds two numbers");
    m.def("encode", &encode, "Performs arithmetic encoding of contents of the input file");
    m.def("decode", &decode, "Performs arithmetic decoding (decompression) of contents of the input file");
}
