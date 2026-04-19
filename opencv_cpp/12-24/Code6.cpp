#include"opencv2/opencv.hpp"

void show33() {
	//픽셀 바꿀때만 그레이 스케일
	cv::Mat src{ cv::imread("tekapo.bmp") };
	cv::imshow("SRC", src);
	cv::Point2f srcPts[3];
	cv::Point2f dstPts[3];

	// 원본에서 기준이 될 3점(삼각형) 선택
	srcPts[0] = cv::Point2f(0, 0);
	srcPts[1] = cv::Point2f(src.cols - 1.0f, 0.0f);
	srcPts[2] = cv::Point2f(src.cols - 1.0f, src.rows - 1.0f);

	// 그 3점이 변환 후 어디로 갈지 목표점 3개 지정
	dstPts[0] = cv::Point2f(50.0f, 50.0f);
	dstPts[1] = cv::Point2f(src.cols - 100.0f, 100.0f);
	dstPts[2] = cv::Point2f(src.cols - 50.0f, src.rows - 50.0f);

	// 3점 매칭을 만족하는 아핀 변환 행렬(2x3) 계산
	cv::Mat M = cv::getAffineTransform(srcPts, dstPts);

	// 행렬 M을 이용해 실제로 이미지 변환(기울임/이동/회전/스케일 포함)
	cv::Mat dst;
	cv::warpAffine(src, dst, M, src.size());

	cv::imshow("SRC", src);
	cv::imshow("DST", dst);
	cv::waitKey();
	cv::destroyAllWindows();
}

void my1() {
	cv::Mat img = cv::imread("ka.jpg");
	if (img.empty()) {
		std::cout << "이미지 로드 실패: ka.jpg\n";
		return;
	}

	// 1) 600x600 리사이즈
	cv::Mat resized;
	cv::resize(img, resized, cv::Size(600, 600), 0, 0, cv::INTER_AREA);

	// 2) CLAHE로 선명하게 (Y 채널만)
	cv::Mat ycrcb;
	cv::cvtColor(resized, ycrcb, cv::COLOR_BGR2YCrCb);

	std::vector<cv::Mat> ch;
	cv::split(ycrcb, ch); // ch[0]=Y, ch[1]=Cr, ch[2]=Cb

	cv::Ptr<cv::CLAHE> clahe = cv::createCLAHE(2.0, cv::Size(8, 8));
	cv::Mat y2;
	clahe->apply(ch[0], y2);
	ch[0] = y2;

	cv::Mat merged, enhanced;
	cv::merge(ch, merged);
	cv::cvtColor(merged, enhanced, cv::COLOR_YCrCb2BGR);

	cv::imwrite("ka_600_clahe.jpg", enhanced);

	cv::imshow("original 600x600", resized);
	cv::imshow("enhanced (CLAHE)", enhanced);
	cv::waitKey(0);

}

//1 0 150
//0 1 100
//34~36 거의 같음
void show34() {

	cv::Mat src = cv::imread("tekapo.bmp");
	cv::Mat move = cv::Mat_<float>({ 2,3 },
		{ 1.0f,0.0f,150.0f,
		0.0f,1.0f,100.0f });
	cv::Mat dst;
	cv::warpAffine(src, dst, move, cv::Size());
	cv::imshow("SRC", src);
	cv::imshow("dst", dst);
	cv::waitKey();
	cv::destroyAllWindows();

}

void show35() {

	cv::Mat src = cv::imread("tekapo.bmp");
	/* std::cout << "기울기" << "\n";
	 float m = 0.0f;
	 std::cin >> m;*/
	cv::Mat move = cv::Mat_<float>({ 2,3 },
		{ 2.0f,0.0f,0.0f,
		0.0f,2.0f,0.0f });
	cv::Mat dst;
	cv::warpAffine(src, dst, move, cv::Size(cvRound(src.cols + src.rows * 1.0f), src.rows));
	//cv::resize(dst, dst, cv::Size(600,600));
	cv::imshow("SRC", src);
	cv::imshow("dst", dst);
	cv::waitKey();
	cv::destroyAllWindows();
}

void show36() {

	cv::Mat src = cv::imread("tekapo.bmp");
	std::cout << "몇 배" << "\n";
	float m = 0.0f;
	std::cin >> m;
	cv::Mat move = cv::Mat_<float>({ 2,3 },
		{ m,0.0f,0.0f,
		0.0f,m,0.0f });
	cv::Mat dst;
	cv::warpAffine(src, dst, move, cv::Size(cvRound(src.cols + src.rows * 1.0f), src.rows));
	//cv::resize(dst, dst, cv::Size(600,600));
	cv::imshow("SRC", src);
	cv::imshow("dst", dst);
	cv::waitKey();
	cv::destroyAllWindows();
}

void show37() {

	cv::Mat src = cv::imread("rose.bmp");
	if (src.empty()) {
		std::cerr << "IMage load failed!" << std::endl;
		return;
	}

	cv::Mat dst1, dst2, dst3, dst4;
	resize(src, dst1, cv::Size(), 4, 4, cv::INTER_NEAREST);
	resize(src, dst2, cv::Size(1920, 1280));
	resize(src, dst3, cv::Size(1920, 1280), 0, 0, cv::INTER_CUBIC);
	resize(src, dst4, cv::Size(1920, 1280), 0, 0, cv::INTER_LANCZOS4);

	cv::imshow("src", src);
	cv::imshow("dst1", dst1(cv::Rect(400, 500, 400, 400)));
	cv::imshow("dst2", dst2(cv::Rect(400, 500, 400, 400)));
	cv::imshow("dst3", dst3(cv::Rect(400, 500, 400, 400)));
	cv::imshow("dst4", dst4(cv::Rect(400, 500, 400, 400)));

	cv::waitKey();
	cv::destroyAllWindows();

}

//영상 회전
void show38() {
	cv::Mat src = cv::imread("tekapo.bmp");

	cv::Point2d center(src.cols / 2, src.rows / 2);
	cv::Mat move = cv::getRotationMatrix2D(center, 20.0, 1.0);//음수면 반시계 //양수면 시계 방향 //2x3 affine 행렬
	//호도 법
	cv::Mat dst;
	cv::warpAffine(src, dst, move, cv::Size());
	cv::imshow("src", src);
	cv::imshow("dst", dst);
	cv::waitKey();
	cv::destroyAllWindows();

}

void show39() {

	cv::Mat src = cv::imread("eastsea.bmp");
	cv::Mat dst1;
	cv::flip(src, dst1,1);//y 축 대칭
	cv::imshow("좌우대칭", dst1);
	cv::Mat dst2;
	cv::flip(src, dst2, 0);//x 축 대칭
	cv::imshow("상하대칭", dst2);

	cv::Mat dst3;
	cv::flip(src, dst3, -1);//원점 대칭
	cv::imshow("원점 대칭", dst3);
	cv::waitKey();
	cv::destroyAllWindows();
}


//----------------------------------------
static int count = 0;
static cv::Point2f dstQuad[4];
static cv::Point2f srcQuad[4];
static cv::Mat src;
void on_mouse1(int event,int x,int y,int flag, void* userdata) {

	if (event == cv::EVENT_LBUTTONDOWN) {
		if (count < 4) {
			srcQuad[count++] = cv::Point2f(x, y);
			cv::circle(src, cv::Point(x, y), 5,
				cv::Scalar(0, 0, 255), -1);
			cv::imshow("SRC", src);

		}
		if (count == 4)
		{
			int width = 200;
			int height = 300;
			dstQuad[0] = cv::Point2f(0, 0);
			dstQuad[1] = cv::Point2f(width-1, 0);
			dstQuad[2] = cv::Point2f(width-1,height-1);
			dstQuad[3] = cv::Point2f(0, height - 1);
			cv::Mat move=
				cv::getPerspectiveTransform(srcQuad, dstQuad);
			cv::Mat dst;
			cv::warpPerspective(src, dst, move, cv::Size(width, height));
			cv::imshow("dst", dst);
		}
	}
}
void show40() 
{
	count = 0;
	src = cv::imread("card.bmp");
	cv::namedWindow("SRC");
	cv::setMouseCallback("SRC", on_mouse1);
	cv::imshow("SRC", src);
	cv::waitKey();
	cv::destroyAllWindows();
}

