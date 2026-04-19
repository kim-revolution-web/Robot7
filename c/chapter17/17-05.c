#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

//구조체를 반환하여 두 변수의 값 교환

struct vision
{

	double left;
	double right;
};

struct vision exchang(struct vision robot);
int main() {

	struct vision robot;

	printf("시력 입력 : ");
	scanf("%lf%lf", &(robot.left), &(robot.right));
	robot = exchang(robot);
	printf("바뀐 시력 : %.1lf %.1lf",robot.left,robot.right);
	return 0;
}

struct vision exchang(struct vision robot) {

	double temp;

	temp = robot.left;
	robot.left = robot.right;
	robot.right = temp;

	return robot;
}
