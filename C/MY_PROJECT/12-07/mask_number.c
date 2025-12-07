#include<stdio.h>
#include<string.h>


//void mask_number(char* dst, const char* src) {
//	int i = 0;
//	if (src == NULL) {
//		dst[0] = '\0';
//		printf("mask NULL");
//		return;
//	}
//	for (i = 0; src[i] != '\0'; i++) {
//		dst[i] = src[i];
//	}
//	dst[i] = '\0';
//
//	//배열방식
//	//010-4567-9012
//	for (i = 4; i < 8 && dst[i] != '\0'; i++) {
//		if (dst[i] != '-')dst[i] = 'X';
//	}
//}

//void mask_number(char* dst, size_t dst_size,
//	const char* src)
//{
//
//	char buf_num[14];
//	char* con = NULL;
//	char* first;
//	char* last;
//	if (src == NULL || dst_size <0) {
//		dst[0] = '\0';
//		printf("maks return\n");
//		return;
//	}
//
//	strcpy_s(buf_num, dst_size, src);
//	first = strtok_s(buf_num, "-", &con);
//	strtok_s(NULL, "-", &con);
//	last = strtok_s(NULL, "-", &con);
//
//	if (!first || !last) {
//		dst[0] = '\0';
//		return;
//	}
//	sprintf_s(dst,dst_size,"%s-XXXX-%s", first, last);
//	
//}



void mask_number(char* dst, size_t dst_size, char* src) {

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

		char* con = NULL;
		file_id = strtok_s(str, "|", &con); //id;
		file_pd = strtok_s(NULL, "|", &con);//pd
		file_name = strtok_s(NULL, "|", &con); //name
		file_number = strtok_s(NULL, "|", &con);//number
		file_rrn = strtok_s(NULL, "|", &con); //rrn
		if (file_number == NULL || file_rrn == NULL) {
			continue;
		}

		mask_number(masked_number, sizeof(masked_number), file_number);
		//mask_rrn(masked_rrn, file_rrn);
		fputs(file_id, stdout);
		fputs(file_pd, stdout);
		fputs(file_name, stdout);
		fputs(masked_number, stdout);

		getchar();//enter 키로한줄씩 뽑기

		//putchar('\n');

		//fprint 가 더 좋지 않나?

		//mask_rrn(masked_rrn, file_rrn);
		//fputs(masked_rrn, stdout);
	}
	fclose(fpr);
}