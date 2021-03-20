// finds the max of an array
double arrayMax(double * data, int len);

// a demo class
class MyClass {
public:
	// constructor method
	MyClass(double value);

	// deconstructor method
	virtual ~MyClass();

	// accessor for get value
	double getValue();

	// multiply value by two
	double timesTwo();
private:
	// private value attribute
	double m_value;
};

// function that dynamically allocates a MyClass instance and returns the pointer to it
MyClass * makeMyClassInstance(double value);
