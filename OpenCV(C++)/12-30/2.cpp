#include "opencv2/opencv.hpp"

void show100() {
	cv::Mat img1 = cv::imread("ka.jpg");
	cv::Mat img2 = img1(cv::Rect(100, 50, 400, 500));
	cv::Mat dst = cv::imread("field.bmp");

	cv::Mat mask;
	cv::cvtColor(img2,mask, cv::COLOR_RGB2GRAY);
	cv::threshold(mask, mask, 0, 255, cv::THRESH_BINARY | cv::THRESH_OTSU);
	
	cv::Mat img3;
	cv::resize(img2, img3, cv::Size(50, 50)); //크기줄임

	//600X400
	cv::resize(img2, img2, cv::Size(600,400));
	cv::resize(mask, mask, cv::Size(600, 400));

	img2.copyTo(dst, ~mask);
	//cv::Mat dst1, dst2, dst3, dst4;
	//bitwise_or(mask, ~mask, dst1);
	cv::VideoCapture cap(0);
	if (!cap.isOpened()) {
		std::cerr << "NO CAM" << "\n";
		return;
	}
	cv::Mat frame;
	while (1) {
		cap >> frame;
		if (frame.empty())
			break;

		cv::imshow("frame", frame);

		if (cv::waitKey(10) == 27)
			break;
	}

	

	
	cv::imshow("img1", img1);
	cv::imshow("mask", mask);
	cv::imshow("dst", dst);
	
	
	//cv::waitKey();
	cv::destroyAllWindows();
}

