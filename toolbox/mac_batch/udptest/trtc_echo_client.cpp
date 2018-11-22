/* TRTC UDP relay server program.c */

#include <inttypes.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <sys/time.h>

#define MAXBUF 1024*1024

struct sockaddr_in serverAddr;
struct sockaddr_in other;

const size_t kMinRtpPacketLen = 12;
static const uint8_t kRtpVersion = 2;

bool IsRtpPacket(const void* data, size_t len) {
  if (len < kMinRtpPacketLen)
    return false;

  return (static_cast<const uint8_t*>(data)[0] >> 6) == kRtpVersion;
}

void DumpHex(const void* data, size_t size) {
  char ascii[17];
  size_t i, j;
  ascii[16] = '\0';
  for (i = 0; i < size; ++i) {
    fprintf(stdout, "%02X ", ((unsigned char*)data)[i]);
    fflush(stdout);
    if (((unsigned char*)data)[i] >= ' ' && ((unsigned char*)data)[i] <= '~') {
      ascii[i % 16] = ((unsigned char*)data)[i];
    } else {
      ascii[i % 16] = '.';
    }
    if ((i+1) % 8 == 0 || i+1 == size) {
      fprintf(stdout, " ");
      fflush(stdout);
      if ((i+1) % 16 == 0) {
	fprintf(stdout, "|  %s \n", ascii);
	fflush(stdout);
      } else if (i+1 == size) {
	ascii[(i+1) % 16] = '\0';
	if ((i+1) % 16 <= 8) {
	  fprintf(stdout, " ");
	  fflush(stdout);
	}
	for (j = (i+1) % 16; j < 16; ++j) {
	  fprintf(stdout, "   ");
	  fflush(stdout);
	}
	fprintf(stdout, "|  %s \n", ascii);
	fflush(stdout);
      }
    }
  }
}

void relay(int sd, char *relayPort) {
    fd_set reads, temps;
    int result = 0;
    struct timeval timeout;
    int rn, sn;
    socklen_t len = sizeof(other);;
    unsigned char bufin_[MAXBUF];
    struct sockaddr_in remote;
    
    FD_ZERO(&reads);
    FD_SET(sd, &reads);

    int count = 2;
    while (count--) {
        temps = reads;
	usleep(100);
	unsigned short data = htons(atoi(relayPort));
	sn = sendto(sd, &data, sizeof(unsigned short), 0, (struct sockaddr *)&other, len);
	fprintf(stdout, "socket %d from %14s:%5d [%5d] echo ----> %14s:%5d [%5d]\n", sd, inet_ntoa(serverAddr.sin_addr), ntohs(serverAddr.sin_port), rn, inet_ntoa(other.sin_addr), ntohs(remote.sin_port), sn);
	fflush(stdout);
    }
}

int main(int argc, char **argv) {
    if(argc != 3) {
        fprintf(stdout, "Usage : %14s <dest_ip> <dest_port>\n", argv[0]);
	fflush(stdout);
        exit(1);
    }
    
    int sock;
    socklen_t length;
    
    if ((sock = socket( PF_INET, SOCK_DGRAM, 0 )) < 0) {
        fprintf(stdout, "Problem creating socket\n");
	fflush(stdout);
        exit(1);
    }
    
    int optvalue = 1;
    if (setsockopt(sock,SOL_SOCKET, SO_REUSEADDR, &optvalue, sizeof(optvalue)) < 0) {
        fprintf(stdout, "Error Reuse binding\n");
	fflush(stdout);
        exit(0);
    }
    
    /* find out what port we were assigned and print it out */
    
    fprintf(stdout, "--------------------\n");
    fprintf(stdout, "DEST  : %s:%s\n", argv[1], argv[2]);
    fprintf(stdout, "--------------------\n");
    fflush(stdout);    

    other.sin_family = AF_INET;
    other.sin_addr.s_addr = inet_addr(argv[1]);
    other.sin_port = htons(atoi(argv[2]));
    
    relay(sock, argv[2]);
    close(sock);
    return(0);
}
