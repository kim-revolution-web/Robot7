#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>

// 파일의 내용을 화면에 출력하기
int main() {

	FILE* fp;
	int ch;
	char str[80];

	/*char path = "/home/robot/work/basic/chapter18/a.txt";
	fp = fopen(path, "r");*/ 

	fp = fopen("a.txt", "r");
	if (fp == NULL) {
		printf("파일이 열리지 않았습니다.\n");
		return 1;

	}
	while (1)
	{
		ch = fgetc(fp); //한글자를 가져오는 함수
		if (ch == EOF)break; //(-1)파일의 끝 

		putchar(ch); //printf("%c",ch);
	}
	
	putchar('\n');
	//rewind(fp); //처음 + EOF/에러 초기화
	fseek(fp, 0, SEEK_SET); // 처음 + EOF 초기화
	fgets(str,sizeof(str),fp);
	fputs(str,stdout);

	fclose(fp); //자원 (Resource) 반환

	return 0;
}
