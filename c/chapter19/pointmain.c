#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include "point.h"

int main() {

	printf("첫 좌표 Gpoint =(%d,%d)\n", Gpoint.x, Gpoint.y);
	Gpoint.x = 10;
	Gpoint.y = 20;
	printf("변환 좌표 Gpoint =(%d,%d)\n", Gpoint.x, Gpoint.y);

	return 0;
};
