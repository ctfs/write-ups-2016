#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void give_shell()
{
	gid_t gid = getegid();
	setresgid(gid, gid, gid);
	system("/bin/sh -i");
}

void vuln(char *input)
{
	char buf[16];
	int secret = 0;
	strcpy(buf, input);

	if (secret == 0xDEADBEEF)
	{
		give_shell();
	}
	else
	{
		printf("Sorry, secret = 0x%08X\n", secret);
	}
}

int main(int argc, char **argv)
{
	if (argc != 2)
	{
		printf("Usage: overflow1 [str]\n");
		return 1;
	}

	vuln(argv[1]);

	return 0;
}
