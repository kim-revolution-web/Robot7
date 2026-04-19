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

void show3() {

	cv::Mat img3=cv::Mat::zeros(512, 512, CV_8UC1); //0도 검정
	cv::Mat img2 = cv::Mat::ones(512, 512, CV_8UC1)*255; //1도 검정
	cv::Mat img1 = cv::Mat::eye(512, 512, CV_8UC1)*255; //항등 행렬
	cv::namedWindow("window1");
	cv::imshow("window1", img1);
	cv::namedWindow("window2");
	cv::imshow("window2", img2);
	cv::namedWindow("window3");
	cv::imshow("window3", img3);
	cv::waitKey();
	/*cv::destroyWindow("window");*/
	cv::destroyAllWindows();
}

void show4() {

	cv::Mat dog1= cv::imread("dog.bmp");

	if (dog1.empty()) {
		std::cerr << "개 사진없음";
		return;
	}
	
	cv::Mat dog2 = dog1.clone(); //깊은 복사

	cv::Mat dog3; //깊은 복사
	dog1.copyTo(dog3);

	cv::Mat img4 = dog1; //copy constructor 복사 //얇은 복사 속도 빠름 

	cv::Mat rot;
	cv::rotate(dog1, rot, cv::ROTATE_90_CLOCKWISE);
	
	dog1.setTo(cv::Scalar(0, 255, 255));

	cv::namedWindow("dog1");
	cv::imshow("dog1", dog1);

	cv::namedWindow("clonedog");
	cv::imshow("clonedog", dog2);

	cv::namedWindow("copydog");
	cv::imshow("copydog",dog3);

	cv::imshow("img4", img4);
	cv::imshow("rot", rot);

	cv::waitKey();
	cv::destroyAllWindows();
}

void show5() {

	cv::Mat img1 = cv::imread("cat.bmp");
	if (img1.empty()) {
		std::cerr << "고양이없다";
		return;
	}
	cv::Mat img2=~img1;//색상 반전

	cv::Mat img3 = img1(cv::Rect(220, 120, 340, 240));//원하는 영역을 자른다

	cv::namedWindow("cat");
	cv::imshow("cat", img1);
	cv::namedWindow("~cat");
	cv::imshow("~cat", img2);

	cv::imshow("cat3", img3);
	cv::waitKey();
	cv::destroyAllWindows();

}

void show6() {

	cv::Mat img1 = cv::Mat::zeros(256,256, CV_8UC1); //512,512
	uchar value = 0;

	for (int i = 0; i < img1.rows; i++) {
		for (int j = 0; j < img1.cols; j++){
			++value;
			img1.at<uchar>(i, j) = value;
		}
	}
	cv::namedWindow("at");
	cv::imshow("at", img1);
	cv::waitKey();
	cv::destroyAllWindows();
}

void show7() {

	cv::Mat img1 = cv::imread("coins.png", cv::IMREAD_UNCHANGED);
	if (img1.empty()) {
		return;
	}
	std::cout << "이미지 폭:" << img1.cols << std::endl;
	std::cout << "이미지 높이:" << img1.rows << std::endl;
	std::cout << "이미지 사이즈:" << img1.size() << std::endl;
	std::cout << "픽셀의 한개 사이즈:" << img1.elemSize() << std::endl;
	std::cout << "채널:" << img1.channels() << std::endl;

	if (img1.type() == CV_8UC1)std::cout << "그레이" << std::endl;
	else if (img1.type()== CV_8UC3)std::cout << "컬러" << std::endl;
	else { std::cout << "PNG" << std::endl; }

	cv::namedWindow("c");
	cv::imshow("c", img1);
	cv::waitKey();
	cv::destroyAllWindows();
}

void show8() {

	float data[] = { 1.0f,2.0f,3.0f,4.0f };
	cv::Mat mat1(2, 2, CV_32FC1, data);
	cv::Mat mat2=mat1.inv();
	cv::Mat mat3=mat1* mat2;
	std::cout << mat1 << std::endl;
	std::cout << mat2 << std::endl;
	std::cout << mat3 << std::endl;

	float dat[] = { 1.0f,2.0f,3.0f,1.0f,5.0f,7.0f,8.0f,8.0f,8.0f };
	cv::Mat ma1(3, 3, CV_32FC1, dat);
	cv::Mat ma2 = ma1.inv();
	cv::Mat ma3 = ma1 * ma2;
	std::cout << ma1 << std::endl;
	std::cout << ma2 << std::endl;
	std::cout << ma3 << std::endl;

	uchar data2[] = { 1,2,3,4,5,6,7,8,9,10,11,12 };
	cv::Mat mat4(3, 4, CV_8UC1, data2);
	std::cout << mat4 << std::endl;
	cv::Mat mat5 = mat4.reshape(0.4);
	std::cout << mat5 << std::endl;

	cv::Mat img1=cv::imread("lena.jpg",cv::IMREAD_GRAYSCALE);
	cv::namedWindow("lena1");
	cv::imshow("lena1", img1);
	cv::Mat img2 = img1 + 50;
	cv::namedWindow("lena2");
	cv::imshow("lena2", img2);
	cv::Mat img3 = img1.t();
	cv::namedWindow("lena3");
	cv::imshow("lena3", img3);
	
	cv::waitKey();
	cv::destroyAllWindows();
}


void printMat(cv::InputArray _mat) //cv::mat 타입이 같거나 부모클래스라 받아줄수 있다
{
	cv::Mat mat = _mat.getMat();
	std::cout << mat << std::endl;
}

void inputArrayOF() {

	uchar data1[] = { 1,2,3,4,5,6 };
	cv::Mat mat1(2, 3, CV_8U, data1);
	printMat(mat1);
}

void show9() {
	inputArrayOF();


}
