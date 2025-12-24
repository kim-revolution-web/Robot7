#include "opencv2/opencv.hpp"

void show26() {

	float filter_data[] = { -1.0f ,-1.0f, 0.0f, -1.0f, 0.0f, 1.0f, 0.0f, 1.0f, 1.0f };
	cv::Mat emboss(3, 3, CV_32FC1, filter_data);// embossin 만드는 필터
	cv::Mat src = cv::imread("rose.bmp", cv::IMREAD_GRAYSCALE);
	cv::Mat dst;
	cv::filter2D(src, dst, -1, emboss, cv::Point(-1, -1), 128.0);  //깊이 -1

	cv::imshow("src", src);
	cv::imshow("dst", dst);
	cv::waitKey();
	cv::destroyAllWindows();

}

void show27() {

	float blur_filter[] = {

		1 / 9.f,1 / 9.f,1 / 9.f,
		1 / 9.f,1 / 9.f,1 / 9.f,
		1 / 9.f,1 / 9.f,1 / 9.f,
	};

	cv::Mat src = cv::imread("rose.bmp", cv::IMREAD_GRAYSCALE);
	cv::Mat dst;
	cv::Mat blur(3, 3, CV_32FC1, blur_filter);
	cv::filter2D(src, dst, -1, blur, cv::Point(-1, -1), 4);//평면 -1 

	//blur 적용
	cv::Mat dst2;// blur 필터를 통과후 만들어질 이미지
	cv::blur(src, dst2, cv::Size(3, 3));

	cv::imshow("src", src);
	cv::imshow("dst", dst);
	cv::imshow("dst2", dst2);
	cv::waitKey();
	cv::destroyAllWindows();


}

void show28() {

	cv::Mat src = cv::imread("rose.bmp", cv::IMREAD_GRAYSCALE);
	cv::imshow("SRC", src);
	cv::Mat dst;
	for (int sigma = 1; sigma <= 5; ++sigma) {
		cv::GaussianBlur(src, dst, cv::Size(), sigma);
		cv::putText(dst, cv::format("Sigma:%d", sigma),
			cv::Point(10, 30), cv::FONT_HERSHEY_PLAIN, 1.0, cv::Scalar(255), 1, cv::LINE_AA);
		cv::imshow(cv::format("Sigma:%d", sigma), dst);
		cv::waitKey();
		cv::destroyAllWindows;
	}
}

static void printKernelTable(const cv::Mat& k32f)
{
	CV_Assert(k32f.type() == CV_32FC1);
	int r = k32f.rows / 2;

	std::cout << "\n[Gaussian 2D kernel] size=" << k32f.rows << "x" << k32f.cols << "\n";
	std::cout << "     ";
	for (int x = -r; x <= r; ++x) std::cout << std::setw(8) << x;
	std::cout << "\n";

	std::cout << std::fixed << std::setprecision(4);
	for (int y = -r; y <= r; ++y) {
		std::cout << std::setw(3) << y << "  ";
		for (int x = -r; x <= r; ++x) {
			float v = k32f.at<float>(y + r, x + r);
			std::cout << std::setw(8) << v;
		}
		std::cout << "\n";
	}
}

void show28_1()
{
	cv::Mat src = cv::imread("rose.bmp", cv::IMREAD_GRAYSCALE);
	if (src.empty()) {
		std::cout << "rose.bmp 로드 실패\n";
		return;
	}

	for (int sigma = 1; sigma <= 5; ++sigma)
	{
		int ksize = 8 * sigma + 1;          // 슬라이드 스타일(σ=1 -> 9x9)
		// int ksize = 6 * sigma + 1;       // 다른 권장식(σ=1 -> 7x7)

		// 1) 2D 가우시안 마스크 만들기
		cv::Mat g1d = cv::getGaussianKernel(ksize, (double)sigma, CV_32F); // 합=1
		cv::Mat kernel2d = g1d * g1d.t();                                  // 2D, 합=1

		// 2) 표처럼 콘솔 출력(원하면 sigma==1일 때만 출력해도 됨)
		printKernelTable(kernel2d);

		// 3) 커널을 눈으로 보이게(가중치 이미지)
		cv::Mat kvis;
		cv::normalize(kernel2d, kvis, 0, 255, cv::NORM_MINMAX);
		kvis.convertTo(kvis, CV_8U);
		cv::resize(kvis, kvis, cv::Size(), 30, 30, cv::INTER_NEAREST);

		// 4) 실제 블러 적용(커널 크기/시그마를 명시해서 “그림의 커널” 느낌)
		cv::Mat dst;
		cv::GaussianBlur(src, dst, cv::Size(ksize, ksize), sigma, sigma, cv::BORDER_DEFAULT);

		cv::putText(dst, cv::format("sigma=%d  ksize=%dx%d", sigma, ksize, ksize),
			cv::Point(10, 30), cv::FONT_HERSHEY_PLAIN, 1.2, cv::Scalar(255), 1, cv::LINE_AA);

		cv::imshow("SRC", src);
		cv::imshow(cv::format("Kernel (sigma=%d)", sigma), kvis);
		cv::imshow(cv::format("GaussianBlur (sigma=%d)", sigma), dst);

		cv::waitKey(0);
		cv::destroyAllWindows();
	}
}

void show29() {

	cv::Mat src{ cv::imread("rose.bmp", cv::IMREAD_GRAYSCALE) };//nuiform initialzer
	cv::imshow("src", src);
	cv::Mat blurred;//Gaussian 을 통과해서 만들어질 이미지;
	float alpha = 1.0f;
	for (int sigma = 1; sigma <= 5; ++sigma)
	{
		cv::GaussianBlur(src, blurred, cv::Size(), sigma);
		cv::Mat dst = (1 + alpha) * src - (alpha * blurred);
		cv::putText(dst, cv::format("Sigma:%d", sigma),
			cv::Point(10, 30), cv::FONT_HERSHEY_PLAIN, 1.0, cv::Scalar(255), 1, cv::LINE_AA);
		cv::imshow(cv::format("Sigma:%d", sigma), dst);
		cv::waitKey();

	}
	cv::destroyAllWindows();



}

void show30() {

	cv::Mat src = cv::imread("ka.jpg", cv::IMREAD_GRAYSCALE);
	cv::Mat dst;
	for (int stddev = 10; stddev <= 30; stddev += 10)
	{
		cv::Mat noise(src.size(), CV_32SC1);
		cv::randn(noise, 0, stddev);
		cv::add(src, noise, dst, cv::noArray(), CV_8UC1); // dst = src+noise;
		cv::putText(dst, cv::format("stddev:%d", stddev), cv::Point(10, 30), cv::FONT_HERSHEY_PLAIN, 1.0,
			cv::Scalar(255), 1, cv::LINE_AA);
		cv::imshow(cv::format("stddev:%d", stddev), dst);
		cv::imshow("ka", src);
		cv::waitKey();
		cv::destroyAllWindows();
	}
}

void show31() {

	cv::Mat src{ cv::imread("lenna.png", cv::IMREAD_GRAYSCALE) };
	cv::imshow("SRC", src);
	cv::Mat dst1; //Gaussian noise가 들어간 영상
	cv::Mat dst2;//양방향 필터를 통과한 영상 어느정도 노이즈가 제거된 연상
	cv::Mat noise(src.size(), CV_32SC1);// 512X512 singde Matrix   CV_32SC1 
	cv::randn(noise, 0, 5);// mean 0,standard deviation : 5

	cv::add(src, noise, dst1, cv::noArray(), CV_8UC1);
	cv::imshow("DST1", dst1);
	cv::bilateralFilter(dst1, dst2, -1, 20, 5);

	
	cv::imshow("DST2", dst2);
	cv::waitKey();
	cv::destroyAllWindows();

}

void show32() {

	cv::Mat src{cv::imread("lenna.png", cv::IMREAD_GRAYSCALE)};
	cv::imshow("SRC", src);

	int num = static_cast<int>(src.total() * 0.1); //전체 픽셀에서  10%정도 쓰겠다
	for (int i = 0; i < num; ++i) {
		
		
		// src.cols 나눠서 나머지가 나눈값보다 크지 않다 그러니 src.cols 보다 적은 값이 되도록 만들어준다
		int x=rand() % src.cols;
		int y = rand() % src.rows;
		src.at<uchar>(y, x) = (i % 2) * 255;

	}
	cv::Mat dst1; //Gaussian Filter가 들어간 영상
	cv::Mat dst2;//양방향 필터를 통과한 영상 어느정도 노이즈가 제거된 연상

	cv::GaussianBlur(src, dst1, cv::Size(), 1);
	cv::medianBlur(src, dst2, 3);
	cv::imshow("GaussianBlur", dst1);
	cv::imshow("medianBlur", dst2);
	cv::imshow("DirtySRC", src);
	cv::waitKey();
	cv::destroyAllWindows();


}