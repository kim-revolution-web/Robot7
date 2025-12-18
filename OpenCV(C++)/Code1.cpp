#include"opencv2/opencv.hpp"

void show1() {
	cv::Mat image1 = cv::imread("lena.jpg");
	cv::Mat image2 = cv::imread("ka.jpg");
	cv::Mat image3; // 픽셀을 for문으러 전부 끌어오는 거
	if (image1.empty() || image2.empty())
	{
		std::cerr << "파일들이 없습니다." << "\n";
		return;
	}
	image3 = image1.clone();//clone 으로 복사하다
	std::cout << "몇차원 : " << image1.dims << "\n";
	std::cout << "컬럼 : " << image1.cols << "\n";
	std::cout << "행(row) :" << image1.rows << "\n";
	cv::namedWindow("lena");
	cv::imshow("lena", image1);
	std::cout << "몇차원 ?" << image2.dims << "\n";
	std::cout << "컬럼 ?" << image2.cols << "\n";
	std::cout << "행(row) ?" << image2.rows << "\n";
	cv::namedWindow("ka");
	cv::imshow("ka", image2);
	std::cout << "몇차원 :" << image3.dims << "\n";
	std::cout << "컬럼 :" << image3.cols << "\n";
	std::cout << "행(row) :" << image3.rows << "\n";
	cv::namedWindow("lena1");
	cv::imshow("lena1", image3);
	cv::waitKey(0); //쓰레드가 안꺼지게 정지해줌
	cv::destroyAllWindows(); // 전부 닫아줘
}

void show2() {
	cv::namedWindow("Color");
	//for (int i = 0; i < 256; i++) {
	//	cv::Mat image(512, 512, CV_8UC3, cv::Scalar(i, 0, 0)); //8u 8bite c3 chennel 3개 /bgr
	//	cv::imshow("Color", image);
	//	cv::waitKey(10);
	//}
	//
	//for (int i = 255; i >0; i--) {
	//	cv::Mat image(512, 512, CV_8UC3, cv::Scalar(0, i, 0)); //8u 8bite c3 chennel 3개 /bgr
	//	cv::imshow("Color", image);
	//	cv::waitKey(10);
	//}
	//
	//for (int i = 0; i < 256; i+20) {
	//	for (int j = 0; j < 256; j+20) {
	//		for (int k = 0; k < 256; k+20) {
	//			cv::Mat image(512, 512, CV_8UC3, cv::Scalar(i, j, k));
	//			cv::imshow("Color", image);
	//			if(cv::waitKey(10)==27)return;
	//		}
	//	}
	//}

	//int b = 0, g = 0, r = 0;
	//cv::Mat image(512, 512, CV_8UC3);

	//cv::namedWindow("Color");
	//cv::createTrackbar("B", "Color", &b, 255);
	//cv::createTrackbar("G", "Color", &g, 255);
	//cv::createTrackbar("R", "Color", &r, 255);

	//while (true) {
	//	image.setTo(cv::Scalar(b, g, r));
	//	cv::imshow("Color", image);
	//	if (cv::waitKey(30) == 27) break; // ESC
	//}

	cv::Mat image2(cv::Size(512, 512), CV_8UC1);
	cv::imshow("Color2", image2);
	cv::waitKey(0);
	cv::destroyAllWindows();
}
