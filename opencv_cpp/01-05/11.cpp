#include "opencv2/opencv.hpp"
#include <iostream>
#include <ctime>
#include <vector>


struct karina {
	cv::Point position;
	int radius;
	bool active;
	karina() {
		this->position = cv::Point(); //좌표 받을려고?
		this->radius = 0; // 반지름
		this->active = false; // 상태?
	}
};

cv::Point getRandom(int width, int height, int radius) {
	int x = rand() % (width - 2 * radius) + radius;
	int y = rand() % (height - 2 * radius) + radius;
	return cv::Point(x, y);
	//랜덤 좌표를 주는거지 나눈값 넘지 않게하고 최고 radius 만큼은 줘서 뭘하려는거지?
	//return으로 좌표 넘겨준거지?
}


void show100() CV_NOEXCEPT
{
	srand((unsigned int)time(0)); //srand 초기화 하려고 time 넣는거지? srand가  
	//unsigned int 받아서 형변환 해준거지?

	
	cv::VideoCapture cap(0); //비디오 겹쳐 카메라 한대 
	if (!cap.isOpened()) {
		std::cerr << "NO CAM" << "\n";
		return;
	}

	int width = cvRound(cap.get(cv::CAP_PROP_FRAME_WIDTH)); //640x480 캡쳐 받은 길이 정수형 변환
	int height = cvRound(cap.get(cv::CAP_PROP_FRAME_HEIGHT)); //높이 변환
	cv::Mat prevgray; //이거 뭐하게?
	karina kar; //구조체 생성
	kar.radius = 30; // 반지름 30
	kar.position = getRandom(width, height, kar.radius);
	//%(영상길이에-지름 60)이만큼을 넘지않게 +최소 반지름 0일때 반지름 만큼 공간 확보
	int score = 0;

	
	while (1) {
		cv::Mat frame, gray_frame, diff, thresh;
		cap >> frame; //VideoCapture를 frame에 넣어 
		if (frame.empty())break;

		cv::flip(frame, frame, 1); //좌우 반전줘
		cv::resize(frame, frame, cv::Size(800, 800)); 
		//이진화 주요 객체 영역과 배경영역을 나눔
		cv::cvtColor(frame, gray_frame, cv::COLOR_BGR2GRAY); 
		//그레이로 나오는데 3색상을 표현 할수 있게 해줘
		cv::GaussianBlur(gray_frame, gray_frame, cv::Size(15, 15), 0);
		//노이즈 제거 이진화 하기전 그레이 색상에  Size 를 왜 주는거지?  평면이면 -1 아닌가?

		if (prevgray.empty()) {//아무것도 안줬으니 무조건 들어와
			gray_frame.copyTo(prevgray); //이진화 작업전 그레이 색상 왜 복사해?
			continue;
		}
		
		cv::absdiff(prevgray,gray_frame,diff);//영상차이 p234  영상 차이로 뭐할껀데?
		cv::threshold(diff, thresh, 25.0, 255.0, cv::THRESH_BINARY); //이진화 해주기

		if (!kar.active)//상태변화 없으면
		{
			int x1 = cv::max(0, kar.position.x - kar.radius);
			//%(영상길이에-지름 60)이만큼을 넘지않게 해서 최소로 더해주고 다시 빼는 게 맞아?
			//0, 가 아니라 0+radius ,(width - 2 * radius) 이렇게 하는거아니야? 
			int y1 = cv::max(0, kar.position.y - kar.radius);
			int x2 = cv::min(width, kar.position.x + kar.radius);
			int y2 = cv::min(height, kar.position.y + kar.radius);
			cv::Rect karRect(x1, y1, x2 - x1, y2 - y1); //사각형 시작좌표야?

			cv::Mat roi = thresh(karRect); 
			int movementPixels = cv::countNonZero(roi);//여기다 좌표를 넣어줘?
			int area = (kar.radius * 2) * (kar.radius * 2); //크기를 지름만큼? 60*60 크기라는거야?
			if (movementPixels > area * 0.1) {//0.1를 왜 곱한거야?
				std::cout << "터치" << ++score << "\r\n";
				kar.position = getRandom(width, height, kar.radius);//랜덤좌표를  position에 넣었어
			}

		}
		
		cv::circle(frame, kar.position, kar.radius, cv::Scalar(255, 255, 255), -1);
		cv::putText(frame, "Score:" + std::to_string(score), cv::Point(20, 30), cv::FONT_HERSHEY_PLAIN, 2,
		cv::Scalar(255,255,255),2);
		

		cv::imshow("GAME", frame);
		gray_frame.copyTo(prevgray); //위에서 했는 왜 또하는거지?
		if (cv::waitKey(10) == 27)
			break;

	}

	cap.release();
	cv::destroyAllWindows();
}

