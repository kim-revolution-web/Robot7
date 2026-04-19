#include <iostream>
#include <string>
using namespace std;

int main()
{
    string s;
    cout << "여러 줄의 문자열을 입력하세요. 입력의 끝은 &문자입니다." << endl;

    // & 문자가 나올 때까지 입력을 읽어 s에 저장
    // & 문자 자체는 버려지고 s에는 들어가지 않는다.
    getline(cin, s, '&');

    // 위에서 엔터('\n')가 버퍼에 남아 있으므로 한 글자를 버린다.
    cin.ignore();

    string f, r;
    cout << endl << "find:";
    getline(cin, f, '\n');    // 한 줄 전체 입력 (그냥 getline(cin, f); 와 같다)
    cout << "replace:";
    getline(cin, r, '\n');

    int startIndex = 0;
    while (true) {
        // s에서 startIndex 위치부터 f를 찾는다.
        int fIndex = s.find(f, startIndex);

        // 더 이상 못 찾으면 루프 종료
        if (fIndex == -1)    // 실제로는 string::npos를 쓰는 게 더 안전
            break;

        // fIndex 위치부터 f.length() 글자만큼 r로 교체
        s.replace(fIndex, f.length(), r);

        // 방금 교체한 r의 바로 다음 위치부터 다시 검색
        startIndex = fIndex + r.length();
    }

    cout << s << endl;

    return 0;
}