#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define true 1
#define false 0

typedef int bool;
typedef struct http_header
{
    char *key;
    char *value;
} http_header_t;

typedef struct req_header
{
    char http_version[9];
    char url[50];
    char method[33];
    void (*error_callback)();
    http_header_t** headers;
    int header_c;
} req_header_t;

typedef struct response
{
    char* code;
    char* short_desc;
    http_header_t** headers;
    int header_c;
    char* content;
} response_t;


void return_resp(response_t* resp, bool final)
{
    int i;

    printf("HTTP/1.1 %s %s\n", resp->code, resp->short_desc);
    for (i = 0; i < resp->header_c; i++) {
        printf("%s: %s\n", resp->headers[i]->key, resp->headers[i]->value);
    }
    printf("\n");
    printf("%s\n", resp->content);
    if (final)
        exit(0);
}

void return_400()
{
    http_header_t** headers = malloc(2*sizeof(http_header_t*));
    headers[0] = malloc(sizeof(http_header_t));
    headers[0]->key = "Content-Type";
    headers[0]->value = "text/html; charset=utf-8";
    headers[1] = malloc(sizeof(http_header_t));
    headers[1]->key = "Server";
    headers[1]->value = "httc/1.0 Ubuntu/14.04.2";

    response_t* resp = malloc(sizeof(response_t));
    resp->code = "400";
    resp->short_desc = "BAD REQUEST";
    resp->headers = headers;
    resp->header_c = 2;
    resp->content = "<html><head><title>400 Bad Request</title></head><body>400 Bad Request<br/>Are you trying to hack me?</body></html>\n";
    return_resp(resp, true);
}

response_t* hacker_response(char* desc)
{
    http_header_t** headers = malloc(2*sizeof(http_header_t*));
    headers[0] = malloc(sizeof(http_header_t));
    headers[0]->key = "Content-Type";
    headers[0]->value = "text/html; charset=utf-8";
    headers[1] = malloc(sizeof(http_header_t));
    headers[1]->key = "Server";
    headers[1]->value = "httc/1.0 Ubuntu/14.04.2";

    response_t* resp = malloc(sizeof(response_t));
    resp->code = "200";
    resp->short_desc = "OK";
    resp->headers = headers;
    resp->header_c = 2;
    
    char* content = malloc(sizeof(char) * 1000);
    snprintf(content, 1000, "<html><head><title>STOP TRYING TO HACK ME</title></head><body><p>%s</p></body></html>\n", desc);
    resp->content = content;
    return resp;
}

char* get_line(bool required)
{
    char* line = NULL;
    size_t size;

    if (getline(&line, &size, stdin) == -1){
        if (required)
            return_400();
    }
    
    return line;
}

req_header_t* get_header()
{
    req_header_t* header = malloc(sizeof(req_header_t));
    http_header_t* l;
    char* line, tmp;
    char key[51], value[51], method[51], url[51], http_version[51];

    header->headers = malloc(sizeof(http_header_t*));
    header->header_c = 0;

    line = get_line(true);

    if(line == NULL || sscanf(line, "%33[^ ] %50[^ ] %8[^ ]", method, url, http_version) != 3) {
        return_400();
    }
    memcpy(header->http_version, http_version, 8);
    memcpy(header->method, method, 33);
    memcpy(header->url, url, 50);
    header->error_callback = &exit;

    while (line = get_line(false)) {
        if(line == NULL)
            return_400();

        if (sscanf(line, "%50[^:]: %50[^\n]", key, value) != 2) {
            break;
        }
        else {
            header->headers = realloc(header->headers, sizeof(http_header_t*)*(++header->header_c));
            header->headers[header->header_c-1] = malloc(sizeof(http_header_t));
            l = header->headers[header->header_c-1];
            l->key = key;
            l->value = value;
        }
    }               

    return header;
}

char* clean_url(char* original)
{
    char tmp_result[50];
    bool modified = false;
	int i;

    if (strlen(original) < 1 || original[0] != '/') {
        return_resp(hacker_response("please stop trying to hack me thanks"), true);
    }

    if (!strcmp(original, "/")) {
        return "/index.html";
    }

	for (i=0; i<strlen(original); i++) {
		if (original[i] == '.') {
			if (i < strlen(original)-1 && original[i+1] == '.') {
                return_resp(hacker_response("WHOOP WHOOP hAcKeR ALERT"), true);
            }
        }
        if (original[i] == '#' || original[i] == '?') {
            strncpy(&tmp_result[i], "\0", 1);
            modified = true;
        }
        else {
            strncpy(&tmp_result[i], &original[i], 1);
        }

        if (original[i] == '\0') {
            break;
        }
	}

    if (!modified) {
        return original;
    }
    else {
        char* result = malloc(sizeof(char)*50);
        strncpy(result, tmp_result, 50);
        return result;
    }
}

response_t* process_request(req_header_t* request)
{
    FILE *fp;

    char *c_url, *false_req;
    response_t* resp;
    http_header_t** headers;

    c_url = clean_url(request->url);

    if (strncmp(request->method, "GET", 3)) {
        headers = malloc(3*sizeof(http_header_t*));
        headers[0] = malloc(sizeof(http_header_t));
        headers[0]->key = "Content-Type";
        headers[0]->value = "text/html; charset=utf-8";
        headers[1] = malloc(sizeof(http_header_t));
        headers[1]->key = "Allow";
        headers[1]->value = "GET";
        headers[2] = malloc(sizeof(http_header_t));
        headers[2]->key = "Server";
        headers[2]->value = "httc/1.0 Ubuntu/14.04.2";

        false_req = malloc(sizeof(char)*1000);
        snprintf(false_req, 1000, "<html><head><title>405 Method Not Allowed</title></head><body>405 Method Not Allowed<br/>The method %s is not supported.</body></html>\n", request->method);
        resp = malloc(sizeof(response_t));
        resp->code = "405";
        resp->short_desc = "NOT ALLOWED";
        resp->headers = headers;
        resp->header_c = 3;
        resp->content = false_req;
        return resp;
    }

    char path[101];
    strcpy(path, "/home/app/web/");
    strncpy(path + strlen(path), c_url, 50);
    strncpy(path + 100, "\0", 1);
    fp = fopen(path, "r");
    if (!fp) {
        headers = malloc(2*sizeof(http_header_t*));
        headers[0] = malloc(sizeof(http_header_t));
        headers[0]->key = "Content-Type";
        headers[0]->value = "text/html; charset=utf-8";
        headers[1] = malloc(sizeof(http_header_t));
        headers[1]->key = "Server";
        headers[1]->value = "httc/1.0 Ubuntu/14.04.2";

        char* content = malloc(sizeof(char)*1000);
        snprintf(content, 1000, "<html><head><title>404 Not Found</title></head><body>404 Not Found<br/>The URL %s doesn't exist. What are you, stupid?</body></html>\n", c_url);
        resp = malloc(sizeof(response_t));
        resp->code = "404";
        resp->short_desc = "NOT FOUND";
        resp->headers = headers;
        resp->header_c = 2;
        resp->content = content;
        return resp;
    }

    char* content = malloc(sizeof(char)*4097);
    fread(content, 1, 4096, fp);
    fclose(fp);
    
    headers = malloc(2*sizeof(http_header_t*));
    headers[0] = malloc(sizeof(http_header_t));
    headers[0]->key = "Content-Type";
    headers[0]->value = "text/html; charset=utf-8";
    headers[1] = malloc(sizeof(http_header_t));
    headers[1]->key = "Server";
    headers[1]->value = "httc/1.0 Ubuntu/14.04.2";

    resp = malloc(sizeof(response_t));
    resp->code = "200";
    resp->short_desc = "OK";
    resp->headers = headers;
    resp->header_c = 2;
    resp->content = content;
    return resp;
}

int main()
{
    int i;
    setbuf(stdout, NULL);

    while (true) {
        req_header_t* request = get_header();
        response_t* response = process_request(request);
        return_resp(response, false);

        for (i=0; i++; i<request->header_c) {
            free(request->headers[i]);
        }
        free(request->headers);
        free(request);

        free(response);
    }
    return 0;
}
