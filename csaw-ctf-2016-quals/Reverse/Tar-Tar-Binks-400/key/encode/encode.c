/* Encode strings as base 40 triplets.
   Al Williams DDJ
*/
 
#include <stdio.h>
#include <string.h>
 
// The character table is a 2x38 array. The 2 arrays are for
// the shift state and by convention 0 is always 0
// code 39 (not in the array which tops out at index 38)
// causes the shift to be set for the next character

char ctable[2][39]=
  {
    {
      '\0','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9',' ','\n'
    },
    {
      '\0','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','(','!','@','#',',','.','?','/','*',')','<','>'       
    }
  };
 


unsigned int encoded[10000];
unsigned int posi;

 
#define ZEROCHAR '~'  // use this to represent zero in input
// what to use for unknown symbols -- note must not be shifted!
#define UNKNOWN_SYM 37  // space in the default encoding
 

int decode(int in,char *out, int start)
{
  static int shiftstate=0;
  int count=3;  // assume we will emit 3 characters
    
  unsigned int tmp;
  // get first character
  tmp=in/1600;
  if (tmp==39)  // test for shift
    {
    shiftstate=1;
    count--;  // won't count as output
    }
  else
    {
      // real character, so look it up and reset shift
      // which may not have been set anyway
     out[start++]=ctable[shiftstate][tmp];
     shiftstate=0;
    }
  // get 2nd character and repeat logic
  // keep in mind that X*1600 => X*1024+X*512+X*64
  // so this could be optimized if necessary
  tmp=(in-tmp*1600)/40;
  if (tmp==39)
    {
      shiftstate=1;
      count--;
    }
  else
    {
    out[start++]=ctable[shiftstate][tmp];
    shiftstate=0;
    }
  // get 3rd character.. if you don't have a mod
  // function you could say tmp=(in-tmp*40)
  // don't forget that x*40 = x*32+x*8 so you could
  // make * 40 very efficient if you needed to optimize
  tmp=in%40;
  if (tmp==39)
    {
      shiftstate=1;
      count--;
    }
  else
    {
      out[start++]=ctable[shiftstate][tmp];
      shiftstate=0;
    }
  return count;   // return count
}

int pending=0;  // encode needs to send more than one symbol
  
 
// return a symbol (or symbols, see pending) for a given character
int encode(int c)
{
  int i;
  static int shifted=-1;
// if we are mid shift, just send the pending symbol
  if (shifted!=-1)  
    {
      i=shifted;
      shifted=-1;
      pending=0;
      return i;
    }
  // make it easy for the user to enter a zero
  if (c==ZEROCHAR) c='\0';
  // simple search for the symbol -- run time
  // performance isn't a big deal here because
  // we will just run this on the PC at design time
  for (i=0;i<39;i++)
    {
      if (ctable[0][i]==c)
    {
      pending=0;  
      return i;  // b40 symbol
    }
      if (ctable[1][i]==c)
    {
      pending=1;
      shifted=i;
      return 39;    // shift code
    }
    }
  // use 0 for any unmatched character
  // you might prefer using your symbol for '.' or '?'
  // and you can set that in the #define
  fprintf(stderr,"Warning character %c (%x) unmatched\n",c,c);
  pending=0;
  return UNKNOWN_SYM;  // unmatched character
}
 
// Emit a 16 bit quantity
// in the d array (d[2] is first digit, d[0] is last digit)
void emit(int *d)
{
  unsigned int v;
  v=d[2]*1600+d[1]*40+d[0];
  encoded[posi++] = v;
  printf("%04X,",v);
}
   

void drive_encode(char* str, int len){
    int d[3];  // current B40 "digits"
  int cp=3;  // pointer in d array
  int c;     // current character

  while (len--)
      {
        c = *str++;
        int cval;
        pending=1;   // make sure we call encode once
        while (pending)  // while encode has something to say
      {
        int cenc;
        cenc=encode(c);  // could be index (0-37) or shiftcode
        d[--cp]=cenc;
        // every 3 characters we have to emit something
        if (cp==0)
          {
            emit(d);
            cp=3;  // reset d array
          }
      }
         
      }
     
    // flush any left overs
     if (cp!=3)
      {
      while (cp!=-1) d[--cp]=0;
      emit(d);  // write that last word
      }
}

 
 
int main(int argc, char *argv[])
{
  int d[3];  // current B40 "digits"
  int cp=3;  // pointer in d array
  int c;     // current character

  char* test = "Milos Raonic (born 1990) is a Canadian professional tennis player. He reached a career high world No. 4 singles ranking in May 2015, as ranked by the Association of Tennis Professionals (ATP). His career highlights include a Grand Slam final at the 2016 Wimbledon Championships and two Grand Slam semifinals at the 2014 Wimbledon Championships and 2016 Australian Open. He was the 2011 ATP Newcomer of the Year, and has been ranked continuously inside the top 20 since August 2012. Raonic is the first player born in the 1990s to win an ATP title, to be ranked in the top 10, and to qualify for the ATP World Tour Finals. He has eight ATP singles titles, all won on hard courts. He is frequently described as having one of the best serves among his contemporaries. Statistically, he is among the strongest servers in the Open Era, winning 91p of service games to rank third all time. Aided by his serve, he plays an all court style with an emphasis on short points.";
  int len = strlen(test)+1;
 
  drive_encode(test, len);

  printf("\n");
  int i;
  char buf[4];
  for(i =0; i < posi; ++i){
     // printf("%04X,",encoded[i]);

  // grab a triplet
  // while (scanf("%x,",&v)>0) 
  //   {
  //     // decode it
      c=decode(encoded[i],buf,0);
      buf[c]='\0';
      // for us printing it is fine
      printf("%s",buf);

  }
  // done!  
  return 0;
   
}