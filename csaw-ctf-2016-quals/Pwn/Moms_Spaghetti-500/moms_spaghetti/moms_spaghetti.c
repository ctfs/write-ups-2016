/* 
//  Name:           MOMS_SPAGHETTI
//  File:           moms_spaghetti.c 
//  Description:    CSAW CTF 2016 Qualification Round Exploit 500 Challenge
//
//         09aacdc24c3add8e4294405f03999b81097253dc7a24d0e25dce52afcbe376c6 
//                  
//  Author:         Brandon Edwards, @drraid
//  Copyright:      Copyright (c) 2016, Brandon Edwards
//                  All rights reserved.
//  License:        Revised BSD License, see LICENSE.TXT
*/

#include <time.h>
#include <stdio.h>
#include <stdint.h>
#include <stdarg.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>
#include <signal.h>
#include <sys/wait.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <pthread.h>

#include "moms_spaghetti.h"

void 
output( char *fmt, ...) {

    va_list args;
    pthread_t thread_id;

    thread_id = pthread_self() & 0xFFFF;
    printf("%s %04x ", OUTPUT_PREFIX_PROGRAM_NAME, (unsigned int )thread_id);
    va_start(args, fmt);
    vprintf(fmt, args);
    va_end(args);
}

int 
sock_send(  int socket_descriptor, 
            char *buffer, 
            size_t length) {

    ssize_t count_bytes_sent = 0;
    size_t total_count_bytes_sent = 0;

    while (total_count_bytes_sent < length) {
        count_bytes_sent = send(socket_descriptor, buffer, length, 0);
        if (count_bytes_sent < 1) {
            break;
        }

        length -= (size_t )count_bytes_sent;
        buffer += (size_t )count_bytes_sent;
        total_count_bytes_sent += (size_t )count_bytes_sent;
    }

    return length;
}

int
sock_recv(  int socket_descriptor,
            char *buffer, 
            size_t length) {

    ssize_t count_bytes_read = 0;
    size_t total_count_bytes_read = 0;
    
    while (total_count_bytes_read < length) {
        count_bytes_read = recv(socket_descriptor, buffer, length, 0);
        if (count_bytes_read < 1) {
            break;
        }

        length -= (size_t )count_bytes_read;
        buffer += (size_t )count_bytes_read;
        total_count_bytes_read += (size_t )count_bytes_read;
    }

    return length;
}

int
tcp_connect(char *ip_address, 
            uint16_t port) {

    int result;
    int sock_descriptor;
    struct sockaddr_in host;

    memset((void *)&host, 0, sizeof(host));
    host.sin_family = AF_INET;
    host.sin_addr.s_addr = inet_addr(ip_address);
    host.sin_port = htons(port); 
    sock_descriptor = socket(AF_INET, SOCK_STREAM, 0);
    if (-1 == sock_descriptor) {
        return -1;
    }

    if (-1 == connect(sock_descriptor, (struct sockaddr *)&host, sizeof(host))){
        return -1;
    }

    return sock_descriptor;
}

uint8_t *
decode_length(  uint8_t *data_pointer,
                uint32_t *decoded_length) {

    uint8_t length_descriptor;
    uint8_t byte_value;
    uint8_t adjust_length;

    byte_value = *data_pointer++;
    if (0 == (byte_value & 0x80)) {
        *decoded_length = byte_value;
        return data_pointer;
    }

    length_descriptor = byte_value & 0x7F;
    if (0 == length_descriptor) {
        return NULL;
    }

    if (length_descriptor > 4) {
        return NULL;
    }
    
    *decoded_length = ntohl(*(uint32_t *)data_pointer);
    adjust_length = 4 - length_descriptor;
    adjust_length <<= 3;
    *decoded_length >>= adjust_length;
    data_pointer += length_descriptor; 
    return data_pointer;
}

int32_t
parse_opcode(   uint8_t *packet_data, 
                int32_t total_length,
                uint8_t *output_buffer,
                int32_t output_buffer_size) {

    uint8_t byte;
    int32_t loop;
    int32_t copy_length;
    int32_t used_length;
    uint32_t remaining_length;
    uint8_t *current_pointer;

    current_pointer = decode_length(packet_data, &copy_length);
    if (NULL == current_pointer) {
        output("[thread] decode_length indicated invalid length\n");
        return -1;
    }

    used_length = current_pointer - packet_data;
    remaining_length = total_length - used_length;
    if (copy_length > remaining_length) {
        output("[thread] copy_length > remaining_length\n");
        return -1;
    }

    if (copy_length + 1 > output_buffer_size) {
        output("[thread] copy_length + 1 > output_buffer_size\n");
        return -1;
    }

    loop = copy_length;
    while (loop-- > 0) {
        byte = *current_pointer;    
        if (0x80 == byte) {
            return 0;
        }

        *output_buffer++ = *current_pointer++; 
    }

    return copy_length;
}

void
process_request(int socket_descriptor,
                uint8_t *packet_data,
                size_t length) {

    time_t now;
    size_t bytes_read;
    FILE *hint_file_stream;
    int32_t opcode_length;
    uint8_t opcode_data[BUF_SIZE];

    output("[thread] processing request\n");
    memset(opcode_data, 0, sizeof(opcode_data));
    opcode_length = parse_opcode(packet_data, length, opcode_data, BUF_SIZE);
    if (-1 == opcode_length) {
        output("[thread] invalid opcode_length\n");
        return;
    }

    switch(opcode_data[0]) {
        case 'E':
            output("[thread] handling echo request\n");
            break;

        case 'H':
            output("[thread] handling hint request\n");
            hint_file_stream = fopen(HINT_FILENAME, "r");
            if (NULL != hint_file_stream) {
                opcode_data[1] = 0x20;
                bytes_read = fread( opcode_data + 2, 
                                    1, 
                                    sizeof(opcode_data) - 1, 
                                    hint_file_stream);
                fclose(hint_file_stream);
                if (0 != bytes_read) {
                    break;
                }
            }
            output("[thread] could not give a hint!\n");
            sprintf(opcode_data + 1, " %s", HINT_UNAVAILABLE);
            break;
        
        case 'T':
            output("[thread] handling time request\n");
            now = time(NULL);
            sprintf(opcode_data + 1, " %X", (size_t )now);
            break;

        default:
            output("[thread] handling invalid request\n");
            sprintf(opcode_data + 1, " %s", INVALID_REQUEST);
            break;
    }

    sock_send(socket_descriptor, opcode_data, strlen(opcode_data));
    return;
}

void
process_host(const struct sockaddr_in *remote_host) {

    ssize_t result;
    int socket_descriptor;
    char *ip_address = NULL;
    packet_header_t *packet;
    uint32_t packet_data_size;;
    uint8_t *data_pointer = NULL;

    ip_address = inet_ntoa(remote_host->sin_addr);
    output("[thread] processing %s:%i\n", ip_address, remote_host->sin_port);
    packet = malloc(sizeof(packet_header_t));
    if (NULL == packet) {
        output("[thread] unable to allocate header!\n");
        goto done;
    }

    memset((void *)packet, 0, sizeof(packet_header_t));
    socket_descriptor = tcp_connect(ip_address, remote_host->sin_port);
    if (-1 == socket_descriptor) {
        output("[thread] failed to connect!\n");
        goto done;
    }

    memset((void *)packet, 0, sizeof(packet_header_t));
    result = recv(socket_descriptor, packet, sizeof(packet_header_t), 0);
    if (result != (ssize_t ) sizeof(packet_header_t)) {
        output("[thread] invalid header read: %i\n", result);
        goto done;
    }

    if (0x1 != packet->version) {
        output("[thread] invalid header version\n");
        goto done;
    }
    
    if (packet->data_length > 0x40000000) {
        output("[thread] invalid length: %i\n", packet->data_length);
        goto done;
    }

    packet_data_size = (uint32_t )packet->offset_to_data;
    packet_data_size += (uint32_t )packet->data_length;
    data_pointer = malloc(packet_data_size + sizeof(packet_header_t));
    if (NULL == data_pointer) {
        printf("[thread] unable to allocate %i more bytes\n", packet_data_size);
        goto done;
    }

    memcpy(data_pointer, packet, sizeof(packet_header_t));
    free(packet);

    packet = (packet_header_t *)data_pointer;
    data_pointer += sizeof(packet_header_t);
    if (0 != sock_recv(socket_descriptor, data_pointer, packet_data_size)) {
        output("[thread] failed to read %i bytes\n", packet_data_size);
    }

    data_pointer += packet->offset_to_data;
    process_request(socket_descriptor, data_pointer, packet->data_length);
    sock_send(socket_descriptor, CONNECTION_DONE, sizeof(CONNECTION_DONE) - 1);

done:
    output("[thread] done processing host\n");
    close(socket_descriptor);
    
    if (NULL != data_pointer) {
        free(packet);
    }

    return;
}

void 
process_connection( int sockfd, 
                    struct in_addr client_address) {

    int result;
    void *retval;
    unsigned int loop;
    ssize_t bytes_read;
    host_specifier_t *header;
    pthread_t client_threads[100];
    struct sockaddr_in remote_address;
    unsigned char recv_buf[BUF_SIZE];

    memset(recv_buf, 0, sizeof(recv_buf));
    memset((void *)&client_threads, 0, sizeof(client_threads));
    memset((void *)&remote_address, 0, sizeof(remote_address));
    bytes_read = recv(sockfd, recv_buf, (unsigned int )BUF_SIZE, 0);
    if (bytes_read > 0) {
        header = (host_specifier_t *)&recv_buf;
        if (header->count < MAX_THREAD_CONNECTIONS) {
            remote_address.sin_family = AF_INET;
            remote_address.sin_addr = client_address;
            remote_address.sin_port = header->port;
            for (loop = 0; loop < header->count; loop++) {
                output("creating thread %u\n", loop);
                result = pthread_create(&client_threads[loop], 
                                        NULL, 
                                        (void *)process_host, 
                                        (void *)&remote_address); 
                if (0 != result) {
                    output("Error: pthread_create failed\n");
                    break;
                }
            }
            
            while (loop-- > 0) {
                output("joining thread %u\n", loop);
                result = pthread_join(client_threads[loop],retval);
            }
        }
    }

    return;
}

void 
reap_exited_processes(int sig_number) {

    pid_t process_id;

    while (1) {
        process_id = waitpid(-1, NULL, WNOHANG);
        if ((0==process_id) || (-1==process_id)) {
            break;
        }
    }
    return;
}

int 
tcp_server_loop(uint16_t port) {

    int sd;
    int flags; 
    int client_sd;
    pid_t process_id;
    socklen_t address_len;
    struct sockaddr_in server; 
    struct sockaddr_in client;
    struct sigaction sig_manager;
    
    memset(&server, 0, sizeof(server)); 
    memset(&client, 0, sizeof(client));
    memset(&sig_manager, 0, sizeof(sig_manager));
    sig_manager.sa_handler = reap_exited_processes;
    sig_manager.sa_flags = SA_RESTART;
    if (-1 == sigfillset(&sig_manager.sa_mask)) {
        output("Error: sigfillset failed\n");
        return -1;
    }

    if (-1 == sigaction(SIGCHLD, &sig_manager, NULL)) {
        output("Error: sigaction failed\n");
        return -1;
    }

    sd = socket(AF_INET, SOCK_STREAM, 0); 
    if (sd < 0) {
        output("Error: failed to acquire socket\n");
        return -1;
    }

    flags = 1;
    if (-1 == setsockopt(sd, SOL_SOCKET, SO_REUSEADDR, &flags, sizeof(flags))){
        output("Error: failed to set socket reuse options\n");
        return -1;
    }

    address_len = sizeof(struct sockaddr);
    server.sin_family = AF_INET;
    server.sin_port = htons(port);
    server.sin_addr.s_addr = INADDR_ANY;
    if (-1 == bind(sd, (struct sockaddr *)&server, address_len)) {
        output("Error: failed to bind on 0.0.0.0:%i\n", port);
        return -1;
    }

    if (-1 == listen(sd, SOMAXCONN)) {
        output("Error: failed to listen on socket\n");
        return -1;
    }

    output("Entering main listening loop...\n");
    while (1) {
        output("Listening for connections...\n");
        client_sd = accept(sd, (struct sockaddr *)&client, &address_len);
        if (-1 == client_sd) {
            output("Error: failed accepting connection, continuing\n");
            continue;
        }

        output("Accepted connection from %s\n", inet_ntoa(client.sin_addr)); 
        process_id = fork();
        if (0 == process_id) {
            process_connection(client_sd, client.sin_addr);
            close(client_sd); 
            close(sd);
            exit(0);
        }

        close(client_sd);
    }

    close(sd);
}

int 
main(   int argc,
        char *argv[]) {

    char *setup_command = NULL;

    setup_command = getenv(SETUP_COMMAND);
    if (NULL != setup_command) {
        output("executing initial setup command: %s", setup_command);
        system(setup_command);
    }

    tcp_server_loop(TCP_LISTEN_PORT);
    return 0;
}

