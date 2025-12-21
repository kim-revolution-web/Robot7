#include<iostream>
#include"opencv2/opencv.hpp"
#include<vector>

void ex2_2() {

	std::cout << "Hello opencv" << CV_VERSION << std::endl;

	cv::Mat ig;
	ig = cv::imread("kim.jpg");

	if (ig.empty()) {
		std::cout << "사진 없다";
		return ;
	}
	cv::namedWindow("kim");
	cv::imshow("kim", ig);
	cv::waitKey(0);


	return;
}

void misson1() {

	std::cout << "hello open cv" << CV_VERSION << std::endl;
	cv::Mat mis = cv::imread("kim.jpg");

	if (mis.empty()) {
		std::cout << "사진없음" << std::endl;
		return;
	}
	std::cout << "width(cols) = " << mis.cols << "\n";
	std::cout << "height(rows) = " << mis.rows << "\n";
	std::cout << "channels = " << mis.channels() << "\n";

	cv::Rect c(50, 50, 100, 150);
	cv::Mat roi = mis(c);
	roi.setTo(cv::Scalar(0, 0, 255));

	//510*340
	cv::Rect c1(50, 100, 200, 400); //.setTo 덮어쓰기
	cv::Mat ro = mis(c1).clone(); //cv::Mat ro1; mis(c).copy(ro1);
	ro(cv::Rect(0, 0, 150, 350)).setTo(cv::Scalar(0, 255, 255));

	std::cout << "ro size = " << ro.cols << " x " << ro.rows << "\n";
	cv::namedWindow("kim");
	cv::imshow("kim",mis); 
	cv::namedWindow("kijk");
	cv::imshow("kijk", ro);
	cv::waitKey(0);
	cv::destroyAllWindows();

	
}

void misson1_1() {

	cv::Mat mis2;
	std::cout << "배끼기" << CV_VERSION << std::endl;
	mis2 = cv::imread("kim.jpg");
	if (mis2.empty()) {
		std::cout << "사진 실패" << std::endl;
		return;

	}

	std::cout << "width(cols): " << mis2.cols <<"\n" << "height(rows): " << mis2.rows << "\n" <<
		"channels :"  << mis2.channels() << std::endl;
	
	cv::Rect c(50, 50, 200, 300);
	mis2(c)(cv::Rect(0, 0, 100, 200)).setTo(cv::Scalar(255, 0, 0));
	cv::Mat clo2=mis2(c).clone();

	clo2(cv::Rect(0,0,100,200)).setTo(cv::Scalar(255,0,0));
	cv::imshow("copy", mis2);
	cv::imshow("copy1", clo2);
	
	cv::waitKey();
	cv::destroyAllWindows();


}

//압축풀질 낮춰서 저장
void misson2() {

	cv::Mat img = cv::imread("kim.jpg");
	if (img.empty()) {
		std::cout << "파일이미지 안나옴" << std::endl;
		return;
	}

	std::vector <int> params95;
	params95.push_back(cv::IMWRITE_JPEG_QUALITY);
	params95.push_back(95);
	
	std::vector <int> params50;
	params50.push_back(cv::IMWRITE_JPEG_QUALITY);
	params50.push_back(50);

	std::vector <int> params10 =
	{ cv::IMWRITE_JPEG_QUALITY ,10};

	cv::imwrite("kim_q95.jpg", img, params95);
	cv::imwrite("kim_q50.jpg", img, params50);
	cv::imwrite("kim_q10.jpg", img, params10);

	cv::imshow("orginal",img);
	cv::Mat a95 = cv::imread("kim_q95.jpg");
	cv::Mat a50 = cv::imread("kim_q50.jpg");
	cv::Mat a10 = cv::imread("kim_q10.jpg");
	cv::imshow("a95", a95);
	cv::imshow("params50", a50);
	cv::imshow("params10", a10);
	

	cv::waitKey();
	cv::destroyAllWindows();
}

static void putLabel(cv::Mat& img, const std::string& text)
{
	// 글씨가 잘 보이도록 뒤에 검은 박스 깔기(간단 버전)
	cv::rectangle(img, cv::Rect(0, 0, img.cols, 40), cv::Scalar(0, 0, 0), cv::FILLED);
	
	cv::putText(img, text, cv::Point(10, 28),
		cv::FONT_HERSHEY_SIMPLEX, 0.8, cv::Scalar(255, 255, 255), 2);
	//텍스트를 10,28지점에 넣을꺼야? Scalar흰색,2뭐야 
}

void mission2_2compare()
{
	cv::Mat original = cv::imread("kim.jpg");
	if (original.empty()) {
		std::cout << "kim.jpg 로드 실패\n";
		return;
	}

	// JPEG 품질 옵션
	std::vector<int> p95 = { cv::IMWRITE_JPEG_QUALITY, 95 }; //jpg에서 압출할수 있는건 jpeg라서 jpeg로 하는거야?
	std::vector<int> p50 = { cv::IMWRITE_JPEG_QUALITY, 50 };
	std::vector<int> p10 = { cv::IMWRITE_JPEG_QUALITY, 10 };

	// 저장
	cv::imwrite("kim_q95.jpg", original, p95);
	cv::imwrite("kim_q50.jpg", original, p50);
	cv::imwrite("kim_q10.jpg", original, p10);

	// 다시 읽기(실제로 저장된 결과를 비교하기 위해)
	cv::Mat q95 = cv::imread("kim_q95.jpg");
	cv::Mat q50 = cv::imread("kim_q50.jpg");
	cv::Mat q10 = cv::imread("kim_q10.jpg");

	if (q95.empty() || q50.empty() || q10.empty()) { 
		
		std::cout << "저장된 jpg 재로드 실패(작업 폴더 확인)\n";
		return;
	}

	
	cv::resize(q95, q95, original.size());
	cv::resize(q50, q50, original.size());
	cv::resize(q10, q10, original.size());//q95,높이 넓이== original.size() = (width, height) 한다는거야?
	// 라벨 넣기(원본/압축품질)
	cv::Mat img0 = original.clone();
	cv::Mat img1 = q95.clone();
	cv::Mat img2 = q50.clone();
	cv::Mat img3 = q10.clone();

	putLabel(img0, "original"); //깊은복사해서 Lable이 뭐하는거야?
	putLabel(img1, "Q95");
	putLabel(img2, "Q50");
	putLabel(img3, "Q10");
	
	// 가로로 붙이기
	std::vector<cv::Mat> list = { img0, img1, img2, img3 }; /// <Mat> vector 신선하네
	cv::Mat canvas;
	cv::hconcat(list, canvas);//canvas에 matlist묶음

	// 너무 크면 화면에 안 들어갈 수 있으니 축소해서 표시
	double scale = 0.5; // 필요하면 0.4~0.8로 조절
	cv::Mat show;
	cv::resize(canvas, show, cv::Size(), scale, scale);//이것도 모르겠어

	cv::namedWindow("compare (original | Q95 | Q50 | Q10)", cv::WINDOW_NORMAL); //뭐가 노멀야? 뭐하는거야?
	cv::imshow("compare (original | Q95 | Q50 | Q10)", show);
	cv::waitKey(0);
	cv::destroyAllWindows();
}

void mission2_3() 
{
	cv::Mat img = cv::imread("kim.jpg");
	if (img.empty()) {
		std::cout << "kim.jpg 로드 실패\n";
		return ;
	}

	// ------------------------------------------------------
	// 1) rectangle(): 이미지 위에 "테두리만" 그리기
	// ------------------------------------------------------
	cv::Mat draw1 = img.clone();
	cv::Rect r1(30, 40, 180, 120); // (x=30, y=40)에서 시작, 가로180 세로120
	cv::rectangle(draw1, r1, cv::Scalar(0, 255, 0), 3); // 초록 테두리, 두께 3

	// ------------------------------------------------------
	// 2) rectangle() + FILLED: 사각형 "채워서" 그리기
	// ------------------------------------------------------
	cv::Mat draw2 = img.clone();
	cv::Rect r2(250, 60, 140, 180);
	cv::rectangle(draw2, r2, cv::Scalar(0, 0, 255), cv::FILLED); // 빨강으로 꽉 채움

	// ------------------------------------------------------
	// 3) img(Rect): ROI "자르기" (부분 영상 뷰/복사)
	//    - ROI에 setTo 하면 원본에도 영향(뷰) -> 그래서 clone본에서 실험
	// ------------------------------------------------------
	cv::Rect r3(80, 220, 200, 140);

	// 3-1) ROI를 따로 창에 보여주기(자른 결과)
	cv::Mat roi_view = img(r3); // ROI 뷰(원본 공유)

	// 3-2) ROI에 setTo로 색칠하면 원본도 바뀌는지 확인
	cv::Mat draw3 = img.clone();
	cv::Mat roi_in_draw3 = draw3(r3);                 // draw3의 ROI 뷰
	roi_in_draw3.setTo(cv::Scalar(255, 0, 0));        // 파랑(BGR)으로 ROI 전체 채움

	// ------------------------------------------------------
	// 출력
	// ------------------------------------------------------
	cv::imshow("original", img);
	cv::imshow("1) rectangle border (r1)", draw1);
	cv::imshow("2) rectangle filled (r2)", draw2);
	cv::imshow("3) ROI view (r3) + setTo on cloned image", draw3);
	cv::imshow("3-1) ROI only (r3)", roi_view); // ROI만 따로 보여주기

	cv::waitKey(0);
	cv::destroyAllWindows();

}


void resize_and_window_flags_demo()
{
	cv::Mat img = cv::imread("kim.jpg");
	if (img.empty()) {
		std::cout << "kim.jpg 로드 실패\n";
		return;
	}

	// ============================
	// 1) resize: 비율(scale)로 줄이기/늘리기
	// ============================
	double scale_down = 0.5;  // 절반으로 축소
	double scale_up = 1.5;  // 1.5배 확대

	cv::Mat half, one_and_half;
	// dsize를 비워두고(fx, fy)로 크기 결정
	cv::resize(img, half, cv::Size(), scale_down, scale_down);
	cv::resize(img, one_and_half, cv::Size(), scale_up, scale_up);

	// ============================
	// 2) resize: 원하는 픽셀 크기로 "직접" 지정
	// ============================
	cv::Mat fixed_300x400;
	cv::resize(img, fixed_300x400, cv::Size(300, 400)); // width=300, height=400

	// ============================
	// namedWindow 플래그 비교
	// ============================

	// (A) AUTOSIZE: 이미지 크기에 딱 맞게 창 생성 (창 크기 변경이 제한되는 편)
	cv::namedWindow("A_AUTOSIZE_half", cv::WINDOW_AUTOSIZE);
	cv::imshow("A_AUTOSIZE_half", half);

	// (B) NORMAL: 사용자가 창 크기 조절 가능 (resizeWindow가 잘 먹음)
	cv::namedWindow("B_NORMAL_fixed300x400", cv::WINDOW_NORMAL);
	cv::resizeWindow("B_NORMAL_fixed300x400", 600, 500); // 창 크기 "강제로" 키워보기
	cv::imshow("B_NORMAL_fixed300x400", fixed_300x400);

	// (C) NORMAL + KEEPRATIO: 창을 늘려도 영상 비율 유지하려고 노력
	cv::namedWindow("C_NORMAL_KEEP_RATIO", cv::WINDOW_NORMAL | cv::WINDOW_KEEPRATIO);
	cv::resizeWindow("C_NORMAL_KEEP_RATIO", 800, 250); // 일부러 가로로 길게
	cv::imshow("C_NORMAL_KEEP_RATIO", img);

	// (D) NORMAL + FREERATIO: 창 비율대로 영상이 찌그러질 수 있음(자유 비율)
	cv::namedWindow("D_NORMAL_FREE_RATIO", cv::WINDOW_NORMAL | cv::WINDOW_FREERATIO);
	cv::resizeWindow("D_NORMAL_FREE_RATIO", 800, 250); // 똑같이 가로로 길게
	cv::imshow("D_NORMAL_FREE_RATIO", img);

	cv::waitKey(0);
	cv::destroyAllWindows();
}