//txt 회원가입을해 구조체로 해서 ->텍스로 저장해 
/// 로그인할때 덱스랑 맞는지 비교해
//관리자 가 볼 휴대 번호 중간을 X표를 만들고 
// 주민등록 뒷자리는 첫짜리만 보이게

typedef struct Privet {
	char name[20];
	int number;  //xxx - xxxx - xxxx char?
	int RRN;// xxxxxx-xxxxxxx
	char adress[30];
	char adress_After[30];

		//정보를 따로 받아?전부 나눠서 받는게 편할듯
}pv;

#include<stdio.h>

int main() {


	FILE* fp[100];
	char buf[100];
	char* str;
	int i = 0;
	pv cus[100];

	for()//for문으로 하나 줘? fgets로 나눠서 줘?
	cus->name[i];
	cus->number[i];
	cus->RRN[i];
	cus->adress[i];
	cus->adress_After[i];
	

	




	//회원가입해서 텍스트에 저장하고 싶어
	for (i = 0; i < 100; i++) {
		pv pri[i]; // 여러개 필요하니까
	}
	

	for (i = 0; i < 100; i++)// 포인트에 사이즈면 8bie정도?
	{


		fp[i] = fopen(i.txt, "r+"); //텍스트 이름을 바꿔서 어려개 저장하고 싶어
		//r+로 결정   나중에 열기도 할꺼니까 a+가 좋은가? 중간부터 고치수 있게 R+? 


		str = fgets(buf, sizeof(buf), stdin);
		//개체 정보랑 똑같은게 있는지도 비교해야해
		
		
		//입력 정보가 있을때만 입력 
		if (str != NULL) {

			//객체써서 있는 형식 대로 입력되기

			//화면에 입력도 뜨면서 파일에 도 써야지

			fprintf(fp[i], "%99s", str);
			fputs(fp[i], stdout);//파일에 쓰여진걸 출력
		}
	}


	return 0;
};
