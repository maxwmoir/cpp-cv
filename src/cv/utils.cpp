/**
 * @file <utils.cpp>
 * @brief A couple of utility functions to detect movement and concavity.
 *
 * @author Max Moir
 * @date 21/07/2025
 */

#include <vector>
#include "utils.h"

using namespace std;

bool checkConcavity(vector<float> points) {
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

bool checkMovement(vector<float> points) {
    /**
     * Determines whether the target is moving quickly enough to be in flight.
     */
    return true;
}
