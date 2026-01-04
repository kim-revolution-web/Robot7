#include"opencv2/opencv.hpp"
#include<iostream>
#include<ctime>
#include<vector>

structkarina {
    cv::Point position;// ✅ (x,y) 좌표 저장용
int radius;// ✅ 원(또는 스프라이트)의 반지름(크기)
bool active;// ✅ "활성화 상태"로 쓰려고 만든 변수(현재 코드는 거의 사용 안 함)

karina() {
this->position = cv::Point();// ✅ (0,0)으로 초기화
this->radius =0;// ✅ 반지름 초기값
this->active =false;// ✅ 초기엔 비활성(하지만 아래에서 if(!active)라 항상 true가 됨)
    }
};

cv::Point getRandom(int width,int height,int radius) {
// ✅ 랜덤 위치 생성 (원/이미지가 화면 밖으로 나가지 않게 "radius만큼 여유"를 둠)
// x: [radius, width - radius), y: [radius, height - radius) 범위에서 뽑히게 함
int x =rand() % (width  -2 * radius) + radius;
int y =rand() % (height -2 * radius) + radius;
return cv::Point(x, y);// ✅ 좌표를 반환
}

voidshow100() CV_NOEXCEPT
{
// ✅ srand(): rand()의 난수 시드를 초기화.
// time(0)은 현재 시간을 초 단위로 주고, (unsigned int)로 형변환해서 넣는 것.
srand((unsignedint)time(0));

cv::VideoCapture cap(0);// ✅ 0번 카메라 장치 열기
if (!cap.isOpened()) {
        std::cerr <<"NO CAM\n";
return;
    }

// ⚠️ 주의: 아래 width/height는 "캠 기본 해상도"임(예: 640x480).
// 그런데 네 코드는 frame을 800x800으로 resize 하므로, 이 값은 곧 "틀린 기준"이 됨.
int width =cvRound(cap.get(cv::CAP_PROP_FRAME_WIDTH));
int height =cvRound(cap.get(cv::CAP_PROP_FRAME_HEIGHT));

    cv::Mat prevgray;// ✅ "이전 프레임(그레이)" 저장용 (프레임 차이 계산에 필요)

    karina kar;
    kar.radius =30;// ✅ 표시 크기(반지름)
    kar.position =getRandom(width, height, kar.radius);// ✅ 초기 위치 랜덤
int score =0;

while (1) {
        cv::Mat frame, gray_frame, diff, thresh;
        cap >> frame;// ✅ 카메라에서 프레임 받아오기
if (frame.empty())break;

        cv::flip(frame, frame,1);// ✅ 좌우 반전(거울 모드)

        cv::resize(frame, frame, cv::Size(800,800));// ⚠️ 좌표계가 바뀜(중요!)

// ✅ resize 이후에는 width/height를 frame 기준으로 다시 잡아야 함
        width = frame.cols;
        height = frame.rows;

// ✅ BGR(3채널) -> Gray(1채널) 변환 (3색상을 표현하게 하는 게 아니라 "흑백 1채널"로 줄이는 것)
        cv::cvtColor(frame, gray_frame, cv::COLOR_BGR2GRAY);

// ✅ 블러(가우시안): 노이즈 줄여서 "작은 흔들림/잡음"이 diff로 튀는 걸 완화
// cv::Size(15,15)는 커널(필터) 크기. 보통 홀수(3,5,7,...)로 씀.
// 마지막 0은 sigma 자동 계산.
        cv::GaussianBlur(gray_frame, gray_frame, cv::Size(15,15),0);

if (prevgray.empty()) {
// ✅ 첫 프레임에는 비교 대상(prevgray)이 없으니
// "기준 프레임"으로 저장하고 다음 루프로 넘어감
            gray_frame.copyTo(prevgray);
continue;
        }

// ✅ 프레임 차이(이전-현재)를 절댓값으로: 움직인 픽셀만 밝게 남음
        cv::absdiff(prevgray, gray_frame, diff);

// ✅ 차이가 일정 이상(25)인 픽셀을 255로: 움직임 영역만 남기는 이진화
        cv::threshold(diff, thresh,25.0,255.0, cv::THRESH_BINARY);

// ✅ active를 실제로 바꾸는 코드가 없어서 지금은 항상 (!kar.active) = true 상태
if (!kar.active)
        {
// ✅ "원 주변 사각형 ROI" 만들기
// max/min은 ROI가 화면 밖으로 나가지 않게 클리핑(잘라내기)하는 용도
int x1 = cv::max(0, kar.position.x - kar.radius);
int y1 = cv::max(0, kar.position.y - kar.radius);
int x2 = cv::min(width,  kar.position.x + kar.radius);
int y2 = cv::min(height, kar.position.y + kar.radius);

cv::Rect karRect(x1, y1, x2 - x1, y2 - y1);// ✅ (x1,y1)에서 시작, 폭/높이

            cv::Mat roi =thresh(karRect);// ✅ 해당 영역만 잘라서
int movementPixels = cv::countNonZero(roi);// ✅ "흰색(255)" 픽셀 개수 = 움직임 픽셀 수

// ✅ 원래는 ROI 크기(실제 폭*높이)를 쓰는 게 더 정확함(가장자리면 잘리니까)
int area = karRect.width * karRect.height;

// ✅ area*0.1 : ROI 면적의 10% 이상이 움직였을 때만 "터치"로 판정(노이즈 방지)
if (movementPixels > area *0.1) {
                std::cout <<"터치 " << ++score <<"\n";
                kar.position =getRandom(width, height, kar.radius);// ✅ 새로운 위치로 이동
            }
        }

// ✅ 흰 원으로 표시(여기를 나중에 사진 스프라이트로 바꾸면 됨)
        cv::circle(frame, kar.position, kar.radius, cv::Scalar(255,255,255),-1);

        cv::putText(frame,"Score:" + std::to_string(score),
            cv::Point(20,30), cv::FONT_HERSHEY_PLAIN,2,
            cv::Scalar(255,255,255),2);

        cv::imshow("GAME", frame);

// ✅ "이번 프레임"을 다음 루프의 prevgray로 갱신(계속 움직임 비교하려면 매 프레임 갱신 필요)
        gray_frame.copyTo(prevgray);

if (cv::waitKey(10) ==27)break;
    }

    cap.release();
    cv::destroyAllWindows();
}
