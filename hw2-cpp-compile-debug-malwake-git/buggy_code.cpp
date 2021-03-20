#include "buggy_code.hpp"
#include <iostream>

///
// This is a simple exercise to test your ability to use the GDB debugger to find errors in the program below.

// array max
double arrayMax(double * data, int len) {
	double maxVal = data[0];
	for (int i=0; i<len; i++) {
		if (data[i] > maxVal) {
			maxVal = data[i];
		}
	}
	return maxVal;
}

MyClass::MyClass(double value) {
	m_value = value;
	std::cout << "constructing a value" << std::endl;
}

MyClass::~MyClass() {
	std::cout << "deconstructing a class" << std::endl;
}

double MyClass::getValue() {
	// should return m_value
	return m_value;
}

double MyClass::timesTwo() {
	// should multiply the class value times 2
	return m_value*2;
}

MyClass * makeMyClassInstance(double value) {
	// should dynamically allocate a MyClass instance using the new command with passed value
	// from this function
  MyClass * a =new MyClass(value);
	return a;
}
