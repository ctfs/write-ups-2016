# Break In 2016 - Crypto-Numbero

**Category:** crypto
**Points:** 100
**Solves:** 7
**Description:**

> 249929761157732020161556121009125440871694502549075144988219699324612968709313502340276966732128645621282888705508840858566948023130606222964801977446316823159281256329353559220858509063084671505269932006162189731434947807072043095879259154468002856960

# Write-up

In this question the number given was a double type. So all one had to do 
was to understand this part and after that it was just scanning and printing 
the number. 

Starting approach could be to read the number and then convert it to string 
byte by byte but that would lead to some garbage chars at the end and that's 
when one has to figure out that the number is larger than an integer. So now 
try out some other data types of larger size than int.

Here's the code for how this number was created:

249929761157732020161556121009125440871694502549075144988219699324612968709313502340276966732128645621282888705508840858566948023130606222964801977446316823159281256329353559220858509063084671505269932006162189731434947807072043095879259154468002856960

    /********** strtodouble.c ********************/
    #include<stdio.h>    
    int main() {
        double d[8];
        scanf("%s", d); 
        printf("%lf\n", d[0]);
        return 0;
    }

After the string was converted to double, the decimal part was removed to 
increase the difficulty by broadning the field in which number could 
lie. Also removing the decimal part had no effect on the string.


And here's the code to read the number and then print it in string:

    /********** doubletostr.c ********************/
    #include<stdio.h>    
    int main() {
        double x;
        scanf("%lf", &x);
        puts(&x);
        printf("\n%s\n",&x);
        return 0;
    }

On running the number via this you get

    y0ug0t!t

Which is the flag.

# Other write-ups and resources 

* None

