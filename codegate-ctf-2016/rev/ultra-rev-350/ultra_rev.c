#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void dec(char *path, char *allData)
{
	/*
	
	decrypt your file
	allData[a]^key[b]^key2[c]^key3[d]
	
	*/
}
int check(unsigned short a1, int startAddr, unsigned int Size, char *allData)
{
	unsigned int v3;
	unsigned int v4;
	unsigned int v5;
	signed int v6;
	int v7;
	unsigned int v8;
	unsigned long long v9;
	unsigned int v10;
	unsigned int v11;

	v4 = Size;
	v5 = a1;
	v6 = 0;
	if( v4 > 1 )
	{
		v8 = v4;
		do
		{
			v8 -= 2;
			v5 += *(unsigned short *)(allData + startAddr);
			v9 = (unsigned long long)v5 << 16;
			startAddr += 2;
			if( !(unsigned short)v8 )
			{
				v5 = ((int)(((v9)>>32)&0xffffffff)) + ((unsigned int)v9 >> 16);
			}
		}while(v8 > 1);
		v4 = v8;
	}

	v11 = ((( (v3 >> 16) | ((((((unsigned long long)v5 >> 16) + (unsigned short)v5) >> 16) + ((((unsigned long long)v5 >> 16) + (unsigned short)v5) & 0xffff)) << 16) ) << 16 ) | (((v3 >> 16) | ((((((unsigned long long)v5 >> 16) + (unsigned short)v5) >> 16)+ ((((unsigned long long)v5 >> 16) + (unsigned short)v5) & 0xffff)) << 16)) >> (32-16) ));

	v10 = v11;

	printf("%x\n",(unsigned short)v10);
	return (unsigned short)v10;
}

int main(int argc, char *argv[])
{
	int v3, v4, v7, v8, v9, v10, v12, v14, v15, v16, v17, v18, v19, v20, v21;
	unsigned int v13;
	char v11;
	signed int v5;	
	char path[50];

	if( argc < 2 )
	{
		printf("Usage: ultra_rev [path]\n");
		exit(0);
	}

	strncpy(path,argv[1],30);
	strcat(path+strlen(path),"/execute_me_enc");
	printf("path : %s\n",path);
	FILE *fp = fopen( path, "r" );

	char *allData;
    int cnt = 0;
    int arraySize;

    if(fp == NULL)
    {
            printf("*** File open error ***\n");
            exit(1);
    }

    allData = (char*)malloc(1);

    while(!feof(fp))
    {
            allData = (char*)realloc(allData, cnt+1);
            fscanf(fp, "%c", &allData[cnt]);
            cnt++;
    }
    arraySize = cnt;


	v3 = 0x60271070;
	v4 = 0;
	v5 = arraySize;

	v7 = v4;
	v8 = v5;
	v9 = v5 - 3;
	v10 = v4 + 1;
	
	if( *(char *)(allData + v4) == 0x62)
	{
		if( *(allData + v4) + *(allData + 1) == 210 )
		{

			if( check(0, v7, v8, allData) == 0xdead )
			{
				printf("Correct File!\n\n");
				dec(argv[1],allData);
				return 0;
			}
		}
	}	
	printf("Not Correct File\n");
	return 0;
}
