// gcc ./blag.c -m32 -fstack-protector-all -o blag

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXPOSTS 8

typedef struct {
    int adminonly;
    char author[32];
    char title[32];
    char body[320];
} Post;

char adminpassword[32];
int numposts = 0;
int isadmin = 0;
Post* posts[MAXPOSTS];

void readline(char* buf, int n, FILE* in) {
    fgets(buf, n, in);
    buf[strcspn(buf, "\n")] = 0; // strip newline
}

void auth() {
    char buf[32];
    printf("Enter admin password:\n");
    readline(buf,32,stdin);
    if (!strcmp(adminpassword, buf)) {
        printf("Authenticated!\n");
        isadmin = 1;
    } else {
        printf("Wrong password!\n");
    }
}

void addpost() {
    if (numposts >= MAXPOSTS) {
        printf("Blag is full!\n");
        return;
    }
    Post* p = posts[numposts];
    char buf[32];
    printf("Author?\n");
    readline(buf,sizeof(p->author),stdin);
    strcpy(p->author,buf);
    printf("Title?\n");
    readline(buf,sizeof(p->title),stdin);
    strcpy(p->title,buf);
    printf("Body?\n");
    readline(buf,sizeof(p->body),stdin);
    strcpy(p->body,buf);
    numposts++;
}

void listposts() {
    int i;
    for (i = 0; i < numposts; i++) {
        Post* p = posts[i];
        printf("Post #%d: %s by %s\n",i,p->title,p->author);
    }
}

void readpost() {
    int i;
    char buf[8];
    printf("Index?\n");
    readline(buf,sizeof(buf),stdin);
    sscanf(buf, "%d", &i);
    if (i >= numposts || i < 0) {
        printf("Invalid index!\n");
        return;
    }
    Post* p = posts[i];
    if (!isadmin && p->adminonly) {
        printf("Admin only!\n");
        return;
    }
    printf("%s by %s:\n%s\n",p->title,p->author,p->body);
}

void menu() {
    printf("Commands:\n"
           "\n"
           "list: List all posts.\n"
           "read: Read post.\n"
           "add: Add post.\n"
           "auth: Authenticate as admin.\n"
           "quit: Exactly what it says on the tin.\n");
    char line[8];
    while (1) {
        printf("> ");
        readline(line, sizeof(line), stdin);
        if (!strcmp(line,"list")) {
            listposts();
        } else if (!strcmp(line,"read")) {
            readpost();
        } else if (!strcmp(line,"add")) {
            addpost();
        } else if (!strcmp(line,"auth")) {
            auth();
        } else if (!strcmp(line,"quit")) {
            break;
        } else {
            printf("Invalid command.\n");
        }
    }
}

void readpostsfromfile() {
    char line[320];
    FILE *in;
    int i;
    int adminpost;
    Post* p;
    if ((in = fopen("blogposts.txt","r")) == NULL) {
        printf("Can't read blog posts!");
        exit(1);
    }
    fgets(line, sizeof(line), in);
    sscanf(line, "%d", &numposts);
    for (i = 0; i < numposts; i++) {
        p = posts[i];
        readline(line, sizeof(line), in);
        sscanf(line, "%d", &p->adminonly);
        readline(line, sizeof(line), in);
        strcpy(p->author,line);
        readline(line, sizeof(line), in);
        strcpy(p->title,line);
        readline(line, sizeof(line), in);
        strcpy(p->body,line);
    }
    fclose(in);
}

int main(int argc, const char* argv[]) {
    int i;
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);

    memset(adminpassword, 0, sizeof(adminpassword));
    FILE *in;
    if ((in = fopen("adminpassword.txt","r")) == NULL) {
        printf("Can't read admin password!");
        exit(1);
    }
    readline(adminpassword, sizeof(adminpassword), in);
    fclose(in);
    for (i = 0; i < MAXPOSTS; i++) {
        posts[i] = malloc(sizeof(Post));
        memset(posts[i],0,sizeof(Post));
    }
    readpostsfromfile();
    menu();
}
