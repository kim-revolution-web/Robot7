#define _CRT_SECURE_NO_WARNINGS
#include<stdio.h>
#include<string.h>
// 파일의 내용을 화면에 출력하기
int main() {

	FILE* rfp, * afp;
	int rh, ah;
	char str[80];
	int i = 0;


	rfp = fopen("biznesscard.txt", "r"); // 읽기
	afp = fopen("biznesscard.txt", "a+"); //읽거나 파일의 끝에 추가하기위해 개방


	if (rfp == NULL) {
		printf("읽기 파일이 열리지 않았습니다.\n");
		return 1;
	}

	if (afp == NULL) {
		printf("읽기 파일이 열리지 않았습니다.\n");
		return 1;
	}
	printf("번호를 입력하세요\n");
	scanf("%d", &i);


	while (1)
	{

		switch (i) {

		case 1:
			rh = fgetc(rfp);
			if (rh == EOF)break;
			putchar(rh);
			break;

		case 2:

			printf("이름 :");
			scanf("%s", str);
			str[strcspn(str, "\r\n")] = '\0';
			if (strcmp(str, "end") == 0)
			{
				break;
			}
			else if (strcmp(str, "list") == 0)
			{
				fseek(afp, 0, SEEK_SET);
				while (1)
				{
					fgets(str, sizeof(str), afp);

					if (feof(afp))
					{
						break;
					}
					printf("%s", str);
				}
			}
			else {
				fprintf(afp, "%s\n", str);
			}
			
		}
		break;
	}




	fclose(afp);
	fclose(rfp);



	return 0;
}