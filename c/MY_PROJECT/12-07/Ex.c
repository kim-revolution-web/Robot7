#include<stdio.h>
#include<string.h>

typedef struct Privet {
	char id[20];
	char pd[20];
	char name[20];
	char number[14];  //xxx - xxxx - xxxx char?
	char RRN[15];// xxxxxx-xxxxxxx
	char adress[30];
	char adress_After[30];


}pv;
pv cus;
void read_stdin(char* buf, int size)//size_t size
{
	int ch = 0;
	int i = 0;
	if (size <= 0) { printf("stdin 반환"); return; };

	if (fgets(buf, size, stdin) == NULL) {
		buf[0] = '\0';   // EOF 등 실패 시 안전하게 비워두기
		return;
	}
	i = strcspn(buf, "\r\n");

	if (buf[i] == '\r' || buf[i] == '\n') {

		buf[i] = '\0';
	}
	else {
		while ((ch = getchar()) != '\n' && ch != EOF) {
			//전부버려 개행 전까지 
		}
	}
}




void sign_up(void) {
	FILE* fpa;


	if (fopen_s(&fpa, "i.txt", "a+") != 0 || fpa == NULL) {
		printf("파일이 열지 못함");
		return;

	}
	//str = fgets(buf, sizeof(buf), stdin);

	printf("ID : ");
	//scanf_s("%19s", cus.id, (unsigned)sizeof(cus.id));
	//fgets(cus.id, sizeof(cus.id), stdin);
	read_stdin(cus.id, sizeof(cus.id));

	printf("PW : ");
	//scanf_s("%19s", cus.pd, (unsigned)sizeof(cus.pd));
	//fgets(cus.pd, sizeof(cus.pd), stdin);
	read_stdin(cus.pd, sizeof(cus.pd));

	printf("이름 : ");
	//scanf_s("%19s", cus.name, (unsigned)sizeof(cus.name));
	//fgets(cus.name, sizeof(cus.name), stdin);
	read_stdin(cus.name, sizeof(cus.name));

	printf("전화번호(010-1234-5678) 형식에 맞게 써주세요 : ");
	//scanf_s("%13s", cus.number, (unsigned)sizeof(cus.number));
	//fgets(cus.number, sizeof(cus.number), stdin);
	read_stdin(cus.number, sizeof(cus.number));

	printf("주민번호(000000-0000000)형식에 맞게 써주세요 : ");
	//scanf_s("%14s",cus.RRN, (unsigned)sizeof(cus.RRN));
	//fgets(cus.RRN, sizeof(cus.RRN), stdin);
	read_stdin(cus.RRN, sizeof(cus.RRN));

	printf("주소 : ");
	//scanf_s("%29s", cus.adress, (unsigned)sizeof(cus.adress));
	//fgets(cus.adress, sizeof(cus.adress), stdin); //scnaf_s \n 버퍼가 남아서 못씀
	read_stdin(cus.adress, sizeof(cus.adress));

	printf("상세 주소 : ");
	//scanf_s("%29s",cus.adress_After, (unsigned)sizeof(cus.adress_After));
	//fgets(cus.adress_After, sizeof(cus.adress_After), stdin);
	read_stdin(cus.adress_After, sizeof(cus.adress_After));

	fprintf(fpa, "%s|%s|%s|%s|%s|%s|%s\n",
		cus.id, cus.pd, cus.name, cus.number, cus.RRN,
		cus.adress, cus.adress_After);

	fclose(fpa);


}

void login() {
	char login_id[20] = { 0 };
	char login_pd[20] = { 0 };
	FILE* fpr;
	errno_t rfp;
	char str[100];
	char* file_id;
	char* file_pd;
	int longin_flag = 0;
	

	printf("ID 입력:");
	scanf_s("%19s", login_id, (unsigned)sizeof(login_id));
	printf("pass ward 입력:");
	scanf_s("%19s", login_pd, (unsigned)sizeof(login_pd));
	rfp = fopen_s(&fpr, "i.txt", "r");
	if (rfp != 0 || fpr == NULL) {
		printf("파일이 열리지 않음");
		return;
	}
	while (fgets(str, sizeof(str), fpr) != NULL)// 한줄씩일기
	{
		str[strcspn(str, "\n")] = '\0';
		char* context = NULL;
		file_id = strtok_s(str, "|", &context);
		file_pd = strtok_s(NULL, "|", &context);
		if (file_id == NULL || file_pd == NULL) {
			continue;// 잘못된 줄이면 그냥 넘어감
		}

		printf("id %s\n", file_id);
		printf("pd %s\n", file_pd);
		if (strcmp(login_id, file_id) == 0 &&
			strcmp(login_pd, file_pd) == 0)
		{
			printf("로그인 성공\n");
			longin_flag = 1;
			break;
		}
	}
	if (longin_flag != 1)
	{
		printf("로그인 실패\n");
	}
	fclose(fpr);

}

int main() {

	int menu;

	while (1) {
		printf("1. 회원가입\n");
		printf("2. 로그인\n");
		printf("3. 종료\n");
		scanf_s("%d", &menu);
		int ch;
		while ((ch = getchar()) != '\n' && ch != EOF) {}

		if (menu == 1) {
			sign_up();
		}
		else if (menu == 2) {
			login();
		}
		else if (menu == 3) {
			break;
		}
		else {
			printf("잘못된 입력\n");
		}
	}



	return 0;
};
