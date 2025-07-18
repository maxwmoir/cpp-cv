/**
 * @file <client.h>
 * @brief UDP client class implementation for sending float vectors to a server
 *
 * @author Max Moir
 * @date 10/07/2025
 */

#ifndef CLIENT_H
#define CLIENT_H


#include <iostream>
#include <cstring>
#include <unistd.h>
#include <arpa/inet.h>
#include <vector>

using namespace std;

/**
 * Simple UDP cliemt to connect to a socket, and send node information to the host server
 */
class Client {

    private:

        int sockfd;
        struct sockaddr_in serverAddr;

    public:

        Client(const string& ip, int port) {
            /**
             * Initialises the client object and socket connection
             *
             * @throws Socket creation error if binding fails
             */

            sockfd = socket(AF_INET, SOCK_DGRAM, 0);

            if (sockfd < 0) {
                perror("Socket creation failed");
                exit(EXIT_FAILURE);
            }

            memset(&serverAddr, 0, sizeof(serverAddr));
            serverAddr.sin_family = AF_INET;
            serverAddr.sin_port = htons(port);
            inet_pton(AF_INET, ip.c_str(), &serverAddr.sin_addr);
        }

        void sendFloatVector(const vector<float>& points) {
            /**
             * Sends a vector of floats in a datagram to the python server.
             *
             * @param points Ball trajectory points to send to server
             * @throws Sending error if sendto fails
             */
            size_t dataSize = points.size() * sizeof(float);
            ssize_t sent = sendto(sockfd, points.data(), dataSize, 0,(struct sockaddr*)&serverAddr, sizeof(serverAddr));

            if (sent < 0) {
                perror("Datagram sending failed");
            } else {
                cout << "Sent " << sent << " bytes (" << points.size() << " floats)" << endl;
            }
        }


        void closeSocket() {
            /**
             * Closes the client's socket
             */
            close(sockfd);
        }

        ~Client() {
            /**
             * Closes socket on object destruction
             */
            closeSocket();
        }
};

#endif // CLIENT_H
