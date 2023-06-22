cmake_minimum_required(VERSION 3.4...3.18)
project(arithmetic_encoding LANGUAGES CXX)

add_subdirectory(pybind11)
pybind11_add_module(arithmetic_encoding arithmetic_encoding.cpp)
target_link_libraries(arithmetic_encoding PRIVATE pybind11::module pybind11::lto)

pybind11_extension(arithmetic_encoding)
