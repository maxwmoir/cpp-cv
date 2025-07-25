/**
 * @file <main_test.cc>
 * @brief Google test file to test functions used for the trajectory tool.
 *
 * @author Max Moir
 * @date 20/07/2025
 */

#include <gtest/gtest.h>
#include <vector>
#include "utils.h"

// Demonstrate some basic assertions.
TEST(ConcavityTest, BasicAssertions) {

    vector<float> points = {0.0, 0.0, 1.0, 10.0, 2.0, 2.0};




    EXPECT_EQ(checkConcavity(points), true);

    points = {0.0, 0.0, 0.5, 0.5, 1.0, 1.0};

    bool first = checkConcavity(points);

    EXPECT_EQ(checkConcavity(points), true);

    points = {0.0, 0.0, 0.5, 0.4999, 1.0, 1.0};

    EXPECT_EQ(checkConcavity(points), false);

    points = {100.0, 5.0, 50.0, 19, 0.0, 6.0};

    EXPECT_EQ(checkConcavity(points), true);

}

TEST(MovementTest, BasicAssertions) {

    vector<float> points = {0.0, 0.0, 1.0, 10.0, 2.0, 2.0};

    EXPECT_EQ(checkMovement(points, 2), true);

}
