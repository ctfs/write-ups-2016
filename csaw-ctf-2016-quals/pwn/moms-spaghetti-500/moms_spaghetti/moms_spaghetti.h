#ifndef __MOMS_SPAGHETTI__
#define __MOMS_SPAGHETTI__

#define BUF_SIZE 256
#define VALUE_BUF_SIZE 64
#define TCP_LISTEN_PORT 24242
#define OUTPUT_PREFIX_PROGRAM_NAME "MOMS_SPAGHETTI"
#define CONNECTION_DONE " DONE"
#define INVALID_REQUEST "INVALID REQUEST! "
#define HINT_FILENAME "hint.txt"
#define HINT_UNAVAILABLE "HINT UNAVAILABLE"
#define SETUP_COMMAND "SPAGHETTI_SETUP_COMMAND"
#define MAX_THREAD_CONNECTIONS 100

typedef struct host_specifier_s {
    unsigned short count;
    unsigned short port;
} host_specifier_t;

typedef struct packet_header_t {
    uint16_t version;
    uint16_t offset_to_data;
    uint32_t data_length;
} packet_header_t;

void output(char *fmt, ...);

int sock_send(  int sockfd, 
                char *buffer, 
                size_t length);

int sock_recv(  int socket_descriptor,
                char *buffer, 
                size_t length);

int tcp_connect(char *ip_address, 
                uint16_t port);

void process_host(const struct sockaddr_in *remote_host);

void process_connection(int socket_descriptor,
                        struct in_addr client);

void process_request(   int socket_descriptor,
                        uint8_t *packet_data,
                        size_t length);

int32_t parse_opcode(   uint8_t *packet_data, 
                        int32_t total_length,
                        uint8_t *output_buffer,
                        int32_t output_buffer_size);

uint8_t *decode_length( uint8_t *data_pointer,
                        uint32_t *decoded_length);

int tcp_server_loop(uint16_t port);

void reap_exited_processes(int sig_number);

#endif
