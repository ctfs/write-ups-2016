#include <stdio.h>
#include <stdlib.h>
#include <gcrypt.h>
#include <assert.h>
#include <string.h>
#include <unistd.h>
#include <openssl/rand.h>
#include <gnutls/gnutls.h>
#include <gnutls/crypto.h>

#ifndef FLAG
#define FLAG "HITCON{xxxxxxxxxxxxxxxxxxxxxxxxxxxxx}"
#endif

const char flag[] = FLAG;
int type = 0;
char *method[] = {
    "1. /dev/urandom",
    "2. openssl",
    "3. grypt",
    "4. gnutls"
};

char* gen_key(size_t l)
{
    char *key = (char*) malloc(l);
    if (!key) {
        puts("Error, plz contact admin");
        exit(1);
    }

    if (type == 0) {
        FILE *fp = fopen("/dev/urandom", "r");
        if (!fp) {
            puts("Error, plz contact admin");
            exit(1);
        }
        fread(key, 1, l, fp);
        fclose(fp);
    } else if (type == 1) {
        RAND_bytes(key, l);
    } else if (type == 2) {
        gcry_randomize(key, l, GCRY_STRONG_RANDOM);
    } else if (type == 3) {
        gnutls_rnd(GNUTLS_RND_NONCE, key, l);
    } else {
        puts("Unsupport method.");
        exit(1);
    }

    return key;
}

void encrypt()
{
    printf("PRNG method: %s\n", method[type]);

    puts("len?");
    size_t len = read_int();
    if (len <= 0 || len >= 0x10000) {
        puts("Too big!");
        exit(0);
    }

    size_t out_len = len + strlen(flag);
    char *buf = (char*) malloc(out_len + 1);
    if (!buf) {
        puts("Error, plz contact admin");
        exit(1);
    }
    bzero(buf, out_len + 1);
    puts("data?");
    read(0, buf, len);
    memcpy(buf + len, flag, strlen(flag));

    char *key = gen_key(out_len);

    for (int i = 0; i < out_len; i++)
        buf[i] ^= key[i];

    puts("encrypt content:");
    for (int i = 0; i < out_len; i++)
        printf("%02x", buf[i] & 0xff);
    puts("");

    free(key);
    free(buf);
    exit(0);
}

void prng()
{
    for (int i = 0; i < sizeof(method)/sizeof(char*); i++)
        puts(method[i]);
    printf("> ");
    type = (read_int()-1) % 4;
}

int menu()
{
    puts("====== OTP system ======");
    puts("1. encrypt");
    puts("2. change PRNG");
    puts("3. exit");
    printf("> ");
    return read_int();
}

int read_int()
{
    char buf[0x10];
    fgets(buf, 0x10, stdin);
    return atoi(buf);
}

void motd()
{
    puts("Welcome to OTP system.");
    puts("OTP system can help to encrypt your content with a random key.");
    puts("The flag will be hide in the encrypted file. :)");
}

int main()
{

    setvbuf(stdout, 0, 2, 0);
    setvbuf(stdin, 0, 2, 0);

    motd();

    while(1) {
        switch (menu()) {
            case 1:
                encrypt();
                break;
            case 2:
                prng();
                break;
            case 3:
                puts("bye~");
                exit(0);
        }
    }
}
