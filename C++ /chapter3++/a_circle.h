//#indef _CIRCLE_H_
//#define _CIRCLE_H_

#pragma once

class Circle {

private:
	int radius;

public:
	Circle();
	Circle(int r);
	double getArea();
};