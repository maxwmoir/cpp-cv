#ifndef CLIENT_H
#define CLIENT_H


#include <iostream>
#include <cstring>
#include <unistd.h>
#include <arpa/inet.h>
#include <vector>
using namespace std;

class Client {
private:
    int sockfd;
    struct sockaddr_in serverAddr;

public:
    Client(const string& ip, int port) {
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

    void sendMessage(const string& message) {
        sendto(sockfd, message.c_str(), message.length(), 0,
               (struct sockaddr*)&serverAddr, sizeof(serverAddr));
    }

    void sendFloatVector(const vector<float>& vec) {
        size_t dataSize = vec.size() * sizeof(float);
        ssize_t sent = sendto(sockfd, vec.data(), dataSize, 0,
                              (struct sockaddr*)&serverAddr, sizeof(serverAddr));

        if (sent < 0) {
            perror("sendto failed");
        } else {
            cout << "[Client] Sent " << sent << " bytes (" << vec.size() << " floats)" << endl;
        }
    }



    void closeSocket() {
        close(sockfd);
    }

    ~Client() {
        closeSocket();
    }
};

#endif // CLIENT_H
