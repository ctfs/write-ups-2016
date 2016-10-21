# tjctf-2016 : financial-transaction-60

**Category:** Cryptography
**Points:** 60
**Description:** The History Museum sent us some money and encrypted the transfer using an Enigma Machine. Unfortunately, we were unable to decrypt the cipher and retrieve the money. Can you help us out? This is all we have.

## Write-up

Based on the architecture of the enigma, and the amount of information given to us about the configuration, it's best to just try a brute force decryption. Here's a modified simulation script used to brute force it:

```C
#include <stdio.h>
#define MSGLEN 80
#define TO 'A'
/* Rotor wirings */
char rotor[5][26]={
    /* Input "ABCDEFGHIJKLMNOPQRSTUVWXYZ" */
    /* 1: */ "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
    /* 2: */ "AJDKSIRUXBLHWTMCQGZNPYFVOE",
    /* 3: */ "BDFHJLCPRTXVZNYEIWGAKMUSQO",
    /* 4: */ "ESOVPZJAYQUIRHXLNFTGKDCMWB",
    /* 5: */ "VZBRGITYUPSDNHLXAWMJQOFECK" };
char ref[26]="YRUHQSLDPXNGOKMIEBFZCWVJAT";
char notch[5]="QEVJZ";
/* Encryption parameters follow */
typedef struct P
{
  char order[3];/*={ 1, 2, 3 };*/
  char rings[3];/*={ 'A','A','A' };*/
  char pos[3];/*={ 'A','A','A' };*/
  char plug[10];/*="AMTE";*/
} Params;
/*take a char and return its encoded version according to the
  encryption params, update params, i.e. advance wheels
  this part uses Fauzan Mirza's code*/
char scramble(char c, Params *p)
{
  int i, j, flag = 0;
        c=toupper(c);
        if (!isalpha(c))
            return -1;
        /* Step up first rotor */
        p->pos[0]++;
        if (p->pos[0]>'Z')
            p->pos[0] -= 26;
        /* Check if second rotor reached notch last time */
        if (flag)
        {
            /* Step up both second and third rotors */
            p->pos[1]++;
            if (p->pos[1]>'Z')
                p->pos[1] -= 26;
            p->pos[2]++;
            if (p->pos[2]>'Z')
                p->pos[2] -= 26;
            flag=0;
        }
        /*  Step up second rotor if first rotor reached notch */
        if (p->pos[0]==notch[p->order[0]-1])
        {
            p->pos[1]++;
            if (p->pos[1]>'Z')
                p->pos[1] -= 26;
            /* Set flag if second rotor reached notch */
            if (p->pos[1]==notch[p->order[1]-1])
                flag=1;
        }
        /*  Swap pairs of letters on the plugboard */
        for (i=0; p->plug[i]; i+=2)
        {
            if (c==p->plug[i])
                c=p->plug[i+1];
            else if (c==p->plug[i+1])
                c=p->plug[i];
        }
        /*  Rotors (forward) */
        for (i=0; i<3; i++)
        {
            c += p->pos[i]-'A';
            if (c>'Z')
                c -= 26;
            c -= p->rings[i]-'A';
            if (c<'A')
                c += 26;
            c=rotor[p->order[i]-1][c-'A'];
            c += p->rings[i]-'A';
            if (c>'Z')
                c -= 26;
            c -= p->pos[i]-'A';
            if (c<'A')
                c += 26;
        }
        /*  Reflecting rotor */
        c=ref[c-'A'];
        /*  Rotors (reverse) */
        for (i=3; i; i--)
        {
            c += p->pos[i-1]-'A';
            if (c>'Z')
                c -= 26;
            c -= p->rings[i-1]-'A';
            if (c<'A')
                c += 26;
            for (j=0; j<26; j++)
                if (rotor[p->order[i-1]-1][j]==c)
                    break;
            c=j+'A';
            c += p->rings[i-1]-'A';
            if (c>'Z')
                c -= 26;
            c -= p->pos[i-1]-'A';
            if (c<'A')
                c += 26;
        }
        /*  Plugboard */
        for (i=0; p->plug[i]; i+=2)
        {
            if (c==p->plug[i])
                c=p->plug[i+1];
            else if (c==p->plug[i+1])
                c=p->plug[i];
        }
  return c;
}
/*take a string, return encoded string*/
char *enigma(char *in, Params *p)
{
  int j;
  char out[MSGLEN];
  for(j = 0; j < strlen(in); j++)
  out[j] = scramble(in[j], p);
  out[j] = '\0';
  return out;
}
/*read in a string, and pass it through enigma*/
void cypher(Params p)
{
  char in[MSGLEN], s[MSGLEN];
  int c, i = 0;

  while((c = getchar()) != '\n')
  {
    in[i] = toupper(c);
    i++;
  }
  in[i] = '\0';
  strcpy(s, enigma(in, &p));
  printf("\n%s\n%s\n", s, in);
}
/*given a cipher text, and a crib, test all possible settings of wheel order a, b, c*/
void rotate(int a, int b, int c, char *cyph, char *crib, char *plug, int *ct)
{
  Params p;
  p.order[0] = a;
  p.order[1] = b;
  p.order[2] = c;
  p.rings[0] = p.rings[1] = p.rings[2] = 'A';
  strcpy(p.plug, plug);
  for(p.pos[0] = 'A'; p.pos[0] <= 'Z'; p.pos[0]++)
  {
    for(p.pos[1] = 'A'; p.pos[1] <= 'Z'; p.pos[1]++)
    {
      for(p.pos[2] = 'A'; p.pos[2] <= 'Z'; p.pos[2]++)
      {
/*        for(p.rings[0] = 'A'; p.rings[0] <= 'Z'; p.rings[0]++)
        {
          for(p.rings[1] = 'A'; p.rings[1] <= 'Z'; p.rings[1]++)
          {
            for(p.rings[2] = 'A'; p.rings[2] <= 'Z'; p.rings[2]++)
            {
*/          // if (p.pos[0] != 'c' || p.pos[1] != 't' ||  p.pos[2] != 'f')
//               continue;
//
          Params cp = p;
          int i = 0;

          while(strlen(crib) > i)
          {
        if(cyph[i] != scramble(crib[i], &cp))
        break;
        else
        i++;
          }
          if(strlen(crib) == i)
          {
        char s[MSGLEN];

        (*ct)++;
            printf("Wheels %d %d %d Start %c %c %c Rings %c %c %c Stecker \"%s\"\n",
                        p.order[0], p.order[1], p.order[2],
                        p.pos[0], p.pos[1], p.pos[2],
                        p.rings[0], p.rings[1], p.rings[2], p.plug);
        cp = p;
        strcpy(s, enigma(cyph, &cp));
                printf("%s decoded -> %s\n", cyph, s);
              }
/*            }
          }
        }
*/      }
    }
  }
}
/*do the whole check including steckering of up to two pairs of letters*/
void test(int a, int b, int c, char *cyph, char *crib, int *ct)
{
  char A, B, C, D;
  int i = 0, cs;
  char s[5];

  strcpy(s, "");
  printf("Checking wheels %d %d %d\n",  a, b, c);
  for(cs = 0; cs < 3; cs++)
  {
    if(cs > 0)
    {
      for(A = 'A'; A <= TO; A++)
      {
        for(B = A + 1; B <= TO; B++)
        {
      s[0] = A;
      s[1] = B;
      s[2] = '\0';
      if(cs > 1)
      {
        for(C = A + 1; C <= TO; C++)
        {
          if(C == B)
          continue;
          for(D = C + 1; D <= TO; D++)
              {
            if(D == A || D == B)
        continue;
        i++;
        s[2] = C;
        s[3] = D;
        s[4] = '\0';
                rotate(a, b, c, cyph, crib, s, ct);
          }
            }
          }
      else
      rotate(a, b, c, cyph, crib, s, ct);
        }
      }
    }
    else
    rotate(a, b, c, cyph, crib, s, ct);
  }
}
/*run on all permutations of wheels a, b, c*/
void permute(int a, int b, int c, char *cyph, char *crib, int *ct)
{
  test(a, b, c, cyph, crib, ct);
  test(a, c, b, cyph, crib, ct);
  test(b, a, c, cyph, crib, ct);
  test(b, c, a, cyph, crib, ct);
  test(c, a, b, cyph, crib, ct);
  test(c, b, a, cyph, crib, ct);
}
/*all triples of five possible wheels*/
void permuteAll(char *cyph, char *crib)
{
  int ct = 0;
  permute(1, 2, 3, cyph, crib, &ct);
  permute(1, 2, 4, cyph, crib, &ct);
  permute(1, 2, 5, cyph, crib, &ct);
  permute(1, 3, 4, cyph, crib, &ct);
  permute(1, 3, 5, cyph, crib, &ct);
  permute(1, 4, 5, cyph, crib, &ct);
  permute(2, 3, 4, cyph, crib, &ct);
  permute(2, 3, 5, cyph, crib, &ct);
  permute(2, 4, 5, cyph, crib, &ct);
  permute(3, 4, 5, cyph, crib, &ct);
  printf("\nFound %d solutions.\n", ct);
}
/*helper to read a character*/
char readCh()
{
  char c, ret;

  while((c = getchar()) != '\n')
  ret = c;
  return ret;
}
/*init the starting position*/
void initParams(Params *p)
{
  int i;
  char c;

  printf("d)efault or u)ser: ");
  c = readCh();
  if(c != 'u')
  {
    for(i = 0; i < 3; i++)
    {
      p->order[i] = i + 1;
      p->rings[i] = 'A';
      p->pos[i] = 'A';
    }
    strcpy(p->plug, "");
  }
  else
  {
      for(i = 0; i < 3; i++)
      {
        printf("Wheel %d: ", i + 1);
        p->order[i] = readCh() - 48;
      }
      for(i = 0; i < 3; i++)
      {
/*        printf("Ring  %d: ", i + 1);*/
        p->rings[i] = 'A';/*readCh();*/
      }
      for(i = 0; i < 3; i++)
      {
        printf("Start %d: ", i + 1);
        p->pos[i] = readCh();
      }
      printf("Stecker: ");
      i = 0;
      while((c = getchar()) != '\n')
      {
        p->plug[i] = c;
    i++;
      }
      p->plug[i] = '\0';
  }
  printf("Wheels %d %d %d Start %c %c %c Rings %c %c %c Stecker \"%s\"\n",
         p->order[0], p->order[1], p->order[2],
         p->pos[0], p->pos[1], p->pos[2],
         p->rings[0], p->rings[1], p->rings[2], p->plug);
}
/********************************************MAIN*********************************************/
void main(int argc, char *argv[])
{
  Params p;

  if(argc > 2)  /*bombe case*/
  {
    permuteAll(argv[1], argv[2]);
  }
  else
  {
    initParams(&p);
    cypher(p);
  }
}
```
Running the above code piped to grep, we can search for keywords like `MONEY`.
It should eventually come up with: `ZAJXVLXIGOURMONEYXHERNCXOCQAPLYSMJRTROUBLEXMONEOFQSEKVXMMXADING` and a nearby line `H S Z` config, gave us `ORGETTINGTEMXHQSJSOFAESAFLAGFORYOURDJVSCMUWPEEJYISNOTEVERYTHIDL0`. Combine the words from both and you will get `MONEYISNOTEVERYTHING`

## Other write-ups and resources

* [My Computer is a Potato - gitbooks.io](https://bobacadodl.gitbooks.io/tjctf-2016-writeups/content/financial_transaction_50_pts.html)
