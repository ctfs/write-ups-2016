#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <fcntl.h>

#define QUERY "What's your name?\n"
#define DEFAULT "Default Highscore \x00"
#define NAME  0xf8 
#define HIGH  512

typedef struct player{
	int score;
	int namelen;
	char* name;
	char  ascii[26];
	char  padding[79];
}play,*pptr;

void play_game(pptr p,int rand);
pptr get_name();

char highest[HIGH];	
int  hscore;
pptr p;		

void main(void){
	int rand;
	char select;

	setvbuf(stdout,NULL,_IONBF,0);
	memset(highest,0,HIGH);
	memcpy(highest,DEFAULT,sizeof(DEFAULT));	
	hscore = 0x40;

	rand = open("/dev/urandom",O_RDONLY);
	if(rand == -1){
		exit(EXIT_FAILURE);	
	}

	p = get_name();	
	
	printf("Welcome %s\n",p->name);	

	while(1){
		play_game(p,rand);	
		printf("%s ",highest);
		printf("score: %d\n",hscore);
		printf("Continue? ");	
		scanf(" %c",&select);	
		switch(select){
			case 'n':
			goto EXIT;
			default:
			break;
		}
	}
EXIT:
	close(rand);
}

void play_game(pptr p,int rand){
	char* buff; 
	int len = p->namelen;
	buff = malloc(len);	
	if(!buff){
		return;
	}
	read(rand,buff,len);	
	
	for(size_t i = 0;i < len-1;++i){
		buff[i] ^= p->name[i];	
		buff[i] = (((unsigned char)buff[i] % 26)+97);
	}

	int chance = 3;
	int count = 0;
	char c = '_';
	while(chance > 0){
		for(size_t i=0;i<len-1;++i){
			if(p->ascii[buff[i]-97]){
				write(STDOUT_FILENO,buff+i,1);
			}	
			else {write(STDOUT_FILENO,"_",1);}
		}
		write(STDOUT_FILENO,"\n",1); scanf(" %c",&c);	
		if(c < 97 || c > 122){
			printf("nope\n");
			chance--;
			continue;
		}
		else if(p->ascii[c-97]){
			printf("nope\n");
			chance--;
			continue;
		}
		else{
			int prev = count;
			for(size_t i=0;i<len-1;++i){
				if(c == buff[i]){
					p->ascii[c-97] = 1;
					count++;
				}
			}			
			if(prev == count) chance--;
			if(count >= len-1){
				p->score += 32 * (0.25 * (len-1));
				goto END;
			}
		}

	}
	p->score += count*(0.25 * (len-1)) ;
END:
 	if(p->score > hscore ){
		char d;
		char* e;
                int len;
		char* new_name;

		printf("High score! change name?\n");
		scanf(" %c",&d);
		if(d == 'y'){
			new_name = malloc(NAME);
			memset(new_name,0,NAME);
			len = read(STDIN_FILENO,new_name,NAME);
			p->namelen = len;
			if(e = strchr(new_name,'\n')) *e = '\x00';
			/*memcpy bug wrong length in use*/
			/*second iteration of this loop will allow you to write to memory*/
			memcpy(p->name,new_name,len);
			free(new_name);
		}
		/*able to leak an address corrupting the struct in memory*/
               	snprintf(highest,HIGH,"Highest player: %s",p->name);
		hscore = p->score;
          }
	memset(p->ascii,0,26);
	free(buff);
}

pptr get_name(){
	char name[NAME];
	char* c;
	int len;
	pptr p;

	write(STDOUT_FILENO,QUERY,sizeof(QUERY)-1);
	memset(name,0,NAME);
	len = read(STDIN_FILENO,name,NAME-1);

	if(c = strchr(name,'\n')){
		*c = '\x00';	
	}
		
	c = malloc(len);
	p = malloc(sizeof(play));
	memset(p,0,sizeof(play));

	p->name = c;
	p->namelen = len;

	memcpy(p->name,name,len);
	return p;
}

