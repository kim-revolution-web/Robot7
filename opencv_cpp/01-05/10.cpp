#include "opencv2/opencv.hpp"
#include <iostream>
#include<ctime>
#include<vector>

struct Ball {
	cv::Point position;// x ,y  2차원 평면 위에 있는 점의 좌표를 표현하는 템플릿 클래스
	int radius; // 반지름
	bool active;
	Ball() {
		this->position = cv::Point();
		this->radius = 0;
		this->active = false;
	}
};

cv::Point getRandomPosition(int width, int height, int radius) {
	int x = rand() % (width - 2 * radius) + radius;
	//rand() % (width - 2 * radius) + radius;  나누고 나서 +radius 하면 최소값
	//rand() % (width - 2 * radius) 이건 최대값 
	int y = rand() % (height - 2 * radius) + radius;
	return cv::Point(x, y); //Point 형이니까 Point 리턴
}

void runProject() CV_NOEXCEPT //이 함수는 예외를 던지지 않는다” 라고 표시하는 용도야.
{
	srand((unsigned int)time(0)); //srand는 안에 값을 바꿔줘야 하는데 그걸 타임으로 넣어줌 난수 seed 초기화

	cv::VideoCapture cap(0); //기본카메라 설정
	if (!cap.isOpened()) {
		std::cerr << "웹 캡이 없습니다.\n";
		return;
	}

	int width = cvRound(cap.get(cv::CAP_PROP_FRAME_WIDTH)); //정수형으로 변환할때 반올림을 한다 ,프레임 폭
	int height = cvRound(cap.get(cv::CAP_PROP_FRAME_HEIGHT));
	cv::Mat prev_gray;//이전 화면
	Ball redBall; //Ball 객체
	redBall.radius = 20;
	redBall.position = getRandomPosition(width, height, redBall.radius);
	int score = 0;

	while (true)
	{
		cv::Mat frame, gray_frame, diff, thresh;// 흰 픽셀(ball)
		cap >> frame;
		if (frame.empty())break;

		cv::flip(frame, frame, 1);//화면이 반전되서 나옴 
		//움직임 감지
		cv::resize(frame, frame, cv::Size(800, 800));
		cv::cvtColor(frame, gray_frame, cv::COLOR_BGR2GRAY);
		//움직임 감지에서 중요한 건 색이 아니라 밝기 변화
		//컬러(BGR) 3채널이면 비교량이 많고 잡음도 늘어남
		//그레이 1채널이면 빠르고 안정적으로 “변화”만 볼 수 있음
		cv::GaussianBlur(gray_frame, gray_frame, cv::Size(15, 15), 0);
		//카메라 노이즈/잔잔한 픽셀 변화 때문에 움직임으로 오검출이 날 수 있어.
		//블러로 작은 흔들림 / 노이즈를 뭉개서
		//진짜 큰 변화(손이 들어옴 같은 것)만 남기려는 목적.
		if (prev_gray.empty()) {
			gray_frame.copyTo(prev_gray);//그레이 프레임 카피
			continue;
		}

		cv::absdiff(prev_gray, gray_frame, diff); //영상 객체 추적,배경제거
		//움직인 부분은 차이가 커지고, 배경은 차이가 작음
		cv::threshold(diff, thresh, 25.0, 255.0, cv::THRESH_BINARY );//이진화
		
		

		if (!redBall.active)
		{
			// ball 외곽선 사각형
			int x1 = cv::max(0, redBall.position.x - redBall.radius);
			int y1 = cv::max(0, redBall.position.y - redBall.radius);
			int x2 = cv::min(width, redBall.position.x + redBall.radius);
			int y2 = cv::min(height, redBall.position.y + redBall.radius);
			cv::Rect ballRect(x1, y1, x2 - x1, y2 - y1);

			cv::Mat roi = thresh(ballRect);
			int movementPixels = cv::countNonZero(roi); //영상의 차이를 구분하기 위해서 
			// 픽셀들의 움직임을 체크
			int area = (redBall.radius * 2) * (redBall.radius * 2);
			if (movementPixels > area * 0.1) { //10% 임계치 튜닝값 
				std::cout << "터치" << ++score << "\r\n";
				redBall.position = getRandomPosition(width, height, redBall.radius);

			}
		}
		

		cv::circle(frame, redBall.position, redBall.radius, cv::Scalar(255, 255, 255), -1);
		cv::putText(frame, "Score:" + std::to_string(score), cv::Point(20, 30), cv::FONT_HERSHEY_PLAIN, 2,
			cv::Scalar(255, 255, 255),2);


		//------------------------------------
		cv::Mat img1 = cv::imread("ka.jpg");
		cv::Mat img2 = img1(cv::Rect(100, 50, 400, 500));
		cv::Mat img3;
		cv::resize(img2, img3, cv::Size(50, 50)); //크기줄임
		cv::Mat mask;
		cv::cvtColor(img2, mask, cv::COLOR_RGB2GRAY);
		cv::threshold(mask, mask, 0, 255, cv::THRESH_BINARY | cv::THRESH_OTSU);

		cv::resize(mask, mask, cv::Size(50, 50));

		//img3.copyTo(, ~mask);//원이랑 합성

		//cv::circle(frame, redBall.position, redBall.radius, cv::Scalar(255, 255, 255), -1); 
		
		if (score > 5) {//5점이상 좌우대칭
			cv::flip(frame, frame, 0);// 상하
			cv::flip(frame, frame, -1);//좌우 상하
			cv::putText(frame, "LR reversal" + std::to_string(score), cv::Point(20, 30), cv::FONT_HERSHEY_PLAIN, 2,
			cv::Scalar(255, 255, 255), 2);
			
		}
		
		if (score >10) {//10점이상 상하대칭
			cv::flip(frame, frame, 0); //상하
			cv::flip(frame, frame, 1);
			cv::putText(frame, "UD reversal " + std::to_string(score), cv::Point(20, 30), cv::FONT_HERSHEY_PLAIN, 2,
				cv::Scalar(255, 255, 255), 2);
		}
		
		if (score > 15) {//10점이상 상하대칭
			cv::flip(frame, frame, 1); //좌우상하
			cv::putText(frame, "UD LR reversal" + std::to_string(score), cv::Point(20, 30), cv::FONT_HERSHEY_PLAIN, 2,
				cv::Scalar(255, 255, 255), 2);
			cvtColor(frame, frame, cv::COLOR_RGB2GRAY);
		}

		if (score > 20) { //code6 / show 38
			cv::Point2d center(frame.cols / 2, frame.rows / 2);
			cv::Mat move = cv::getRotationMatrix2D(center, 20.0, 1.0);//음수면 반시계 //양수면 시계 방향 //2x3 affine 행렬
			//호도 법
			cv::Mat dst;
			cv::warpAffine(frame, frame, move, cv::Size());
		}


		//cv::Mat dst_open;
		//for (int i = 0; i < 50; i++) {
		//	cv::morphologyEx(frame, dst_open, cv::MORPH_OPEN, cv::Mat());  //기본이 3X3 침식->팽창
		//}

		//cv::Mat dst_close;
		//for (int i = 0; i < 50; i++) {
		//	cv::morphologyEx(frame, dst_close, cv::MORPH_CLOSE, cv::Mat()); //기본이 3X3 팽창 -> 침식 
		//}


		//----------------------------------
		
		cv::imshow("GAME", frame);
		gray_frame.copyTo(prev_gray); //화면 없데이트
		if (cv::waitKey(10) == 27)break;

	}
	cap.release(); //메모리 헤제
	cv::destroyAllWindows();
}
