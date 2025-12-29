#include "opencv2/opencv.hpp"
#include <iostream>
#include<ctime>
#include<vector>

struct Ball {
	cv::Point position;// x ,y
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
	int y = rand() % (height - 2 * radius) + radius;
	return cv::Point(x, y);
}

void runProject() CV_NOEXCEPT
{
	srand((unsigned int)time(0));
	cv::VideoCapture cap(0);
	if (!cap.isOpened()) {
		std::cerr << "웹 캡이 없습니다.\n";
		return;
	}
	int width = cvRound(cap.get(cv::CAP_PROP_FRAME_WIDTH));
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

		cv::flip(frame, frame, 1);//반전
		//움직임 감지
		cv::cvtColor(frame, gray_frame, cv::COLOR_BGR2GRAY);
		cv::GaussianBlur(gray_frame, gray_frame, cv::Size(15, 15),0);
		if (prev_gray.empty()) {
			gray_frame.copyTo(prev_gray);
			continue;
		}
		cv::absdiff(prev_gray, gray_frame, diff);
		cv::threshold(diff, thresh, 25.0, 255.0, cv::THRESH_BINARY);
		if (!redBall.active) 
		{
			// ball 외곽선 사각형
			int x1 = cv::max(0, redBall.position.x - redBall.radius);
			int y1 = cv::max(0, redBall.position.y - redBall.radius);
			int x2 = cv::min(width, redBall.position.x + redBall.radius);
			int y2 = cv::min(height, redBall.position.y + redBall.radius);
			cv::Rect ballRect(x1, y1, x2-x1,y2-y1);

			cv::Mat roi = thresh(ballRect);
			int movementPixels = cv::countNonZero(roi);
			// 픽셀들의 움직임을 체크
			int area = (redBall.radius * 2) * (redBall.radius * 2);
			if (movementPixels > area * 0.1) {
				std::cout << "터치" << ++score << "\r\n";
				redBall.position = getRandomPosition(width, height, redBall.radius);

			}
		}
		cv::circle(frame, redBall.position, redBall.radius, cv::Scalar(0, 0, 255), -1);
		cv::putText(frame,"Score:"+std::to_string(score),cv::Point(20,30),cv::FONT_HERSHEY_PLAIN,2,
			cv::Scalar(255, 255, 255), 2);
		cv::imshow("GAME", frame);
		gray_frame.copyTo(prev_gray); //화면 없데이트
		if (cv::waitKey(10) == 27)break;
		
	}
	cap.release();
	cv::destroyAllWindows();
}