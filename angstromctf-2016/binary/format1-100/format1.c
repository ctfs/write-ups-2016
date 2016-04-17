#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int secret = 0;

void give_shell()
{
	gid_t gid = getegid();
	setresgid(gid, gid, gid);
	system("/bin/sh -i");
}

int main(int argc, char **argv)
{
	char buf[128];
	memset(buf, 0, sizeof(buf));
	fgets(buf, 128, stdin);
	printf(buf);

	if (secret == 192)
	{
		give_shell();
	}
	else
	{
		printf("Sorry, secret = %d\n", secret);
	}

	return 0;
}
