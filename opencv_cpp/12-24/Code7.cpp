#include"opencv2/opencv.hpp"

void show41() {

	cv::Mat src = cv::imread("lenna.png", cv::IMREAD_GRAYSCALE);
	cv::Mat dx;// x성분의 미분
	cv::Mat dy;// y성분의 미분
	cv::Mat dxy;
	cv::Sobel(src, dx, CV_32FC1, 1, 0);//dx만 하겠다.
	cv::Sobel(src, dy, CV_32FC1, 0, 1);
	cv::Sobel(src, dxy, CV_32FC1, 1, 1);
	cv::imshow("SRC", src);
	cv::imshow("dx", dx);
	cv::imshow("dy", dy);
	cv::imshow("dxy", dxy);
	cv::Mat mag;//크기를 볼 Matrix
	cv::magnitude(dx, dy, mag); //abs절대 값
	mag.convertTo(mag, CV_8UC1);
	cv::imshow("Mag", mag);
	//임계값
	cv::Mat real_edge;
	real_edge = mag >= 170;
	cv::imshow("real_edge", real_edge);
	cv::waitKey();
	cv::destroyAllWindows();

}

void show42()
{
	cv::Mat src = cv::imread("lenna.png", cv::IMREAD_IGNORE_ORIENTATION);
	cv::Mat dst1;
	cv::Mat dst2;

	cv::Canny(src, dst1, 50, 100); //50~100 낮으면 검출이 많아서 다른것이 많이 들어온다
	cv::Canny(src, dst2, 50, 230); //50~150
	cv::imshow("SRC", src);
	cv::imshow("DST1", dst1);
	cv::imshow("DST2", dst2);
	cv::waitKey();
	cv::destroyAllWindows();
}

void show43() {

	cv::Mat src = cv::imread("building.jpg", cv::IMREAD_GRAYSCALE);
	cv::imshow("SRC", src);
	cv::Mat edges;
	cv::Canny(src, edges, 50, 150);
	cv::imshow("edges", edges);
	std::vector<cv::Vec2f>lines;

	cv::HoughLines(edges, lines, 1.0, CV_PI / 180, 250);//rho, theta, thresdsold

	//선 좌표 찾기

	/*for (int i = 0; i < lines.size(); i++) {
		std::cout << lines[i] << std::endl;
	}*/
	//찾은 선을 그려준다 이건 정해진 방식틀대로 하는것이다
	cv::Mat dst;
	cv::cvtColor(edges, dst, cv::COLOR_GRAY2BGR);
	for (int i = 0; i < lines.size(); i++)
	{

		float r = lines[i][0];
		float t = lines[i][1];
		double cos_t = cos(t);
		double sin_t = sin(t);
		double x0 = r * cos(t);
		double y0 = r * sin(t);
		cv::Point pt1(cvRound(x0 + 1000 * (-sin_t)),
			cvRound(y0 + 1000 * cos_t));
		cv::Point pt2(cvRound(x0 - 1000 * (-sin_t)),
			cvRound(y0 - 1000 * cos_t));
	cv:line(dst, pt1, pt2, cv::Scalar(0, 0, 255), 2);


	}
	cv::imshow("dst", dst);

	cv::waitKey();
	cv::destroyAllWindows();

}

void show44() {

	cv::Mat src = cv::imread("coins3.jpg", cv::IMREAD_GRAYSCALE);
	std::vector<cv::Vec3f>circles;
	cv::Mat blurred;
	cv::blur(src,blurred, cv::Size(3, 3));
	cv::Mat dst;
	cv::HoughCircles(blurred, circles,cv::HOUGH_GRADIENT,1,5,275.5,95.5);
	cv::cvtColor(blurred,dst,cv::COLOR_GRAY2BGR);
	for (auto&& circle : circles) {
		cv::Point center(cvRound(circle[0]),
			cvRound(circle[1]));
			int radius = cvRound(circle[2]);
			cv::circle(dst, center, radius, cv::Scalar(0, 0, 255),2);

	}

	cv::imshow("dst", dst);
	cv::waitKey();
	cv::destroyAllWindows();

}