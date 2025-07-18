/**
 * @file <main.cpp>
 * @brief OpenCV tool to detect a target's trajectory and send past coordinates to a server.
 *
 * @author Max Moir
 * @date 10/07/2025
 */

#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/opencv.hpp>
#include <vector>
#include "client.h"

using namespace cv;
using namespace std;

// Constant declarations
const int CONTOUR_SIZE = 1000;
const float CONTOUR_PRECISION = 0.001;

// Target colour thresholds
const int HUE_MIN = 83,  SAT_MIN = 70 , VAL_MIN = 100;
const int HUE_MAX = 108, SAT_MAX = 255, VAL_MAX = 255;

const int NODES = 5;
const int CAMERA = 2;

const string HOST = "127.0.0.1";
const int PORT = 9999;

vector<pair<float, float>> findLargeContours(Mat& mask, Mat& img, bool show_contours) {
    /**
     * Takes input mask and finds all the contours of large enough size to be the target.
     *
     * @param mask Image matrix with colour mask
     * @param img  Image matrix to draw contours onto
     * @param show_cont Boolean representing contour visibility in output image
     * @return Vector of the center of mass of each contour
     */
    vector<vector<Point>> contours;
    vector<Vec4i> hierarchy;
    vector<pair<float, float>> centers;

    findContours(mask, contours, hierarchy, RETR_EXTERNAL, CHAIN_APPROX_NONE);

    for (int i = 0; i < contours.size(); i++) {
        int area = contourArea(contours[i]);
        vector<vector<Point>> valid(contours.size());
        vector<Rect> boundRect(contours.size());

        // Filter for large contours
        if (area > CONTOUR_SIZE) {
            // Bound contour
            float peri = arcLength(contours[i], true);
            approxPolyDP(contours[i], valid[i], CONTOUR_PRECISION * peri, true);
            boundRect[i] = boundingRect(valid[i]);

            // Calculate contour center of mass and add it to centers vector
            Moments m = moments(contours[i]);
            float cx = m.m10 / m.m00;
            float cy = m.m01 / m.m00;
            centers.push_back(make_pair(cx, cy));

            // Draw contours to output image
            if (show_contours) {
                drawContours(img, valid, i, Scalar(255, 0, 255), 2);
            }
        }
    }

    return centers;
}

bool validPoints(vector<float> points) {
    /**
     * Determines whether a point arc is valid (concave), used to filter arcs that are not thrown.
     */

    if (points.size() != 6) {
        return 0;
    }

    // Find y-coordinate the along line between first and last points at mid-point x value.
    float mid = (points[5] - points[1]) / (points[4] - points[0]) * (points[2] - points[0]) + points[1];

    // If the mid point is smaller than the found value the quadratic is concave and valid
    return points[3] >= mid;
}


int main() {
    /**
     * Initisalises the program and enters main loop.
     */

    // Image data structures
    VideoCapture cap(0);
    Mat img, imgHSV, mask, imgBlur;

    // Number of ball arc positions saved (how many frames to keep info)
    vector<pair<float, float>> past(NODES);
    vector<pair<float, float>> recent_centers;

    // Number of nodes in grid for quadratic interpolent
    bool show_contours = true, show_center = true;

    // namedWindow("Trackbars", (640, 20));
    // createTrackbar("Center", "Trackbars", &showCent, 1);
    // createTrackbar("Contour", "Trackbars", &showCont, 1);
    // createTrackbar("Hue Min", "Trackbars", &hmin, 179);
    // createTrackbar("Hue Max", "Trackbars", &hmax, 179);
    // createTrackbar("Sat Min", "Trackbars", &smin, 255);
    // createTrackbar("Sat Max", "Trackbars", &smax, 255);
    // createTrackbar("Val Min", "Trackbars", &vmin, 255);
    // createTrackbar("Val Max", "Trackbars", &vmax, 255);

    Client client(HOST, PORT);

    int frame = 0;
    while (true) {

        // Read image from camera, flip it, blur it and find large contours that fit colour requirements
        cap.read(img);

        flip(img, img, 1);
        cvtColor(img, imgHSV, COLOR_BGR2HSV);

        Scalar lower(HUE_MIN, SAT_MIN, VAL_MIN);
        Scalar upper(HUE_MAX, SAT_MAX, VAL_MAX);

        inRange(imgHSV, lower, upper, mask);
        GaussianBlur(mask, imgBlur, Size(3, 3), 3, 0);

        // Find centers of valid contours
        recent_centers = findLargeContours(mask, img, show_contours);

        // Overwrite past vector cyclicly with new center information
        if (recent_centers.size()) {
            past[frame % NODES] = recent_centers[0];
            frame ++;
        }

        // Create and send packet to server with spaced points
        vector<float> packet_data = {
            past[0].first,
            past[0].second,
            past[2].first,
            past[2].second,
            past[4].first,
            past[4].second,
        };

        if (validPoints(packet_data)) {
            client.sendFloatVector(packet_data);
        }

        if (show_center && recent_centers.size()) {
            pair<float, float> p = recent_centers[0];
            if (p.first != 0 || p.second != 0) {
                circle(img, Point(p.first, p.second), 3, Scalar(0, 225, 0), 3);

            }
        }

        imshow("img", img);
        waitKey(1);
    }

}
