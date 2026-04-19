#include "opencv2/opencv.hpp"
#include <iostream>
#include <vector>

void show45() {

	cv::Mat src = cv::imread("butterfly.jpg", cv::IMREAD_COLOR);
	cv::imshow("SRC", src);

	cv::Mat B(src.size(), CV_8UC1);
	cv::Mat G(src.size(), CV_8UC1);
	cv::Mat R(src.size(), CV_8UC1);

	for (int i = 0; i < src.rows; ++i) 
	{
		for (int j = 0; j < src.cols; ++j) 
		{
			cv::Vec3b& p1 = src.at<cv::Vec3b>(i, j);
			uchar& p_b = B.at<uchar>(i, j);
			p_b = p1[0];
			uchar& p_g = G.at<uchar>(i, j);
			p_g = p1[1];
			uchar& p_r = R.at<uchar>(i, j);
			p_r = p1[2];

			/*B.at<uchar>(i, j) = p1[0];
			G.at<uchar>(i, j) = p1[1];
			R.at<uchar>(i, j) = p1[2];*/

		}
	}
	cv::imshow("Blue channel", B);
	cv::imshow("Green channel", G);
	cv::imshow("Red channel", R);
	cv::waitKey();
	cv::destroyAllWindows();

}

void show46() {

	cv::Mat src = cv::imread("candied.png",cv::IMREAD_UNCHANGED);//png는 UNCHANGED 써야 4채널써야 한다
	std::vector<cv::Mat>bgr_plans;
	cv::split(src,bgr_plans);
	std::cout << std::size(bgr_plans) << std::endl;

	cv::imshow("SRC", src);
	cv::imshow("Blue", bgr_plans[0]);
	cv::imshow("Green", bgr_plans[1]);
	cv::imshow("Red", bgr_plans[2]);
	cv::waitKey();
	cv::destroyAllWindows();

}

static void on_hue_change(int, void*);//한수의 proto type
static cv::Mat src;
static cv::Mat src_hsv;
static int lower_bound = 0;
static int upper_bound = 0;
static cv::Mat mask;

void show47() 
{
	src = cv::imread("candies.png");
	cv::cvtColor(src, src_hsv, cv::COLOR_BGR2HSV);
	cv::namedWindow("SRC");
	cv::createTrackbar("LOWER_HUE","SRC" ,&lower_bound,179,on_hue_change);
	cv::createTrackbar("UPPER_HUE", "SRC", &upper_bound, 179, on_hue_change);
	cv::imshow("CANDIES", src);
	cv::waitKey();
	cv::destroyAllWindows();
}

void on_hue_change(int, void*) {
	cv::Scalar lower(lower_bound, 150, 0); //s> 150 ,v>0
	cv::Scalar upper(upper_bound, 255, 255); // s<255 , v<255
	cv::inRange(src_hsv, lower, upper, mask);
	cv::imshow("SRC", mask);
}