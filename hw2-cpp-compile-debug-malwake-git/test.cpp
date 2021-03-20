#include "buggy_code.hpp" // use \"\" for local includes and <> for system includes

#include <iostream>
#include <assert.h>

// test data
namespace info {
	double data1[] = {1, 20, 3, 4, 5, 1, 5, 2, 1, 10, 3, 1, 5, 2, 1};
	double data2[] = {1, 2, 3, 4, 5, 1, 5, 2, 1, 1, 3, 1, 5, 2, 1};
}

double data1[] = {1, 2, 3, 4, 5, 1, 5, 2, 1, 10, 3, 1, 5, 2, 1};

int test() {
	std::cout << "starting test" << std::endl;
	// we will create a new scope for each test with curly braces

	{
		std::cout << "\n\ntesting dynamic allocation and accessor" << std::endl;
		MyClass * a = makeMyClassInstance(20);
		// you shoud allocate your class instance here using the new command
		std::cout << "calling accessor getValue to get private m_value attribute" << std::endl;
		assert(a->getValue() == 20);
		// make sure you delete what you dynamically allocate
		delete a;
		std::cout << "PASS" << std::endl;
	}

	{
		std::cout << "\n\ntesting static allocation and accessor/timesTwo" << std::endl;
		MyClass a(100);
		std::cout << "calling accessor getValue to get private m_value attribute" << std::endl;
		assert(a.getValue() == 100);
		assert(a.timesTwo() == 200);
		std::cout << "PASS" << std::endl;
	}
	std::cout << "notice that a is automatically deleted when we leave this scope" << std::endl;

	{
		std::cout << "\n\ntesting arrayMax" << std::endl;
		assert(arrayMax(info::data1, 15) == 20);
		assert(arrayMax(info::data2, 15) == 5);
		assert(arrayMax(data1, 15) == 10);
		std::cout << "PASS" << std::endl;
	}

	std::cout << "\n\nSUCCESS!" << std::endl;
	return 0;
}

int main() {
	test();
}
