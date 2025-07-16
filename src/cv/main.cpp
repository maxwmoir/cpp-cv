#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/opencv.hpp>
#include <vector>
#include "client.h"

using namespace cv;
using namespace std;

// Image data structures
Mat img, imgHSV, mask, imgBlur;

// Color threshold values for the ball
int hmin = 83, smin = 70, vmin = 100;
int hmax = 108, smax = 255, vmax = 255;

// Number of ball arc positions saved (how many frames to keep info)
int N = 5;
int frames = 0;
vector<pair<float, float>> past(N);

// Number of nodes in grid for quadratic interpolent
int quad_size = 1000;
int showArc = 0, showCont = 0, showCent = 0;
vector<pair<float, float>> quad(quad_size);


void interpolatePolynomial(Client& client) {

    float x0 = past[0].first;
    float y0 = past[0].second;
    float x1 = past[2].first;
    float y1 = past[2].second;
    float x2 = past[4].first;
    float y2 = past[4].second;

    vector<float> nodes = {x0, y0, x1, y1, x2, y2 };

    if ((!x0 && !y0) || (!x1 && !y1) || (!x2 && !y2)) {
        return;
    }

    client.sendFloatVector(nodes);

    // Calculate Lagrange basis functions
    for (int i = 0; i < 650; i++) {
        float x = i;

        double L0 = ((x - x1) * (x - x2)) / ((x0 - x1) * (x0 - x2));
        double L1 = ((x - x0) * (x - x2)) / ((x1 - x0) * (x1 - x2));
        double L2 = ((x - x0) * (x - x1)) / ((x2 - x0) * (x2 - x1));

        // Calculate interpolated y value
        double interpolated_y = y0 * L0 + y1 * L1 + y2 * L2;
        quad[i % quad_size] = make_pair(x, interpolated_y);
    }

}

void getLargeContours() {
    vector<vector<Point>> contours;
    vector<Vec4i> hierarchy;

    findContours(mask, contours, hierarchy, RETR_EXTERNAL, CHAIN_APPROX_NONE);

    for (int i = 0; i < contours.size(); i++) {
        int area = contourArea(contours[i]);

        vector<vector<Point>> valid(contours.size());
        vector<Rect> boundRect(contours.size());



        if (area > 1000) {
            float peri = arcLength(contours[i], true);
            approxPolyDP(contours[i], valid[i], 0.001 * peri, true);
            boundRect[i] = boundingRect(valid[i]);
            Moments m = moments(contours[i]);

            float cx = m.m10 / m.m00;
            float cy = m.m01 / m.m00;

            past[frames % N] = make_pair(cx, cy);
            frames++;

            if (showCont)
                drawContours(img, valid, i, Scalar(255, 0, 255), 2);
        }
    }
}


int main() {

    VideoCapture cap(2);

    namedWindow("Trackbars", (640, 20));
    createTrackbar("Arc", "Trackbars", &showArc, 1);
    createTrackbar("Center", "Trackbars", &showCent, 1);
    createTrackbar("Contour", "Trackbars", &showCont, 1);
    createTrackbar("Hue Min", "Trackbars", &hmin, 179);
    createTrackbar("Hue Max", "Trackbars", &hmax, 179);
    createTrackbar("Sat Min", "Trackbars", &smin, 255);
    createTrackbar("Sat Max", "Trackbars", &smax, 255);
    createTrackbar("Val Min", "Trackbars", &vmin, 255);
    createTrackbar("Val Max", "Trackbars", &vmax, 255);

    Client client("127.0.0.1", 9999);

    while (true) {
        cap.read(img);

        flip(img, img, 1);
        cvtColor(img, imgHSV, COLOR_BGR2HSV);

        Scalar lower(hmin, smin, vmin);
        Scalar upper(hmax, smax, vmax);

        inRange(imgHSV, lower, upper, mask);
        GaussianBlur(mask, imgBlur, Size(3, 3), 3, 0);

        getLargeContours();


        if (showCent) {
            for (auto p : past) {
                if (p.first != 0 || p.second != 0) {
                    circle(img, Point(p.first, p.second), 3, Scalar(0, 225, 0), 3);

                }
            }
        }

        if (showArc) {
            for (auto p : quad) {
                circle(img, Point(p.first, p.second), 1, Scalar(255, 255, 255), 1);
            }
        }

        interpolatePolynomial(client);

        imshow("img", img);

        waitKey(1);
    }

}
