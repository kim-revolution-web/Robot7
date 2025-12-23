#include "opencv2/opencv.hpp"


void show20() {

	cv::Mat src = cv::imread("lena.jpg", cv::IMREAD_GRAYSCALE);
	cv::Mat dst = src + 100;
	cv::Mat dst2(src.size(), src.type());
	for (int i = 0; i < src.rows; ++i)
	{
		for (int j = 0; j < src.cols; ++j) {
			dst2.at<uchar>(i,j) = src.at<uchar>(i,j) + 100;
		}
	}
	cv::imshow("SRC", src);
	cv::imshow("dst", dst);
	cv::imshow("dst2", dst2);
	cv::waitKey();
	cv::destroyAllWindows();

}


void on_brightness(int position, void* userdata)
{
	std::cout << "Trackbar" << std::endl;
	cv::Mat src=*(cv::Mat*)userdata;
	cv::Mat dst = src + position;
	cv::imshow("dst", dst);
}

void show21() {

	cv::Mat src = cv::imread("lena.jpg", cv::IMREAD_GRAYSCALE);
	cv::namedWindow("dst");
	//cv::imshow("dst", src);
	cv::createTrackbar("Brightness", "dst", 0, 100, on_brightness,(void*)&src);

	cv::waitKey(0);
	cv::destroyAllWindows();
}

void show22() {

	cv::Mat src = cv::imread("lena.jpg", cv::IMREAD_GRAYSCALE);
	float alpha = 1.0f;
	cv::Mat dst = (1 + alpha) * src - 128 * alpha;
	cv::imshow("SRC", src);
	cv::imshow("DST", dst);
	cv::waitKey();
	cv::destroyAllWindows();
}

void show23() {

	cv::Mat src = cv::imread("hawkes.bmp", cv::IMREAD_GRAYSCALE);
	double min, max = 0.0; //여기 값을 바꿔 주려고 밑에서 &를 해주는 것이다.
	cv::minMaxLoc(src, &min, &max);
	cv::Mat dst=(src - min) * 255 / (max - min);
	cv::imshow("src", src);
	cv::imshow("dst", dst);
	cv::waitKey();
	cv::destroyAllWindows();

}