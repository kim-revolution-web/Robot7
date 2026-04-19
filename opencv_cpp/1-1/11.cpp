#include <opencv2/opencv.hpp>
#include <iostream>
#include <ctime>

#include <windows.h>
#include <mmsystem.h>
#pragma comment(lib, "winmm.lib")


static cv::Point randomCenter(int W, int H, int halfSize) {
    if (W <= 2 * halfSize || H <= 2 * halfSize) return { W / 2, H / 2 };
    int x = rand() % (W - 2 * halfSize) + halfSize;//  
    int y = rand() % (H - 2 * halfSize) + halfSize;
    return { x, y };
}

void runProject() {
    srand((unsigned)time(nullptr));

    cv::VideoCapture cap(0);
    if (!cap.isOpened()) {
        std::cerr << "웹캠이 없습니다.\n";
        return;
    }

    cv::Mat sprite = cv::imread("ka.jpg");
    if (sprite.empty()) {
        std::cerr << "ka.jpg 로드 실패\n";
        return;
    }

    int halfSize = 30;
    cv::resize(sprite, sprite, cv::Size(halfSize * 2, halfSize * 2));

    cv::Mat prevGray;
    int score = 0;

    cv::Mat frame;
    cap >> frame;
    if (frame.empty()) return;
    cv::flip(frame, frame, 1);

    cv::Point targetPos = randomCenter(frame.cols, frame.rows, halfSize);

    //소리
    bool played30 = false;
    bool touching = false;                 // 지금 터치 중인지(연속 터치 방지)
    const double TH_HIGH = 0.35;           // 터치 시작 임계치
    const double TH_LOW = 0.15;

    while (true) {
        cap >> frame;
        if (frame.empty()) break;

        cv::flip(frame, frame, 1);

        int W = frame.cols, H = frame.rows;

        // 움직임 감지용 이진화 영상 만들기
        cv::Mat gray, diff, bin;
        cv::cvtColor(frame, gray, cv::COLOR_BGR2GRAY);
        cv::GaussianBlur(gray, gray, cv::Size(15, 15), 0);

        if (prevGray.empty()) {
            gray.copyTo(prevGray);
            continue;
        }

        cv::absdiff(prevGray, gray, diff);
        cv::threshold(diff, bin, 25, 255, cv::THRESH_BINARY);


        cv::Rect frameRect(0, 0, W, H);//사각형 만들어주고
        cv::Rect dstRect(targetPos.x - sprite.cols / 2,
            targetPos.y - sprite.rows / 2,
            sprite.cols, sprite.rows);

        cv::Rect clipped = dstRect & frameRect; //프레임 밖으로 나가지 않게 해주기

        /*int width = frame.cols;
        int height = frame.rows;

        int x1 = cv::max(0, targetPos.x - halfSize);
        int y1 = cv::max(0, targetPos.y - halfSize);
        int x2 = cv::min(width, targetPos.x + halfSize);
        int y2 = cv::min(height, targetPos.y + halfSize);

        cv::Rect rect(x1, y1, x2 - x1, y2 - y1);*/


        if (clipped.area() > 0) {
            // clipped.area() = clipped.width * clipped.height


             // sprite에서 잘라올 영역(크기 맞추기)
            cv::Rect srcRect(clipped.x - dstRect.x,
                clipped.y - dstRect.y,
                clipped.width, clipped.height);

            //  터치 판정(스프라이트 영역에서 움직임 픽셀 계산)
            int moved = cv::countNonZero(bin(clipped));
            // countNonZero 0이 아닌 영역 bin 이진화 한곳 clipped 프레임 범위

            double ratio = (double)moved / (double)clipped.area();//소리

            //if (moved > (int)(clipped.area() * 0.35)) {   // 민감도(0.05~0.35 조절)
            //   score++;
            //    targetPos = randomCenter(W, H, halfSize);


                //------------------------

            if (!touching && ratio > TH_HIGH) {
                touching = true;

                score++;
                targetPos = randomCenter(W, H, halfSize);

                if (!played30 && score >= 30) {
                    played30 = true;

                    // bgm 시작 (성공 여부 확인도 가능)
                    BOOL ok = PlaySound(TEXT("bgm.wav"), NULL,
                        SND_FILENAME | SND_ASYNC | SND_LOOP);
                    if (!ok) std::cout << "PlaySound failed: bgm.wav\n";
                }
            }

            //  터치 해제(손 뗌)
            else if (touching && ratio < TH_LOW) {
                touching = false;
            }

            //---------
        //}


            cv::Mat spriteDraw = sprite.clone(); //깊은 복사


            if (score > 5) {
                cv::flip(spriteDraw, spriteDraw, 1);
            }
            if (score > 10) {
                cv::flip(spriteDraw, spriteDraw, 0);
            }
            if (score > 15) {
                cv::cvtColor(spriteDraw, spriteDraw, cv::COLOR_BGR2GRAY); //그레이색
                cv::cvtColor(spriteDraw, spriteDraw, cv::COLOR_GRAY2BGR); // copyTo 맞추려고 3채널로 복귀
            }
            if (score > 20) {
                cv::Point2f c(spriteDraw.cols / 2.0f, spriteDraw.rows / 2.0f); 
                cv::Mat M = cv::getRotationMatrix2D(c, 20.0, 1.0); //20도 돌리는 값? 행렬이고
                cv::warpAffine(spriteDraw, spriteDraw, M, spriteDraw.size()); //값을 나타내준다
            }

            if (score > 25) {
                cv::Mat dst_open;
                for (int i = 0; i < 50; i++) {
                    cv::morphologyEx(spriteDraw, spriteDraw, cv::MORPH_OPEN, cv::Mat());  //기본이 3X3 침식->팽창
                }
            }


            //사진(좌표).복사(비디오(벗어나지않는 좌표)에 복사
            spriteDraw(srcRect).copyTo(frame(clipped));
        }

        cv::putText(frame, "Score : " + std::to_string(score),
            cv::Point(20, 30), cv::FONT_HERSHEY_PLAIN, 2,
            cv::Scalar(255, 0, 255), 2);

        cv::imshow("GAME", frame);


        gray.copyTo(prevGray);//이건뭐지?
        if (cv::waitKey(10) == 27) break;
    }

    PlaySound(NULL, 0, 0);// 소리정지
    cap.release();
    cv::destroyAllWindows();
}
