#include <opencv2/opencv.hpp>
#include <iostream>
#include <ctime>

#include <windows.h>
#include <mmsystem.h>
#pragma comment(lib, "winmm.lib")

static cv::Point randomCenter(int W, int H, int halfSize) {
    // 스프라이트가 화면 밖으로 나가지 않게 중심점을 뽑기 위해
    // x는 [halfSize ~ W-halfSize), y는 [halfSize ~ H-halfSize) 범위에서 랜덤
    if (W <= 2 * halfSize || H <= 2 * halfSize) return { W / 2, H / 2 };
    int x = rand() % (W - 2 * halfSize) + halfSize;
    int y = rand() % (H - 2 * halfSize) + halfSize;
    return { x, y };
}

void runProject() {
    srand((unsigned)time(nullptr)); //매번 랜덤 위치를 다르게 해준다 

    cv::VideoCapture cap(0);
    if (!cap.isOpened()) { std::cerr << "웹캠이 없습니다.\n"; return; }

    cv::Mat sprite = cv::imread("ka.jpg");
    if (sprite.empty()) { std::cerr << "face.jpg 로드 실패\n"; return; }

    int baseSize = 40;                 // 30으로 바꾸면 30x30
    int halfSize = baseSize / 2;
    cv::resize(sprite, sprite, cv::Size(baseSize, baseSize));

    cv::Mat prevGray;
    int score = 0;

    // 소리
    bool played30 = false;  // score가 30이 되었을 때 bgm을 1번만 켜기 위한 플래그
    bool touching = false;  // 연속 터치(계속 점수 올라가는 것) 방지
   // 손을 뗐다고 판단하는 임계치(터치 해제)0.15
    //터치 판단하는 임계치(터치) 0.35
    


    // 맞으면 잠깐 사라짐(연출)
    int hideCounter = 0;

    // 첫 프레임 + 저장 준비
    cv::Mat frame;
    cap >> frame;
    if (frame.empty()) return;

    cv::VideoWriter writer(
        "output.avi",
        cv::VideoWriter::fourcc('M', 'J', 'P', 'G'), // MJPG 코덱(윈도우에서 호환 잘 됨)
        30.0,                                        // FPS: 1초에 30프레임 저장
        cv::Size(frame.cols, frame.rows),            // 저장 영상의 해상도(가로, 세로)
        true                                         // 컬러 영상(BGR) 저장
    );

    cv::Point targetPos = randomCenter(frame.cols, frame.rows, halfSize);

    while (true) {
        cap >> frame;
        if (frame.empty()) break;
        cv::flip(frame, frame, 1); // 거울 모드(좌우 반전)

        int W = frame.cols, H = frame.rows;

        // 움직임 감지(프레임 차이로 움직임만 뽑기)
        cv::Mat gray, diff, bin;
        cv::cvtColor(frame, gray, cv::COLOR_BGR2GRAY);//이진화 전 색 변환 
        cv::GaussianBlur(gray, gray, cv::Size(15, 15), 0);//  대부분 값이 홀수 블러링 효과

        if (prevGray.empty()) {
            gray.copyTo(prevGray);
            continue;
        }

        cv::absdiff(prevGray, gray, diff);

        // threshold(src, dst, thresh, maxval, type)
        // - thresh=25  : diff값이 25보다 크면 "움직임"으로 판단
        // - maxval=255 : 움직임으로 판단된 픽셀을 255(흰색)로 만들기
        // 결과: bin은 0(검정) 또는 255(흰색)만 가지는 이진화 영상
        cv::threshold(diff, bin, 25, 255, cv::THRESH_BINARY);

        // -------------------------
        // 스프라이트 변형(최소)
        // -------------------------
        cv::Mat spriteDraw = sprite.clone();

        // (4) 크기변환: 점수가 5 넘으면 1.3배로 커짐
        if (score > 5) cv::resize(spriteDraw, spriteDraw, cv::Size(), 1.3, 1.3);

        // (2) 반전: 점수가 10 넘으면 스프라이트만 좌우반전(얼굴이 뒤집힘)
        if (score > 10) cv::flip(spriteDraw, spriteDraw, 1);

        // (5) 색깔변환: 점수가 15 넘으면 그레이로 바뀜
        // (그레이로 만들면 채널이 1개가 되므로 다시 BGR로 되돌려서 copyTo가 안정적으로 됨)
        if (score > 15) {
            cv::cvtColor(spriteDraw, spriteDraw, cv::COLOR_BGR2GRAY);
            cv::cvtColor(spriteDraw, spriteDraw, cv::COLOR_GRAY2BGR);
        }

        // (3) 축이동/휘어짐을 단순하게 표현: 회전(30도)
        if (score > 20) {
            cv::Point2f c(spriteDraw.cols / 2.0f, spriteDraw.rows / 2.0f); // 중심점(실수 좌표)
            cv::Mat M = cv::getRotationMatrix2D(c, 30.0, 1.0);             // 중심 기준 30도 회전 행렬
            cv::warpAffine(spriteDraw, spriteDraw, M, spriteDraw.size());  // 회전 적용
        }

        // (1) 모핑: 점수가 25 넘으면 CLOSE로 눈/입처럼 작은 어두운 부분이 메워지는 느낌
        if (score > 25) {
            // getStructuringElement: 모폴로지 연산에 쓰는 "커널(모양/크기)"을 만들어 줌
            // MORPH_ELLIPSE + 7x7: 동그란 형태의 7x7 커널
            cv::Mat kernel = cv::getStructuringElement(cv::MORPH_ELLIPSE, cv::Size(7, 7));

            // MORPH_CLOSE(팽창->침식): 작은 어두운 구멍을 메우는 효과(눈/입이 줄어든 느낌)
            for (int i = 0; i < 3; i++) {
                cv::morphologyEx(spriteDraw, spriteDraw, cv::MORPH_CLOSE, kernel);
            }
        }

        // -------------------------
        // 합성 + 터치 판정
        // -------------------------
        cv::Rect frameRect(0, 0, W, H);

        // 스프라이트가 놓일 목표 사각형(중심 targetPos 기준)
        cv::Rect dstRect(targetPos.x - spriteDraw.cols / 2,
            targetPos.y - spriteDraw.rows / 2,
            spriteDraw.cols, spriteDraw.rows);

        // clipped = dstRect와 frameRect의 교집합(화면 밖으로 나간 부분 잘라냄)
        cv::Rect clipped = dstRect & frameRect;

        // 예시(숫자로 감 잡기):
        //  W=640, H=480, spriteDraw가 40x40이고 targetPos=(10,10)이면
        //  dstRect = (-10,-10,40,40)  -> 화면 밖으로 나감
        //  clipped = (0,0,30,30)      -> 화면 안에 있는 부분만 남음

        double ratio = 0.0;
        if (clipped.area() > 0) {
            // bin(clipped): 스프라이트가 있는 영역에서만 "움직임(흰 픽셀)"을 봄
            int moved = cv::countNonZero(bin(clipped));

            // ratio = moved / area
            // 왜 나누냐?
            //  - 스프라이트 크기가 커지거나(1.3배), clipped가 잘리면(30x30) moved의 절대값이 변함
            //  - 그래서 면적으로 나눠서 0~1 사이 비율로 만들면 임계치(0.35)가 안정적임
            ratio = (double)moved / (double)clipped.area();
        }

        // 터치 시작:
        //  - touching==false: 지금까지 손이 안 닿은 상태
        //  - clipped.area()>0: 화면 안에 스프라이트가 실제로 존재
        //  - ratio>0.35: 스프라이트 영역의 35% 이상이 움직였다고 판단
        if (!touching && clipped.area() > 0 && ratio > 0.35) {
            touching = true;
            score++;

            // 다음 위치로 이동(간단 버전: 원래 크기 halfSize로 이동)
            targetPos = randomCenter(W, H, halfSize);

            // (6) 타격 효과음
            PlaySound(TEXT("hit.wav"), NULL, SND_FILENAME | SND_ASYNC);

            // 30점 BGM(반복 재생)
            if (!played30 && score >= 30) {
                played30 = true;
                PlaySound(TEXT("bgm.wav"), NULL, SND_FILENAME | SND_ASYNC | SND_LOOP);
            }

            hideCounter = 6; // 잠깐 사라짐
        }
        // 터치 해제: 비율이 충분히 작아지면 손 뗀 것으로 처리
        else if (touching && ratio < 0.15) {
            touching = false;
        }

        // 사라짐 처리
        if (hideCounter > 0) {
            hideCounter--;
        }
        else {
            if (clipped.area() > 0) {
                // spriteDraw에서 잘라올 영역(클리핑에 맞춰 동일 크기로 잘라서 copyTo)
                cv::Rect srcRect(clipped.x - dstRect.x, clipped.y - dstRect.y,
                    clipped.width, clipped.height);

                spriteDraw(srcRect).copyTo(frame(clipped));
            }
        }

        cv::putText(frame, "Score : " + std::to_string(score),
            cv::Point(20, 30), cv::FONT_HERSHEY_PLAIN, 2,
            cv::Scalar(255, 0, 255), 2);

        cv::imshow("GAME", frame);

        // (8) 동영상 저장
        if (writer.isOpened()) writer.write(frame);

        // 다음 루프에서 diff 계산을 위해 "현재 gray"를 prevGray로 업데이트
        gray.copyTo(prevGray);

        if (cv::waitKey(10) == 27) break;
    }

    PlaySound(NULL, 0, 0);
    cap.release();
    cv::destroyAllWindows();
}
