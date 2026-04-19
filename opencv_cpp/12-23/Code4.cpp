#include "opencv2/opencv.hpp"

void show24()
{
	cv::Mat img1 = cv::imread("lenna256.bmp", cv::IMREAD_GRAYSCALE);
	cv::Mat img2 = cv::imread("square.bmp", cv::IMREAD_GRAYSCALE);
	cv::Mat dst1 = img1 + img2;  //saturate: 포화상태가 된다.
	cv::Mat dst2 = img1 - img2; //더큰 값으로 나옴
	cv::Mat dst3(256, 256, CV_8UC1);
	for (int i = 0; i < 256; ++i) {
		for (int j = 0; j < 256; ++j) {
			dst3.at<uchar>(i, j) = cv::saturate_cast<uchar>(img1.at<uchar>(i, j) + img2.at<uchar>(i, j)); //형변환
			//dst3.at<uchar>(i, j) = img1.at<uchar>(i, j) + img2.at<uchar>(i, j);
		}
	}
	cv::imshow("dst1", dst1);
	cv::imshow("dst2", dst2);
	cv::imshow("dst3", dst3);
	cv::imshow("img1", img1);
	cv::imshow("img2", img2);


	cv::waitKey(0);
	cv::destroyAllWindows();

	return;
}

void show24_1()
{
	cv::Mat img1 = cv::imread("ka.jpg", cv::IMREAD_GRAYSCALE);
	cv::Mat img2 = cv::imread("square.bmp", cv::IMREAD_GRAYSCALE);

	if (img1.empty() || img2.empty()) {
		std::cout << "이미지 로드 실패\n";
		return;
	}

	if (img1.size() != img2.size()) {
		cv::resize(img2, img2, img1.size()); // 크기 맞추기
	}

	cv::Mat dst1 = img1 + img2;  // saturate(포화 덧셈)
	cv::Mat dst2 = img1 - img2;  // saturate(포화 뺄셈)

	cv::imshow("img1", img1);
	cv::imshow("img2", img2);
	cv::imshow("dst_add", dst1);
	cv::imshow("dst_sub", dst2);

	cv::waitKey(0);
	cv::destroyAllWindows();
}

void show25() {

	cv::Mat img1 = cv::imread("lenna256.bmp", cv::IMREAD_GRAYSCALE);
	cv::Mat img2 = cv::imread("square.bmp", cv::IMREAD_GRAYSCALE);
	cv::Mat dst1;
	cv::Mat dst2;
	cv::Mat dst3;
	cv::add(img1, img2, dst1);
	cv::subtract(img1, img2, dst2);
	cv:absdiff(img1, img2, dst3); //절대 값 빼기 똑같은거 남기고 다른거 벌린다 


	cv::imshow("img1",img1);
	cv::imshow("img2", img2);
	cv::imshow("dst1",dst1);
	cv::imshow("dst2", dst2);
	cv::imshow("dst3", dst3);
	cv::waitKey(0);
	cv::destroyAllWindows();


}