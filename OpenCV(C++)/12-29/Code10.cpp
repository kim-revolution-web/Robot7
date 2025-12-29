#include <opencv2/opencv.hpp>
#include<iostream>
void show51() {

	uchar data[] = {
	0,0,1,1,0,0,0,0,
	1,1,1,1,0,0,2,0,
	1,1,1,1,0,0,0,0,
	0,0,0,0,0,3,3,0,
	0,0,0,3,3,3,3,0,
	0,0,0,3,0,0,3,0,
	0,0,3,3,3,3,3,0,
	0,0,0,0,0,0,0,0
	};

	cv::Mat src(8, 8, CV_8UC1, data);
	cv::Mat dst = src * 255;
	cv::Mat label;
	int count = cv::connectedComponents(dst, label);
	std::cout << "Source:\r\n" << src << "\r\n";
	std::cout << "DST :\r\n" << src << "\r\n";
	std::cout << "LABEL :\r\n" << src << "\r\n";
	std::cout << "찾은 객체 수는  :\r\n" << src << "\r\n";



	cv::imshow("dst", dst);
	cv::waitKey();
	cv::destroyAllWindows();
}

void show52() {
	
	const auto src = cv::imread("contours.bmp", cv::IMREAD_GRAYSCALE);
	std::vector<std::vector<cv::Point>>contours;
	cv::findContours(src,contours,cv::RETR_LIST,cv::CHAIN_APPROX_NONE);
	cv::Mat dst;
	cv::cvtColor(src, dst, cv::COLOR_GRAY2BGR);
	int counting = 0;
	for (auto it = contours.begin(); it != contours.end();++it) {
		cv::Scalar c(rand() & 255, rand() & 255, rand() & 255);
		cv::drawContours(dst, contours, counting++, c, 2);
	}
	std::cout << "찾은 개수 :" << counting << "\r\n";
		cv::imshow("SRC", src);
		cv::imshow("DST", dst);
		cv::waitKey();
		cv::destroyAllWindows();
}