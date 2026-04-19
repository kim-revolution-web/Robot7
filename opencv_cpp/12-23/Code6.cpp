#include"opencv2/opencv.hpp"

void show33() {
	//픽셀 바꿀때만 그레이 스케일
	cv::Mat src{ cv::imread("tekapo.bmp") };
	cv::imshow("SRC", src);
	cv::Point2f srcPts[3];
	cv::Point2f dstPts[3];
	srcPts[0] = cv::Point2f(0, 0);
	srcPts[1] = cv::Point2f(src.cols -1.0f, 0.0f);
	srcPts[2] = cv::Point2f(src.cols - 1.0f, src.rows - 1.0f);
	dstPts[0] = cv::Point2f(50.0f, 50.0f);
	dstPts[1] = cv::Point2f(src.cols - 100.0f, 100.0f);
	dstPts[2] = cv::Point2f(src.cols - 50.0f, src.rows - 50.0f);

	cv::Mat dst;
	cv::Mat M = cv::getAffineTransform(srcPts, dstPts);
	cv::warpAffine(src, dst, M, src.size());

	cv::imshow("dst", dst);
	cv::waitKey();
	cv::destroyAllWindows();
}