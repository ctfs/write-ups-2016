/* Decode strings from base 40 triplets.
   Al Williams DDJ
*/
 
#define TESTMAIN 1   // build test harness?
 
 
#include <stdio.h>
 
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
  
// Decode a triplet into out[start] and beyond
// since shift characters don't create characters you could have
// from 1 to 3 characters in out (since [shift]X[shift] is legal)
// so the return value is how many characters were set
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
 
int main(int argc, char *argv[])
{
  int v,c;
  char buf[4];
  char* y = "F5D1,4D6B,ED6A,08A6,38DD,F7FA,609E,EBC4,E55F,E6D1,7C89,ED5B,0871,1A69,5D58,72DE,224B,3AA6,0845,7DD6,58FB,E9CC,0A2D,76B8,ED60,251A,1F6B,32CC,E78D,12FA,201A,E889,2D25,922A,4BC5,F5FF,F8E5,C79B,3A77,4BDB,EA11,5941,58BD,3A95,F5C9,A225,AD40,F8BD,095D,70B6,458C,E7A9,EA68,252F,094B,5E41,0969,6015,5ED5,F6E5,59B9,7CAF,66DF,265B,7837,57B4,7CAF,AED9,F707,6A3C,F8E5,F509,7C8B,0915,2235,336F,33E9,2D14,7C91,5804,83E5,E78D,F4EA,0874,ED6B,4B35,E839,57B4,E77C,EA68,2525,AD41,ED6F,3A4A,4BCC,6015,F440,0858,3AA6,7809,671D,0874,EA77,63AF,2E91,5845,F6C4,086D,7795,3939,57B4,7C89,82DC,32ED,B994,C7AF,9135,0E65,1B66,ED5B,3235,6577,5A80,3AD3,E776,1EE5,AD41,ED59,864C,70B4,3876,ED67,64D6,F8E5,F505,EAD9,7C9C,32ED,B994,B4EF,0C6C,F665,F5F5,9047,521A,E99E,EA68,252F,9D09,76B7,E776,1ED0,095D,0D4D,5D5A,087B,2005,1526,7E76,85AD,78B9,E8B6,782C,251C,32ED,7F68,EBE3,EA41,57FD,ED59,846D,7A05,B994,BB78,ED6A,08A6,38DD,3B5D,7E45,E839,738C,E9CC,0A2D,764A,609E,E8B6,EA68,2524,E6BB,7C9C,639F,3A95,0895,F40F,8328,EA69,7EE5,F8BD,7F7D,0D6D,70B6,458C,E8B6,EA68,251C,6065,B35F,C789,5845,7F7D,6D89,4C6E,A20E,60B5,7E45,ED59,F707,69EF,922A,4BC5,F6EF,8635,F4B9,57B4,7CF8,ED60,2510,095D,20AF,3545,F40F,8328,EA41,58A4,225D,7E7C,4BDB,F8BD,082C,EAE7,5D57,5D50,0914,E7C7,8624,7CF8,ED60,2511,7C8E,7159,8416,7EF9,E7E5,774A,3895,1EC9,7C90,09B9,58BD,5FF5,E99E,EA68,250A,224C,EA3D,73F5,7C89,53A6,3190,3B5D,1526,7DD5,666A,0919,225F,CDEF,79E1,7E7B,7E6B,082C,A277,E885,E8BB,E775,5FF7,EA68,251B,7FDF,589D,7A05,779A,8A5A,7C91,5D5C,32ED,F628,2195,F49A,0C77,EAE1,59B9,58BD,E570,E99E,EA3D,73F9,13AD,2BF5,225D,7F7D,70B6,4A9C,337A,1EC9,4D05,7E75,2578,ED59,38E5,1ECA,A210,3B5D,779A,8A6F,C790,2518,4B41,7C89,5D49,4D05,152D,73C5,79F9,4BED,913C,37C9,5D4D,53C8,0941,7C97,5D5B,346A,82D8,5F36,801F,C800,";
  char* g = strdup(y);
  char* b, q, end;
  end = g+strlen(y);

  long ret;
  int i = 500;
  // grab a triplet
  while (i--) 
    {
      b = strdup(g);
      b[4] = 0;
      // printf("%s\n", b);
      ret = strtol(b,q,16);
      // decode it
      c=decode(ret,buf,0);
      buf[c]='\0';
      // for us printing it is fine
      printf("%s",buf);
      g += 5;
      if(g > end){
        break;
      }
    }
  printf("\n");
}