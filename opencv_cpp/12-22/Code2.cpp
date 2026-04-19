#include"opencv2/opencv.hpp" //현재 디렉토리
//#include <opencv2/opencv.hpp> //시스템에 찾음
void show10() {

	cv::VideoCapture capture(0); //보통 내장 카메라
	if (!capture.isOpened()) {
		std::cerr << "카메라 없음 ";
		return;
	}
	std::cout << "web cam height:" << cvRound(capture.get(cv::CAP_PROP_FRAME_HEIGHT)) << std::endl;
	std::cout << "web cam width:" << cvRound(capture.get(cv::CAP_PROP_FRAME_WIDTH)) << std::endl;

	cv::Mat screen;
	while (1) {
		capture >> screen; //cin>>처럼 생각
		if (screen.empty()) {
			std::cerr << "프레임 안들어옴" << std::endl;
			break;
		}
		cv::imshow("WEBCAM", screen);
		if (cv::waitKey(10) == 27)break; //esc 종료
	}
	screen.release();
	cv::destroyAllWindows();
}

void show11() {


	cv::VideoCapture capture("stopwatch.avi"); //보통 내장 카메라
	if (!capture.isOpened()) {
		std::cerr << "카메라 없음 ";
		return;
	}
	std::cout << "web cam height:" << cvRound(capture.get(cv::CAP_PROP_FRAME_HEIGHT)) << std::endl;
	std::cout << "web cam width:" << cvRound(capture.get(cv::CAP_PROP_FRAME_WIDTH)) << std::endl;
	std::cout << "web cam count:" << cvRound(capture.get(cv::CAP_PROP_FRAME_COUNT)) << std::endl;
	std::cout << "web cam fps:" << cvRound(capture.get(cv::CAP_PROP_FPS)) << std::endl;

	cv::Mat screen;
	cv::Mat inverse_screen;

	while (1) {
		capture >> screen;
		if (screen.empty()) {
			std::cerr << "프레임 안들어옴" << std::endl;
			break;
		}
		inverse_screen = ~screen;
		if (inverse_screen.empty()) {
			std::cerr << "역프레임 안들어옴" << '\n';// std::endl;
			break;
		}
		cv::imshow("MOVE", screen);
		cv::imshow("REVERS_MOVE", inverse_screen);
		if (cv::waitKey(10) == 27)break; //esc 종료
	}
	capture.release();
	inverse_screen.release();
	cv::destroyAllWindows();

}

//안됨
void show12() {

	cv::VideoCapture cap(0);//VidioCapture  생성자 호출
	if (!cap.isOpened()) {
		std::cerr << "웹캠이없습니다." << "\n";
		return;
	}
	double fps = cvRound(cap.get(cv::CAP_PROP_FPS));
	//코덱을 선택
	int width = cvRound(cap.get(cv::CAP_PROP_FRAME_WIDTH));
	int height = cvRound(cap.get(cv::CAP_PROP_FRAME_WIDTH));
	int fourcc = cv::VideoWriter::fourcc('D', 'I', 'V', 'X');
	int delay = cvRound(1000 / fps);
	cv::VideoWriter outputVideo("output.avi", fourcc, 30, cv::Size(width, height));
	//cv::VideoWriter outputVideo("output.avi", fourcc, fps, cv::Size(300, 300));
	cv::Mat screen;
	while (true) {

		cap >> screen;
		outputVideo << screen;
		cv::imshow("VIDEO", screen);
		if (cv::waitKey(10) == 27)break;

	}
	cap.release();
	cv::destroyAllWindows();



}

void show12_1() {
	cv::VideoCapture cap(0);
	if (!cap.isOpened()) {
		std::cerr << "웹캠이 없습니다.\n";
		return;
	}

	// FPS 가져오기 (0 나오면 기본값)
	double fps = cap.get(cv::CAP_PROP_FPS);
	if (fps <= 1.0) fps = 30.0;

	cv::Size outSize(300, 300);
	int fourcc = cv::VideoWriter::fourcc('m', 'p', '4', 'v');

	cv::VideoWriter writer("output.mp4", fourcc, fps, outSize, true);
	if (!writer.isOpened()) {
		std::cerr << "VideoWriter 열기 실패(코덱/경로/권한 문제)\n";
		return;
	}

	cv::Mat frame, resized;
	while (true) {
		cap >> frame;
		if (frame.empty()) break;

		cv::resize(frame, resized, outSize);   
		writer.write(resized);

		cv::imshow("VIDEO", resized);
		if (cv::waitKey(1) == 27) break; // ESC
	}

	writer.release();   
	cap.release();
	cv::destroyAllWindows();
}

void show13() {

	cv::Mat canvas(600, 600, CV_8UC4,cv::Scalar(255,255,255));
	cv::line(canvas, cv::Point(50, 150),
		cv::Point(250, 150), cv::Scalar(0, 0, 255),10);

	cv::line(canvas, cv::Point(250, 150),
		cv::Point(100, 250), cv::Scalar(0, 0, 255), 10);

	cv::line(canvas, cv::Point(100, 250),
		cv::Point(150, 50), cv::Scalar(0, 0, 255), 10);

	cv::line(canvas, cv::Point(150, 50),
		cv::Point(200, 250), cv::Scalar(0, 0, 255), 10);

	cv::line(canvas, cv::Point(200, 250),
		cv::Point(50, 150), cv::Scalar(0, 0, 255), 10);

	cv::arrowedLine(canvas, cv::Point(50, 200),
		cv::Point(150, 150), cv::Scalar(0, 255, 255), 10);
	cv::drawMarker(canvas, cv::Point(30, 350)
		,cv::Scalar(255, 0, 255));



	cv::imshow("canvas", canvas);
	cv::waitKey(0);

	cv::destroyAllWindows();
}

void show14() {
	cv::Mat canvas(600, 600, CV_8UC3, cv::Scalar(255, 255, 255));
	cv::line(canvas, cv::Point(50, 150),
		cv::Point(250, 150), cv::Scalar(0, 0, 255), 10);
	
	cv::circle(canvas, cv::Point(300, 300), 60, cv::Scalar(255, 0, 0));

	std::vector<cv::Point> points;//컨테이너 데이터
	points.push_back(cv::Point(250, 250));
	points.push_back(cv::Point(300, 250));
	points.push_back(cv::Point(300, 300));
	points.push_back(cv::Point(350, 300));
	points.push_back(cv::Point(350, 350));
	points.push_back(cv::Point(250, 350));

	cv::polylines(canvas,points,true,cv::Scalar(0,255,255),2);

	cv::putText(canvas, "I LOVE YOU",
		cv::Point(20, 50), cv::FONT_HERSHEY_PLAIN,
		1.0,cv::Scalar(0,0,255));

	cv::imshow("canvas", canvas);
	cv::waitKey(0);

	cv::destroyAllWindows();
}

void show15() {

	cv::Mat img = cv::imread("ka.jpg");
	cv::imshow("ka",img);
	while (1) {

		int key_value = cv::waitKey(0);
		std::cout << "input key is" << key_value << "\n";
			if (key_value == 'i' || key_value == 'I') {
				img = ~img;
				cv::imshow("inv_ka", img);
			}
			else if (key_value == 'q' or key_value == 27) {
				std::cout << "종료" << std::endl;
				break;
			}

	}
	cv::destroyAllWindows();

}


static cv::Point old_pt;
static cv::Mat img;

void on_mouse(int mouse_event, int mouse_x, int mouse_y, int flag, void* userdata) 
{
	std::cout << "마우스 클릭" << "\n";
	switch (mouse_event) 
	{
	case cv::EVENT_LBUTTONDOWN://1
		std::cout << "왼쪽 버튼 클릭" << std::endl;
		old_pt = cv::Point(mouse_x, mouse_y); //시작
			break;
	case cv::EVENT_LBUTTONUP://4
		std::cout << "왼쪽 버튼 놓을때클릭" << std::endl;
		break;
	case cv::EVENT_MOUSEMOVE://0
		std::cout << "마우스 움직일때 " << std::endl;
		if (flag & cv::EVENT_FLAG_LBUTTON) {
			cv::line(img, old_pt, cv::Point(mouse_x, mouse_y), //끝지점?
				cv::Scalar(0, 255, 255),2);
			cv::imshow("karina", img);
			old_pt = cv::Point(mouse_x, mouse_y); //다시시작?
		}
		break;
	}
}

void show16() {

	img = cv::imread("ka.jpg");
	if (img.empty())return;
	cv::namedWindow("karina");
	cv::imshow("karina", img);
	
	cv::setMouseCallback("karina",on_mouse);// 함수를 등록하고 사용 함수가 리턴이 되야 끝난다

	cv::waitKey(0);
	//cv::destroyAllWindows();
}



void on_level_changed(int position, void* userdata)
{
	//cv::Mat img = *(cv::Mat*)userdata; //old c-style
	cv::Mat img = *(static_cast<cv::Mat*>(userdata));//safety
	img.setTo(position * 16);
	cv::imshow("CANVAS", img);
}
void show17() {

	cv::Mat canvas(800, 800, CV_8UC1);//grayscale
	cv::namedWindow("CANVAS");
	cv::createTrackbar("Level","CANVAS",0,16,
	on_level_changed,(void*)&canvas);
	cv::waitKey();
	cv::destroyAllWindows;
}

//안나옴
void show18() 
{
	cv::Mat scr = cv::imread("lena.jpg");
	cv::Mat mask = cv::imread("mask_smile.bmp");
	scr.setTo(cv::Scalar(0, 255, 0), mask);
	cv::imshow("lena",scr);
	cv::imshow("mask",mask);
	cv::waitKey();
	cv::destroyAllWindows();

}

void show18_1()
{
	cv::Mat scr = cv::imread("lena.jpg");
	cv::Mat mask = cv::imread("mask_smile.bmp", cv::IMREAD_GRAYSCALE); 

	if (scr.empty() || mask.empty()) return;

	if (mask.size() != scr.size())
		cv::resize(mask, mask, scr.size());  

	scr.setTo(cv::Scalar(0, 255, 0), mask);  

	cv::imshow("lena", scr);
	cv::imshow("mask", mask);
	cv::waitKey();
	cv::destroyAllWindows();
}

void show19() {
	cv::Mat scr = cv::imread("airplane.bmp");
	cv::Mat mask = cv::imread("mask_plane.bmp");
	cv::Mat dst = cv::imread("field.bmp");
	cv::Scalar total_pixel = cv::sum(scr);
	std::cout << "총픽셀은:" << total_pixel(0) << "\n";

	cv::imshow("dst", dst);

	scr.copyTo(dst, mask);
	cv::imshow("original", scr);
	cv::imshow("Mask", mask);
	cv::imshow("dst", dst);
	cv::waitKey();
	cv::destroyAllWindows();
}