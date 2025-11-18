#include<iostream>

typedef struct studentinfo{

	char bloodType;
	int stdNumber;
	float grade;


} StudentInfo; 

int main() {

	using namespace std;

	StudentInfo si1 = { 'O',20031128,3.5 };
	StudentInfo si2 = { 'A',20031128,2.5 };

	cout << "혈액형:" << si1.bloodType << endl;
	cout << "학번:" << si1.stdNumber << endl;
	cout << "성적:" << si1.grade << endl;

	cout << "혈액형:" << si2.bloodType << endl;
	cout << "학번:" << si2.stdNumber << endl;
	cout << "성적:" << si2.grade << endl;
	return 0;

	

}