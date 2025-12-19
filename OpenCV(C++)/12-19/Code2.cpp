#include"opencv2/opencv.hpp" //현재 디렉토리
//#include <opencv2/opencv.hpp> //시스템에 찾음
void show10() {

	cv::VideoCapture capture(0); //보통 내장 카메라
	if (!capture.isOpened()) {
		std::cerr << "카메라 없음 ";
		return;
	}
	std::cout << "web cam height:" << cvRound(capture.get(cv::CAP_PROP_FRAME_HEIGHT)) << std::endl;
	std::cout << "web cam width:" << cvRound(capture.get(cv::CAP_PROP_FRAME_WIDTH)) << std::endl;

	cv::Mat screen;
	while (1) {
		capture >> screen; //cin>>처럼 생각
		if (screen.empty()) {
			std::cerr << "프레임 안들어옴" << std::endl;
			break;
		}
		cv::imshow("WEBCAM", screen);
		if (cv::waitKey(10) == 27)break; //esc 종료
	}
	screen.release();
	cv::destroyAllWindows();
}

void show11() {
	

		cv::VideoCapture capture("stopwatch.avi"); //보통 내장 카메라
		if (!capture.isOpened()) {
			std::cerr << "카메라 없음 ";
			return;
		}
		std::cout << "web cam height:" << cvRound(capture.get(cv::CAP_PROP_FRAME_HEIGHT)) << std::endl;
		std::cout << "web cam width:" << cvRound(capture.get(cv::CAP_PROP_FRAME_WIDTH)) << std::endl;
		std::cout << "web cam count:" << cvRound(capture.get(cv::CAP_PROP_FRAME_COUNT)) << std::endl;
		std::cout << "web cam fps:" << cvRound(capture.get(cv::CAP_PROP_FPS)) << std::endl;

		cv::Mat screen;
		cv::Mat inverse_screen;

		while (1) {
			capture >> screen;
			if (screen.empty()) {
				std::cerr << "프레임 안들어옴" << std::endl;
				break;
			}
			inverse_screen = ~screen;
			if (inverse_screen.empty()) {
				std::cerr << "역프레임 안들어옴" << std::endl;
				break;
			}
			cv::imshow("MOVE", screen);
			cv::imshow("REVERS_MOVE",inverse_screen);
			if (cv::waitKey(10) == 27)break; //esc 종료
		}
		screen.release();
		inverse_screen.release();
		cv::destroyAllWindows();
	
}