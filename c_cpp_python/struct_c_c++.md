좋아. struct는 여러 개의 관련된 데이터를 한 덩어리로 묶는 것이야.

예를 들어 사람 정보가 있으면

이름

나이

키

이걸 따로따로 변수 3개로 두는 대신
사람이라는 한 묶음으로 만들 수 있어.

1. C 버전 struct 기본
가장 기본 형태
#include <stdio.h>

struct Person {
    char name[20];
    int age;
    float height;
};

int main() {
    struct Person p1;

    p1.age = 20;
    p1.height = 175.5f;

    printf("나이: %d\n", p1.age);
    printf("키: %.1f\n", p1.height);

    return 0;
}
뜻
struct Person {
    char name[20];
    int age;
    float height;
};

이건 Person이라는 설계도를 만든 거야.

안에는

name

age

height

이 들어감.

사용법
struct Person p1;

이건 Person 구조체 변수 p1을 만든 거야.

즉:

자료형: struct Person

변수명: p1

멤버 접근
p1.age = 20;
p1.height = 175.5f;

. 점으로 안의 값에 접근해.

이걸 멤버 접근 연산자라고 해.

2. C 버전 문자열까지 넣은 예제
#include <stdio.h>
#include <string.h>

struct Person {
    char name[20];
    int age;
};

int main() {
    struct Person p1;

    strcpy(p1.name, "Kim");
    p1.age = 25;

    printf("이름: %s\n", p1.name);
    printf("나이: %d\n", p1.age);

    return 0;
}
왜 strcpy를 쓰냐

C에서 char name[20] 은 문자열 배열이라서

이렇게는 안 돼:

p1.name = "Kim";   // X

그래서 복사해야 해:

strcpy(p1.name, "Kim");
3. C 버전 여러 개 만들기
#include <stdio.h>
#include <string.h>

struct Student {
    char name[20];
    int score;
};

int main() {
    struct Student s1, s2;

    strcpy(s1.name, "Lee");
    s1.score = 90;

    strcpy(s2.name, "Park");
    s2.score = 85;

    printf("%s %d\n", s1.name, s1.score);
    printf("%s %d\n", s2.name, s2.score);

    return 0;
}
4. C 버전 선언하면서 초기화
#include <stdio.h>

struct Point {
    int x;
    int y;
};

int main() {
    struct Point p1 = {10, 20};

    printf("x = %d, y = %d\n", p1.x, p1.y);

    return 0;
}

여기서

x = 10

y = 20

으로 들어가.

5. C 버전 함수에 struct 전달
#include <stdio.h>

struct Point {
    int x;
    int y;
};

void printPoint(struct Point p) {
    printf("x = %d, y = %d\n", p.x, p.y);
}

int main() {
    struct Point p1 = {3, 7};
    printPoint(p1);

    return 0;
}

이건 구조체 변수를 함수에 넘긴 거야.

6. C 버전 typedef 같이 많이 씀

C에서는 매번 struct Person 쓰기 귀찮아서 이렇게 많이 해.

#include <stdio.h>
#include <string.h>

typedef struct {
    char name[20];
    int age;
} Person;

int main() {
    Person p1;

    strcpy(p1.name, "Kim");
    p1.age = 30;

    printf("이름: %s\n", p1.name);
    printf("나이: %d\n", p1.age);

    return 0;
}

이제는

struct Person p1;

이 아니라

Person p1;

이렇게 바로 쓸 수 있어.

7. C++ 버전 struct 기본

C++도 거의 비슷해.

#include <iostream>
#include <string>
using namespace std;

struct Person {
    string name;
    int age;
    float height;
};

int main() {
    Person p1;

    p1.name = "Kim";
    p1.age = 20;
    p1.height = 175.5f;

    cout << "이름: " << p1.name << endl;
    cout << "나이: " << p1.age << endl;
    cout << "키: " << p1.height << endl;

    return 0;
}
C와 C++ 차이점 1

C는 보통 이렇게 썼지:

struct Person p1;

그런데 C++은 구조체 이름만으로 바로 자료형처럼 쓸 수 있어:

Person p1;

struct를 다시 안 붙여도 돼.

C와 C++ 차이점 2

C++은 string을 쓸 수 있어서 문자열 다루기가 편해.

p1.name = "Kim";

C처럼 strcpy() 안 써도 돼.

8. C++ 버전 초기화
#include <iostream>
#include <string>
using namespace std;

struct Point {
    int x;
    int y;
};

int main() {
    Point p1 = {10, 20};

    cout << p1.x << " " << p1.y << endl;

    return 0;
}
9. C++ 버전 함수에 전달
#include <iostream>
#include <string>
using namespace std;

struct Student {
    string name;
    int score;
};

void printStudent(Student s) {
    cout << "이름: " << s.name << endl;
    cout << "점수: " << s.score << endl;
}

int main() {
    Student s1 = {"Lee", 95};
    printStudent(s1);

    return 0;
}
10. C++ struct는 함수도 넣을 수 있음

이게 C보다 큰 차이야.

#include <iostream>
#include <string>
using namespace std;

struct Person {
    string name;
    int age;

    void introduce() {
        cout << "내 이름은 " << name << "이고 나이는 " << age << "살입니다." << endl;
    }
};

int main() {
    Person p1;
    p1.name = "Kim";
    p1.age = 23;

    p1.introduce();

    return 0;
}

즉 C++의 struct는
변수만 넣는 상자가 아니라
함수도 넣을 수 있는 작은 클래스 느낌이야.

11. C++에서 struct와 class 차이

C++에서 거의 비슷한데 기본 차이는 이거야.

struct A {
    int x;
};

class B {
    int x;
};

차이:

struct 는 기본 접근이 public

class 는 기본 접근이 private

즉 struct는 기본적으로 바깥에서 바로 접근 가능.

A a;
a.x = 10;   // 가능

하지만 class는 기본적으로 바로 접근 안 됨.

12. 진짜 쉬운 예제 하나씩
C 예제: 좌표
#include <stdio.h>

struct Point {
    int x;
    int y;
};

int main() {
    struct Point p;

    p.x = 5;
    p.y = 8;

    printf("(%d, %d)\n", p.x, p.y);

    return 0;
}
뜻

x, y를 따로 두지 않고
Point라는 한 묶음으로 관리

C++ 예제: 좌표
#include <iostream>
using namespace std;

struct Point {
    int x;
    int y;
};

int main() {
    Point p;

    p.x = 5;
    p.y = 8;

    cout << "(" << p.x << ", " << p.y << ")" << endl;

    return 0;
}
13. 네가 꼭 기억해야 할 핵심
struct는 왜 쓰냐?

관련 있는 변수들을 하나로 묶으려고

예:

학생 → 이름, 나이, 점수

좌표 → x, y

감지 결과 → success, label, center

기본 문법
C
struct 이름 {
    자료형 멤버;
    자료형 멤버;
};
C++
struct 이름 {
    자료형 멤버;
    자료형 멤버;
};
변수 만들기
C
struct Person p1;
C++
Person p1;
값 넣기
p1.age = 20;

점 . 으로 접근

14. 네가 아까 본 코드랑 연결하면

아까 너 코드에 있던

struct DetectionResult {
    bool success = false;
    std::string label = "NONE";
    cv::Point center = cv::Point(0, 0);
    cv::Rect rect;
};

이건 바로

감지 결과를 한 덩어리로 묶은 struct 야.

즉 따로따로 만들면

bool success;
std::string label;
cv::Point center;
cv::Rect rect;

이렇게 흩어지는데,
구조체로 묶어서

DetectionResult result;

하나로 관리하는 거지.

그리고 쓸 때는

result.success = true;
result.label = "BLUE";
result.center = cv::Point(100, 50);

이렇게 쓰는 거야.

15. 아주 간단 비교
C
struct Point {
    int x;
    int y;
};
C++
struct Point {
    int x;
    int y;
};

겉모양은 거의 같음.

차이:

C는 보통 struct Point p;

C++은 Point p;

C++은 함수도 넣을 수 있음

C++은 string 사용 편함
