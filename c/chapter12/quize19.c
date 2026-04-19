#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <string.h>

int main() {
	int i;
	char str[10]; 
	
	fgets(str,sizeof(str), stdin);
	int len = strlen(str);
	//scanf("%s", str);
	
	printf("%d\n", len);
	
		for (i=len; i>=0; i--) {
			puts(str[i]);
			//printf("%c", str[i]);
		}

	return 0;
}
