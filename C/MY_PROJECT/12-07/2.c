#include<stdio.h>
#include<string.h>
//구조체 활용이 되고 있는건가?
// 부

 typedef enum  {id,pd,name,number,
	RRN,adress,adress_after}What;

typedef struct Privet
{
	char ID[20];
	char PASSWARD[20];
	char NAME[20];
	char NUMBER[14]; //010-1234-1234;
	char RRN[15]; //123456-1234567;
	char ADRESS[50];
	char ADRESS_AFTER[50];

}privet;

privet pv;
What what;



//만든 함수
void read_stdin(char* buf, int size) {
	int ch = 0;
	int i = 0;

	//오류제거 
	if (size <= 0) { printf("size가 없다"); return; }
	//fgets  오류 NULL
	if (fgets(buf, size, stdin) == NULL)
	{
		buf[0] = '\0';
		printf("입력이 없네");
		return;
	}
	//fgets에 \n\0 들어가는데 \n 지우기 
	i = (int)strcspn(buf, "\r\n");
	if (buf[i] == '\r' || buf[i] == '\n')
	{
		buf[i] = '\0';
	}
	//버퍼보다 큰거 지우고 버퍼에 남는 \n 지우기
	else {
		while ((ch = getchar()) != '\n' && ch != EOF) {}
	}
}

	void mask_number(char* dst, size_t dst_size, char* src)
	{

		if (dst == NULL || dst_size == 0 || src == NULL) {
			if (dst != NULL && dst_size > 0) {
				dst[0] = '\0';   // 최소한 빈 문자열로 세팅
			}
			printf("mask 반사\n");
			return;
		}

		strcpy_s(dst, dst_size, src);
		//dst[dst_size - 1] = '\0';

		char* p = strchr(dst, '-');
		if (!p)return;
		p++;

		for (int i = 0; *p && i < 4; i++) {
			if (*p != '-') *p = 'X';
			p++;
		}
	}

	void mask_rrn(char* dst, const char* src) {
		int i = 0;
		
		if (dst == NULL) return;

			if (src== NULL) {
				dst[0] = '\0';
				printf("mask_rrn");
				return;
			}
		
		for (i = 0; src[i] != '\0'; i++) {
			dst[i] = src[i];
		}
		dst[i] = '\0';
	
		//012345-7890123
		for (i = 8; dst[i] != '\0'; i++) {
			dst[i] = 'X';
		}
	}
	//파일열어서 원하는 id,pd묶음으로 전달해주기
	//전역 변수에 넣어서 값을 줘야하나?
	void read_file(char *find,size_t find_size,int buf) {
		char str[256];
		char* efile_id;
		char* efile_pd;
		char* efile_name; 
		char* efile_number;
		char* efile_RRN;

		char save_id[256] = { 0 };
		char save_pd[256] = { 0 };
		char save_name[256] = { 0 };
		char save_number[256] = { 0 };
		char save_RRN[256] = { 0 };


		
		if (find == NULL||find_size==0) {
			printf("my_exists 반사");
			return;
		}

		FILE *fpr;
		if (fopen_s(&fpr,"i.txt","r") != 0 || fpr == NULL) {
			printf("my_exists 파일 판사");
			find[0]='\0';
			return;
			}
		while (fgets(str, sizeof(str), fpr) != NULL) {
			str[strcspn(str, "\r\n")] = '\0';

			char* con=NULL;
			efile_id = strtok_s(str, "|", &con);//id
			efile_pd = strtok_s(NULL, "|", &con);//pd
			efile_name = strtok_s(NULL, "|", &con); //name
			efile_number = strtok_s(NULL, "|", &con); //number
			efile_RRN = strtok_s(NULL, "|", &con); //rrn
			if(!efile_id||!efile_pd||efile_name==NULL||
				efile_number==NULL|| efile_RRN==NULL)
			{continue;}
			
			size_t len_id=strlen(save_id);
			sprintf_s(save_id+len_id, sizeof(save_id)-len_id, "%s|", efile_id);//여기서 모든id저장
			size_t len_pd = strlen(save_pd);
			sprintf_s(save_pd+len_pd, sizeof(save_pd)-len_pd, "%s|", efile_pd);
			size_t len_name = strlen(save_name);
			sprintf_s(save_name + len_name, sizeof(save_name) - len_name, "%s|", efile_name);
			size_t len_number = strlen(save_number);
			sprintf_s(save_number+len_number,sizeof(save_number)-len_number, "%s|", efile_number);
			size_t len_RRN = strlen(save_RRN);
			sprintf_s(save_RRN + len_RRN, sizeof(save_RRN) - len_RRN, "%s|", efile_RRN);
		}

		if (buf == id) {
			strcpy_s(find, find_size, save_id); //id라고 적히면 id전달
		}
		if (buf == pd) {
			strcpy_s(find, find_size, save_pd); 
		}
		if (buf ==name ) {
			strcpy_s(find, find_size, save_name); 
		}
		if (buf == number) {
			strcpy_s(find, find_size, save_number); 
		}
		if (buf == RRN) {
			strcpy_s(find, find_size, save_RRN); 
		}
		//*
		fclose(fpr);
	}

	int my_exists(char* find,int buf) {
		char str[100] = { 0 };
		read_file(str,sizeof(str), buf);//구조체에 저장한 id
		char* con = NULL;
		char *same = strtok_s(str,"|", &con);
		
		while (same != NULL) {
			if (strcmp(find, same) == 0) {
				
				return 1;
			}
			same = strtok_s(NULL, "|", &con);
		}
	}

	//회원가입
	void sign_up() {
		
		FILE* fpa; //파일 닫아주기

		printf("ID 입력 ");
		read_stdin(pv.ID, sizeof(pv.ID));

		if (my_exists(pv.ID,id)) {
			printf("중복된 ID\n");
			return ;
		}

		printf("PASSWARD 입력 ");
		read_stdin(pv.PASSWARD, sizeof(pv.PASSWARD));
		printf(" NAME 입력 ");
		read_stdin(pv.NAME, sizeof(pv.NAME));

		printf("NUMBER 입력 010-1234-1234 형식 맞추기");
		read_stdin(pv.NUMBER, sizeof(pv.NUMBER));

		if (my_exists(pv.NUMBER,number)) {
			printf("중복된 number\n");
			return;
		}


		printf("RRM 입력 123456-1234567 형식 맞추기");
		read_stdin(pv.RRN, sizeof(pv.RRN));
		printf("ADRESS 입력 ");
		read_stdin(pv.ADRESS, sizeof(pv.ADRESS));
		printf("ADRESS_AFTER 입력 ");
		read_stdin(pv.ADRESS_AFTER, sizeof(pv.ADRESS_AFTER));

		//오류 제거
		//fopen_s 정상 0반환 FILE 오류 NULL
		if (fopen_s(&fpa, "i.txt", "a+") != 0 || fpa == NULL)
		{
			printf("파일이 열리지 않았다");
			return;
		}
		
		//fputs
		fprintf(fpa, "%s|%s|%s|%s|%s|%s|%s\n",
			pv.ID, pv.PASSWARD, pv.NAME, pv.NUMBER,
			pv.RRN, pv.ADRESS, pv.ADRESS_AFTER);
		//*
		fclose(fpa);
	}

	//로그인
	void login() {


		//로그인 입력
		char logid[20] = { 0 };
		char logpd[20] = { 0 };
		//파일 비교
		char str[256];//pv가 너무 큼
		char* con = NULL; //중복
		char* pv_id = NULL;
		char* pv_pd = NULL;
		int flag = 0;

		//파일 닫아주기
		FILE* fpr; //파일열때
		//fopen_s 정상 0 반환 FILE 오류 NULL
		if (fopen_s(&fpr, "i.txt", "r") != 0 || fpr == NULL)
		{
			printf("login 파일열기 실패");
			return;
		}
		//아이디 입력
		printf("ID 입력:");
		read_stdin(logid, sizeof(logid));
		printf("PASS WARARD 입력:");
		read_stdin(logpd, sizeof(logpd));

		//파일에서 찾기 반복해서 찾아야함 
		while (fgets(str, sizeof(str), fpr) != NULL) {
			str[strcspn(str, "\r\n")] = '\0';
			//파일로 열었으니까 stdin 처럼 \n버퍼에 없나?
			//줄 마다 초기화
			char* con = NULL;
			pv_id = strtok_s(str, "|", &con);
			pv_pd = strtok_s(NULL, "|", &con);
			//건너뛰기
			if (pv_id == NULL || pv_pd == NULL) {
				continue;
			}
			//비교성공
			if (strcmp(logid, pv_id) == 0
				&& strcmp(logpd, pv_pd) == 0)
			{
				printf("LOGIN\n");
				flag = 1;
				//반복문이라 나가야함 
				break;

			}
		}
		//비교 실패 여러번 실패 하니까 while문 밖으로
		if (flag != 1) {
			printf("LOGIN FAIL\n");
		}
		//*
		fclose(fpr);
	}

	void find_id() {
		FILE* fpr = NULL;
		char str[256] = { 0 };

		char* file_id;
		char* file_pd;
		char* file_name;
		char* file_number;
		char* file_RRN;

		char find_name[20];
		char find_number[14];
		char find_RRN[15];

		int i = 0;

		if (fopen_s(&fpr, "i.txt", "r") != 0 || fpr == NULL) {
			printf("회원정보를 못찾음");
			return;
		}
		printf("name 입력:");
		read_stdin(find_name, sizeof(find_name));
		printf("number 입력:");
		read_stdin(find_number, sizeof(find_number));
		printf("RRN 입력:");
		read_stdin(find_RRN, sizeof(find_RRN));

		while (fgets(str, sizeof(str), fpr) != NULL)
		{
			str[strcspn(str, "\r\n")] = '\0';

			char* con = NULL;//변수
			file_id = strtok_s(str, "|", &con);//id
			file_pd = strtok_s(NULL, "|", &con);//pd
			file_name = strtok_s(NULL, "|", &con); //name
			file_number = strtok_s(NULL, "|", &con); //number
			file_RRN = strtok_s(NULL, "|", &con); //rrn

			if (file_name == NULL || file_number == NULL ||
				file_RRN == NULL)
			{
				continue;
			}

			if (strcmp(file_name, find_name) == 0 &&
				strcmp(file_number, find_number) == 0 &&
				strcmp(file_RRN, find_RRN) == 0)
			{
				printf("찾은 id :\n");
				fputs(file_id, stdout);
				printf("찾은 pd :\n");
				fputs(file_pd, stdout);
				i = 1;
				break;
			}
		}
		if (i != 1) {
			printf("find 실패");
		}
		fclose(fpr);
	}

	void admin_list() {

		FILE* fpr = NULL;
		char str[256] = { 0 };

		char* file_id;
		char* file_pd;
		char* file_name;
		char* file_number;
		char* file_rrn;

		char masked_number[14];
		char masked_rrn[15];

		//파일 열기
		if (fopen_s(&fpr, "i.txt", "r") != 0 || fpr == NULL) {
			printf("admin FILE");
			return;
		}
		while (fgets(str, sizeof(str), fpr) != NULL) {
			
			str[strcspn(str, "\r\n")] = '\0';
			//fputs(str, stdout);
			char* con = NULL;
			file_id = strtok_s(str, "|", &con); //id;
			file_pd = strtok_s(NULL, "|", &con);//pd
			file_name = strtok_s(NULL, "|", &con); //name
			file_number = strtok_s(NULL, "|", &con);//number
			file_rrn = strtok_s(NULL, "|", &con); //rrn
			if (file_number == NULL || file_rrn == NULL||
				file_id == NULL || file_pd == NULL || 
				file_name == NULL) continue;
			

			mask_number(masked_number, sizeof(masked_number),
				file_number);
			mask_rrn(masked_rrn, file_rrn);

			//fputs(file_id, stdout);
			////putchar('|');
			//fputs(file_pd, stdout);
			//fputs(file_name, stdout);
			//fputs(masked_number, stdout);
			//fputs(masked_rrn, stdout);
			//getchar();//enter 키로한줄씩 뽑기
			//putchar('\n');

			fprintf(stdout, "%s|%s|%s|%s|%s\n",
				file_id, file_pd, file_name, masked_number,
				masked_rrn);
			//fprint 가 더 좋지 않나?

			
			
		}
		fclose(fpr);
	}

	int main() {
		int manu;
		int ch = 0;
		while (1) {
			printf("1.회원가입\n");
			printf("2.로그인\n");
			printf("3.ID,PW 찾기\n");
			printf("4.관리자모드(회원 목록 보기)\n");
			printf("5.종료\n");
			scanf_s("%d", &manu);
			while ((ch = getchar()) != '\n' && ch != EOF) {}

			if (manu == 1) {
				sign_up();
			}
			else if (manu == 2) {
				login();
			}
			else if (manu == 3) {
				find_id();
			}
			else if (manu == 4) {
				admin_list();
			}
			else if (manu == 5) {
				break;
			}
			else {
				printf("잘못된 입력입니다");

			}
		}




		return 0;
	}