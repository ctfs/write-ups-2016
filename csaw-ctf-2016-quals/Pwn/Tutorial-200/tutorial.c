#define _GNU_SOURCE
#include <stdio.h>
#include <pwd.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <dlfcn.h>
#include <errno.h>
#include <signal.h>
#include <unistd.h>
#include <stdint.h>

int priv(char *username) {
    struct passwd *pw = getpwnam(username);
    if (pw == NULL) {
        fprintf(stderr, "User %s does not exist\n", username);
        return 1;
    }

    if (chdir(pw->pw_dir) != 0) {
        perror("chdir");
        return 1;
    }


    if (setgroups(0, NULL) != 0) {
        perror("setgroups");
        return 1;
    }

    if (setgid(pw->pw_gid) != 0) {
        perror("setgid");
        return 1;
    }

    if (setuid(pw->pw_uid) != 0) {
        perror("setuid");
        return 1;
    }

    return 0;
}

void func1(int fd){
    
   
	char address[50];
	void (*puts_addr)(int) = dlsym(RTLD_NEXT,"puts");
    	write(fd,"Reference:",10);
	sprintf(address,"%p\n",puts_addr-0x500);
    	write(fd,address,15);


    
}

void func2(int fd){    
    char pov[300];
    bzero(pov,300);    

    write(fd,"Time to test your exploit...\n",29);
    write(fd,">",1);
    read(fd,pov,460);
    write(fd,pov,324);

}

   
    
void menu(int fd){
    while(1){
        char option[2];
        write(fd,"-Tutorial-\n",11);
        write(fd,"1.Manual\n",9);
        write(fd,"2.Practice\n",11);
        write(fd,"3.Quit\n",7);
        write(fd,">",1);        read(fd,option,2);
        switch(option[0]){
            case '1':
                func1(fd);
                break;
            case '2':
                func2(fd);
                break;
            case '3':
                write(fd,"You still did not solve my challenge.\n",38);
                return;
            default:
                write(fd,"unknown option.\n",16);
                break;
        }    
    }
}

int main( int argc, char *argv[] ) {   
  int five;
  int myint = 1;   
  struct sockaddr_in server,client;    
  sigemptyset((sigset_t *)&five);   
  int init_fd = socket(AF_INET, SOCK_STREAM, 0);     

  if (init_fd == -1) {
     perror("socket");
     exit(-1);
  }   
  bzero((char *) &server, sizeof(server));   
  
  if(setsockopt(init_fd,SOL_SOCKET,SO_REUSEADDR,&myint,sizeof(myint)) == -1){
    perror("setsocket");
      exit(-1);
  }   
  
  server.sin_family = AF_INET;
  server.sin_addr.s_addr = htonl(INADDR_ANY);
  server.sin_port = htons(atoi(argv[1]));   

  if (bind(init_fd, (struct sockaddr *) &server, sizeof(server)) == -1) {
     perror("bind");
     exit(-1);
  }   
  
  if((listen(init_fd,20)) == -1){
     perror("listen");
     exit(-1);
  }   
  int addr_len = sizeof(client);   

   while (1) {      

        int fd = accept(init_fd,(struct sockaddr *)&client,(socklen_t*)&addr_len);      

     if (fd < 0) {
        perror("accept");
        exit(1);
     }      
     pid_t pid = fork();      
     
     if (pid == -1) {
       perror("fork");
       close(fd);      
     }
      
     if (pid == 0){
	  alarm(15);
          close(init_fd);
	  int user_priv = priv("tutorial");
	  if(!user_priv){
          	menu(fd);
		close(fd);
	        exit(0);
	  }
     }else{
            close(fd);
      }   

    }
  close(init_fd);
}

