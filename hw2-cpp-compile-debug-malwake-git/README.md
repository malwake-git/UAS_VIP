# hw2-cpp-compile-debug
Practice compiling and debugging in C++

Compile the program with the g++ command with debug flags enabled and debug the program.
When your program passes all of the tests in test.cpp you are finished. You only need
to make changes to  buggy_code.cpp


To get this code running please do the following:

1- Compile the code (type):

g++ test.cpp buggy_code.cpp -o myprogram

2- Run the program created (type):

./myprogram

3- the result (written):

starting test


testing dynamic allocation and accessor
constructing a value
calling accessor getValue to get private m_value attribute
deconstructing a class
PASS


testing static allocation and accessor/timesTwo
constructing a value
calling accessor getValue to get private m_value attribute
PASS
deconstructing a class
notice that a is automatically deleted when we leave this scope


testing arrayMax
PASS


SUCCESS!
