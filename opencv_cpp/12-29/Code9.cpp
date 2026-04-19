#include <opencv2/opencv.hpp>

static void on_thread(int, void*);
//as 디텍션이랑 비슷함
void show48()
{
	cv::Mat src = cv::imread("neutrophils.png", cv::IMREAD_GRAYSCALE); //이진화 하려면 그레이
	cv::namedWindow("SRC");
	cv::namedWindow("DST");
	cv::imshow("SRC", src);

	cv::createTrackbar("Threshold", "DST", 0, 255, on_thread, (void*)&src);
	//처음 시작할때 중간에
	cv::setTrackbarPos("Threshold", "DST",128);
	cv::waitKey();
	cv::destroyAllWindows();
	
}

void on_thread(int position, void*userdata) {

	cv::Mat src=*(static_cast<cv::Mat*>(userdata));
	cv::Mat dst;
	cv::threshold(src, dst, position, 255.0, cv::THRESH_BINARY);
	cv::imshow("DST", dst);
}

//---------------------------------------------
static void on_trackbar(int position, void* userdata) 
{
 cv::Mat *src = (static_cast<cv::Mat*>(userdata));
 int block_size = position;
 if (block_size % 2 == 0) --block_size;// block size 홀수 가 좋다.
 if (block_size < 3) block_size = 3; //최소 3이상 이어야 한다.
 cv::Mat dst;
 cv::adaptiveThreshold(*src,dst,255,
	 cv::ADAPTIVE_THRESH_GAUSSIAN_C,cv::THRESH_BINARY,// 가우시안 사용 가우시안 사용시 5.0tkdyd
	 block_size,5.0);
 cv::imshow("DST", dst);

}
void show49() {

	cv::Mat src = cv::imread("sudoku.jpg", cv::IMREAD_GRAYSCALE);
	cv::imshow("sudoku", src);
	cv::namedWindow("DST");
	cv::createTrackbar("Blocksize", "DST", 0, 200, on_trackbar, (void*)&src);

	cv::waitKey();
	cv::destroyAllWindows();
}

void show50() {
	

	auto src = cv::imread("milkdrop.bmp", cv::IMREAD_GRAYSCALE);
	//모폴로지 를 하려면 
	cv::Mat binary_image;
	cv::threshold(src, binary_image, 0.0, 255.0, cv::THRESH_BINARY | cv::THRESH_OTSU);
	cv::Mat dst_open;
	for (int i = 0; i < 5; i++) {
		cv::morphologyEx(binary_image, dst_open, cv::MORPH_OPEN, cv::Mat());  //기본이 3X3 침식->팽창
	}
	
	cv::Mat dst_close;
	for (int i = 0; i < 5; i++) {
		cv::morphologyEx(binary_image, dst_close, cv::MORPH_CLOSE, cv::Mat()); //기본이 3X3 팽창 -> 침식 
	}
	
	cv::imshow("SRC",src);
	cv::imshow("Bianry", binary_image);
	cv::imshow("OPEN", dst_open);
	cv::imshow("CLOSE", dst_close);

	cv::waitKey();
	cv::destroyAllWindows();
}