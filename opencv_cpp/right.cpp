#include "opencv2/opencv.hpp"
#include <iostream>
#include <ctime>
#include <vector>
#define NOMINMAX
#include <windows.h>
#include <mmsystem.h>

#pragma comment(lib, "winmm.lib")

struct Ball {
	cv::Point position;					// x, y 좌표
	int radius;							// 반지름
	bool active;						// active factor
	// 구조체 생성자
	Ball() {
		this->position = cv::Point();
		this->radius = 0;
		this->active = false;
	}
};


static void reverseFace(int score, cv::Rect faceRect, cv::Mat faceBall, cv::Mat& frame)
{
	switch ((score % 4))
	{
		case 0:
		{
			faceBall.copyTo(frame(faceRect));
			break;
		}
		case 1:
		{
			cv::Mat flipface;
			cv::flip(faceBall, flipface, 1);	// 좌우반전
			flipface.copyTo(frame(faceRect));
			break;
		}
		case 2:
		{
			cv::Mat flipface;
			cv::flip(faceBall, flipface, 0);	// 상하반전
			flipface.copyTo(frame(faceRect));
			break;
		}
		case 3:
		{
			cv::Mat flipface;
			cv::flip(faceBall, flipface, -1);	// 상하좌우 반전
			flipface.copyTo(frame(faceRect));
			break;
		}
	}
}

static void shearFace(int score, cv::Rect faceRect, cv::Mat faceBall, cv::Mat& frame)
{
	float x_shear_factor = 0.4f;									// x축 기울기 Factor
	float y_shear_factor = 0.4f;									// y축 기울기 Factor

	switch ((score % 4))
	{
		case 0:
		{
			faceBall.copyTo(frame(faceRect));
			break;
		}
		case 1:
		{
			int w = faceBall.cols;
			int h = faceBall.rows + static_cast<int>(faceBall.cols * std::abs(x_shear_factor));
			cv::Mat move = cv::Mat_<float>(								
				{ 2,3 },
				{ 1.0f, 0.0f, 0.0f,
				x_shear_factor, 1.0f, 0.0f });

			cv::Mat temp;
			cv::warpAffine(faceBall, temp, move, cv::Size(w,h));
			cv::Mat shear_face;
			cv::resize(temp, shear_face, cv::Size(30, 30));
			shear_face.copyTo(frame(faceRect));
			break;
		}
		case 2:
		{
			int w = faceBall.cols + static_cast<int>(faceBall.rows * std::abs(y_shear_factor));
			int h = faceBall.rows;
			cv::Mat move = cv::Mat_<float>(								
				{ 2,3 },
				{ 1.0f, y_shear_factor, 0.0f,
				0.0f, 1.0f, 0.0f });

			cv::Mat temp;
			cv::warpAffine(faceBall, temp, move, cv::Size(w, h));
			cv::Mat shear_face;
			cv::resize(temp, shear_face, cv::Size(30, 30));
			shear_face.copyTo(frame(faceRect));
			break;
		}
		case 3:
		{
			int w = faceBall.cols + static_cast<int>(faceBall.rows * std::abs(y_shear_factor));
			int h = faceBall.rows + static_cast<int>(faceBall.cols * std::abs(x_shear_factor));
			cv::Mat move = cv::Mat_<float>(								
				{ 2,3 },
				{ 1.0f, y_shear_factor, 0.0f,
				x_shear_factor, 1.0f, 0.0f });

			cv::Mat temp;
			cv::warpAffine(faceBall, temp, move, cv::Size(w, h));
			cv::Mat shear_face;
			cv::resize(temp, shear_face, cv::Size(30, 30));
			shear_face.copyTo(frame(faceRect));
			break;
		}
	}
}

static void expandFace(int score,cv::Rect faceRect, cv::Mat faceBall, cv::Mat& frame, Ball redBall)
{
	switch ((score % 4))
	{
	case 0:
	{
		faceBall.copyTo(frame(faceRect));
		break;
	}
	case 1:
	{
		cv::Mat expandedface;
		int p_x = 0;
		int p_y = 0;
		cv::resize(faceBall, expandedface, cv::Size(), 1.5, 1.5, cv::INTER_LANCZOS4);

		int half_r = std::round(expandedface.cols / 2.0);
		if (redBall.position.x < (frame.cols / 2))
		{
			p_x = redBall.position.x + (half_r - redBall.radius);
		}
		else
		{
			p_x = redBall.position.x - (half_r - redBall.radius);
		}
		if (redBall.position.y < (frame.rows / 2))
		{
			p_y = redBall.position.y + (half_r - redBall.radius);
		}
		else
		{
			p_y = redBall.position.y - (half_r - redBall.radius);
		}

		int x1 = cv::max(0, p_x - half_r);
		int y1 = cv::max(0, p_y - half_r);

		cv::Rect new_R(x1, y1, expandedface.cols, expandedface.rows);
		expandedface.copyTo(frame(new_R));
		break;
	}
	case 2:
	{
		cv::Mat expandedface;
		int p_x = 0;
		int p_y = 0;
		cv::resize(faceBall, expandedface, cv::Size(), 2.25, 2.25, cv::INTER_LANCZOS4);

		int half_r = std::round(expandedface.cols / 2.0);
		if (redBall.position.x < (frame.cols / 2))
		{
			p_x = redBall.position.x + (half_r - redBall.radius);
		}
		else
		{
			p_x = redBall.position.x - (half_r - redBall.radius);
		}
		if (redBall.position.y < (frame.rows / 2))
		{
			p_y = redBall.position.y + (half_r - redBall.radius);
		}
		else
		{
			p_y = redBall.position.y - (half_r - redBall.radius);
		}

		int x1 = cv::max(0, p_x - half_r);
		int y1 = cv::max(0, p_y - half_r);

		cv::Rect new_R(x1, y1, expandedface.cols, expandedface.rows);
		expandedface.copyTo(frame(new_R));
		break;
	}
	case 3:
	{
		cv::Mat expandedface;
		int p_x = 0;
		int p_y = 0;
		cv::resize(faceBall, expandedface, cv::Size(), 3.375, 3.375, cv::INTER_LANCZOS4);

		int half_r = std::round(expandedface.cols / 2.0);
		if (redBall.position.x < (frame.cols / 2))
		{
			p_x = redBall.position.x + (half_r - redBall.radius);
		}
		else
		{
			p_x = redBall.position.x - (half_r - redBall.radius);
		}
		if (redBall.position.y < (frame.rows / 2))
		{
			p_y = redBall.position.y + (half_r - redBall.radius);
		}
		else
		{
			p_y = redBall.position.y - (half_r - redBall.radius);
		}

		int x1 = cv::max(0, p_x - half_r);
		int y1 = cv::max(0, p_y - half_r);

		cv::Rect new_R(x1, y1, expandedface.cols, expandedface.rows);
		expandedface.copyTo(frame(new_R));
		break;
	}
	}
}

static void reduceFace(int score, cv::Rect faceRect, cv::Mat faceBall, cv::Mat& frame, Ball redBall)
{
	switch ((score % 4))
	{
	case 0:
	{
		faceBall.copyTo(frame(faceRect));
		break;
	}
	case 1:
	{
		cv::Mat reducedface;
		cv::resize(faceBall, reducedface, cv::Size(), 0.75, 0.75, cv::INTER_LANCZOS4);

		int r_diff = std::round((faceRect.width - reducedface.cols) / 2.0);
		
		int x1 = faceRect.x + r_diff;
		int y1 = faceRect.y + r_diff;

		cv::Rect new_R(x1, y1, reducedface.cols, reducedface.rows);
		reducedface.copyTo(frame(new_R));
		break;
	}
	case 2:
	{
		cv::Mat reducedface;
		cv::resize(faceBall, reducedface, cv::Size(), 0.5, 0.5, cv::INTER_LANCZOS4);

		int r_diff = std::round((faceRect.width - reducedface.cols) / 2.0);

		int x1 = faceRect.x + r_diff;
		int y1 = faceRect.y + r_diff;

		cv::Rect new_R(x1, y1, reducedface.cols, reducedface.rows);
		reducedface.copyTo(frame(new_R));
		break;
	}
	case 3:
	{
		cv::Mat reducedface;
		cv::resize(faceBall, reducedface, cv::Size(), 0.25, 0.25, cv::INTER_LANCZOS4);

		int r_diff = std::round((faceRect.width - reducedface.cols) / 2.0);

		int x1 = faceRect.x + r_diff;
		int y1 = faceRect.y + r_diff;

		cv::Rect new_R(x1, y1, reducedface.cols, reducedface.rows);
		reducedface.copyTo(frame(new_R));
		break;
	}
	}
}

static void changeFaceColor(int score, cv::Rect faceRect, cv::Mat faceBall, cv::Mat& frame)
{
	switch ((score % 6))
	{
	case 0:
	{
		faceBall.copyTo(frame(faceRect));
		break;
	}
	case 1:
	{
		cv::Mat r_faceBall = faceBall - cv::Scalar(255, 255, 0);
		r_faceBall.copyTo(frame(faceRect));
		break;
	}
	case 2:
	{
		cv::Mat g_faceBall = faceBall - cv::Scalar(255, 0, 255);
		g_faceBall.copyTo(frame(faceRect));
		break;
	}
	case 3:
	{
		cv::Mat r_faceBall = faceBall - cv::Scalar(0, 255, 255);
		r_faceBall.copyTo(frame(faceRect));
		break;
	}
	case 4:
	{
		cv::Mat gray_faceBall;
		cv::cvtColor(faceBall, gray_faceBall, cv::COLOR_BGR2GRAY);
		cv::cvtColor(gray_faceBall, gray_faceBall, cv::COLOR_GRAY2BGR);
		gray_faceBall.copyTo(frame(faceRect));
		break;
	}
	case 5:
	{
		cv::Mat n_faceBall = ~faceBall;
		n_faceBall.copyTo(frame(faceRect));
		break;
	}
	}
}

static void morphologyFace(int score, cv::Rect faceRect, cv::Mat faceBall, cv::Mat& frame)
{
	cv::Mat gray_faceBall;
	cv::cvtColor(faceBall, gray_faceBall, cv::COLOR_BGR2GRAY);
	switch ((score % 6))
	{
	case 0:
	{
		faceBall.copyTo(frame(faceRect));
		break;
	}
	case 1:
	{
		cv::Mat temp;
		cv::threshold(gray_faceBall, temp, 0, 255, cv::THRESH_BINARY | cv::THRESH_OTSU);

		cv::cvtColor(temp, temp, cv::COLOR_GRAY2BGR);
		temp.copyTo(frame(faceRect));
		break;
	}
	case 2:
	{
		cv::Mat temp;
		cv::threshold(gray_faceBall, temp, 0, 255, cv::THRESH_BINARY | cv::THRESH_OTSU);

		cv::Mat morphedface;
		cv::erode(temp, morphedface, cv::Mat());
		cv::cvtColor(morphedface, morphedface, cv::COLOR_GRAY2BGR);
		morphedface.copyTo(frame(faceRect));
		break;
	}
	case 3:
	{
		cv::Mat temp;
		cv::threshold(gray_faceBall, temp, 0, 255, cv::THRESH_BINARY | cv::THRESH_OTSU);

		cv::Mat morphedface;
		cv::dilate(temp, morphedface, cv::Mat());
		cv::cvtColor(morphedface, morphedface, cv::COLOR_GRAY2BGR);
		morphedface.copyTo(frame(faceRect));
		break;
	}
	case 4:
	{
		cv::Mat temp;
		cv::threshold(gray_faceBall, temp, 0, 255, cv::THRESH_BINARY | cv::THRESH_OTSU);

		cv::Mat morphedface;
		cv::morphologyEx(temp, morphedface, cv::MORPH_OPEN, cv::Mat());
		cv::cvtColor(morphedface, morphedface, cv::COLOR_GRAY2BGR);
		morphedface.copyTo(frame(faceRect));
		break;
	}
	case 5:
	{
		cv::Mat temp;
		cv::threshold(gray_faceBall, temp, 0, 255, cv::THRESH_BINARY | cv::THRESH_OTSU);

		cv::Mat morphedface;
		cv::morphologyEx(temp, morphedface, cv::MORPH_CLOSE, cv::Mat());
		cv::cvtColor(morphedface, morphedface, cv::COLOR_GRAY2BGR);
		morphedface.copyTo(frame(faceRect));
		break;
	}
	}
}

static void on_mode_changed(int pos, void* userdata) 
{
	int* mode_ptr = static_cast<int*>(userdata);

	*mode_ptr = pos;

	std::cout << "현재 모드 변경: " << *mode_ptr << std::endl;
}

// Ball 객체의 Position을 설정해주는 함수
cv::Point getRandomPosition(int width, int height, int radius) {
	int x = rand() % (width - 2 * radius) + radius;					// x 좌표의 범위 : (radius ~ (width-radius-1)) 
	int y = rand() % (height - 2 * radius) + radius;				// y 좌표의 범위 : (radius ~ (height-radius-1)) 
	return cv::Point(x, y);
}

void runProject() CV_NOEXCEPT
{
	// rand 함수의 Seed 값 설정.
	srand((unsigned int)time(0));

	// 0번째 Port로 연결된 Cap 영상이 담길 객체 생성.
	cv::VideoCapture cap(0);
	if (!cap.isOpened()) {
		std::cerr << "웹캠이 없습니다.\n";
		return;
	}

	// width, height 선언 및 정의.
	int width = cvRound(cap.get(cv::CAP_PROP_FRAME_WIDTH));
	int height = cvRound(cap.get(cv::CAP_PROP_FRAME_HEIGHT));


	cv::Mat prev_gray;	// 이전 화면
	Ball redBall;		// Ball 객체

	// Ball 객체 멤버 정의.
	redBall.radius = 15;
	redBall.position =
		getRandomPosition(width, height, redBall.radius);

	// 점수를 담을 score 변수 선언 및 정의.
	int score = 0;

	// Trackbar 생성.
	cv::namedWindow("GAME");
	int mode = 0;
	cv::createTrackbar("mode", "GAME", 0, 7, on_mode_changed, (void*)&mode);

	// Game 진행.
	while (true)
	{
		// (frame : 현재 frame)
		// (gray_frame : 이전 frame 정보가 담길 객체)
		// (diff : 현재 frame과 이전 frame의 차이가 담길 객체)
		// (thresh : 이진화된 diff 정보가 담길 객체)
		cv::Mat frame, gray_frame, diff, thresh; // 흰픽셀(ball)

		// cap 영상정보를 frame에 입력.
		cap >> frame;
		if (frame.empty())
		{
			break;
		}

		// User에게 익숙한 거울모드로 설정.
		cv::flip(frame, frame, 1); // 반전

		// 움직임 감지 전 전처리.
		cv::cvtColor(frame, gray_frame, cv::COLOR_BGR2GRAY);
		cv::GaussianBlur(gray_frame, gray_frame, cv::Size(15, 15), 0);	// 15x15의 Mask로 Gaussian Blur 처리.
		if (prev_gray.empty()) {
			gray_frame.copyTo(prev_gray);
			continue;
		}

		// absdiff() 명암과 객체 분리
		cv::absdiff(prev_gray, gray_frame, diff);						// 이전 frame과 현재 frame 사이의 변경점을 diff 객체에 입력.
		cv::threshold(diff, thresh, 25.0, 255.0, cv::THRESH_BINARY);	// diff 객체 이진화. (Threshold = 25.0) (임계값을 넘는 pixel 값은 모두 255로 변경됨.)

		// 
		if (!redBall.active)
		{
			// ball 외곽선 사각형의 좌표값 설정
			int x1 = cv::max(0, redBall.position.x - redBall.radius);
			int y1 = cv::max(0, redBall.position.y - redBall.radius);
			int x2 = cv::min(width, redBall.position.x + redBall.radius);
			int y2 = cv::min(height, redBall.position.y + redBall.radius);
			// 위 좌표값을 기반으로 Rect 객체 생성.
			cv::Rect ballRect(x1, y1, x2 - x1, y2 - y1);

			// 픽셀들의 움직임을 체크
			cv::Mat roi = thresh(ballRect);									// thresh 객체에서 ballRect 부분을 관심영역으로 설정 -> 관심영역만 roi 객체에 입력.
			int movementPixels = cv::countNonZero(roi);						// roi 객체의 pixel 중 0이 아닌 pixel 들의 수를 movementPixels 에 입력. 즉, 변화된 pixel 수를 입력.
			int area = (redBall.radius * 2) * (redBall.radius * 2);			// Ball 객체가 내접하는 사각형 넓이.


			if (movementPixels > area * 0.1)											// 변화된 Pixel 수가 Ball 객체가 내접하는 사각형 넓이의 10% 이상일 때
			{
				std::cout << "터치 " << ++score << "\r\n";								// Ball 객체에 터치된 것으로 간주.
				if (mode == 7)
				{
					PlaySound(TEXT("coin_sound.wav"), NULL, SND_FILENAME | SND_ASYNC);
				}
				redBall.position = getRandomPosition(width, height, redBall.radius);	// Ball 객체의 새로운 위치를 설정.
			}
		}



		cv::Mat img = cv::imread("ref.png");
		cv::Rect faceArea(125, 50, 270, 270);
		cv::Mat face = img(faceArea);
		cv::Mat faceBall;
		cv::resize(face, faceBall, cv::Size(30, 30),0,0, cv::INTER_LANCZOS4);
		
		int x1 = cv::max(0, redBall.position.x - redBall.radius);
		int y1 = cv::max(0, redBall.position.y - redBall.radius);
		int x2 = cv::min(width, redBall.position.x + redBall.radius);
		int y2 = cv::min(height, redBall.position.y + redBall.radius);
		cv::Rect faceRect(x1, y1, x2 - x1, y2 - y1);

		switch (mode)
		{
			// Default 동작.
			case 0:														
			{
				faceBall.copyTo(frame(faceRect));
				break;
			}
			// Flip.
			case 1:
			{
				reverseFace(score, faceRect, faceBall, frame);
				break;
			}
			// Shear.
			case 2:
			{
				shearFace(score, faceRect, faceBall, frame);
				break;
			}
			// Expand.
			case 3:
			{
				expandFace(score, faceRect, faceBall, frame, redBall);
				break;
			}
			// Reduce.
			case 4:
			{
				reduceFace(score, faceRect, faceBall, frame, redBall);
				break;
			}
			// Change Color.
			case 5:
			{
				changeFaceColor(score, faceRect, faceBall, frame);
				break;
			}
			// Mophology.
			case 6:
			{
				morphologyFace(score, faceRect, faceBall, frame);
				break;
			}
			// Sound effect.
			case 7:
			{
				faceBall.copyTo(frame(faceRect));
				break;
			}
		}

		// Score 를 화면에 표시.
		cv::putText(frame, "Score : " + std::to_string(score),
			cv::Point(20, 30), cv::FONT_HERSHEY_PLAIN, 2,
			cv::Scalar(255, 255, 255), 2);

		// frame 화면에 표시.
		cv::imshow("GAME", frame);
		gray_frame.copyTo(prev_gray); // 현재 화면을 이전 화면으로 업데이트
		if (cv::waitKey(10) == 27) break;
	}
	cap.release();
	cv::destroyAllWindows();
}
