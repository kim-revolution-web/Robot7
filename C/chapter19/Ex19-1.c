#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include "point.h"

int main() {

	printf("Ã¹ ÁÂÇ¥ Gpoint =(%d,%d)\n", Gpoint.x, Gpoint.y);
	Gpoint.x = 10;
	Gpoint.y = 20;
	printf("º¯È¯ ÁÂÇ¥ Gpoint =(%d,%d)\n", Gpoint.x, Gpoint.y);

	return 0;
};