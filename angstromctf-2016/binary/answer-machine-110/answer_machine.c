#include <stdio.h>
#include <stdlib.h>

void print_date()
{
	printf("Welcome, today is ");
	fflush(stdout);
	system("/bin/date");
}

int get_message()
{
	char buf[64];

	printf("I can't talk now, so leave a message: ");
	fflush(stdout);
	fgets(buf, 192, stdin);
	
	FILE *fp = fopen("message.txt","a");
	if (!fp)
	{
		printf("Error opening file; message moved to trash\n");
		return 1;
	}
	fwrite(buf, 64, 1, fp);
	fclose(fp);

	return 0;
}

int main(int argc, char **argv)
{
	print_date();
	return get_message();
}
