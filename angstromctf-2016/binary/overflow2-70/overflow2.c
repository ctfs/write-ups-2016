#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* I should probably get rid of this... */
void give_shell()
{
	gid_t gid = getegid();
	setresgid(gid, gid, gid);
	system("/bin/sh -i");
}

void vuln(char *input)
{
	char buf[16];
	strcpy(buf, input);
}

int main(int argc, char **argv)
{
	if (argc != 2)
	{
		printf("Usage: overflow2 [str]\n");
		return 1;
	}

	vuln(argv[1]);

	return 0;
}
