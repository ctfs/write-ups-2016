# EKOPARTY CTF 2016 : jvm-25

**Category:** Reversing
**Points:** 25
**Solves:** 515
**Description:**

> Bytecodes everywhere, reverse them.
> [Attachment](rev25.zip)

## Write-up

First begin by searching for the term `JVM`, which should be listed as `Java Virtual Machine` (basically allows Java to run on nearly any device). Downloading the `.zip` file and extracting the contents should reveal a `.class` file. If you have ever worked with Java programming (or Google `Java bytecodes`) you should see the Java program files compile into `.class` files. I Googled `Java class file to java file` where I found [this website](http://www.javadecompilers.com/) which, when I uploaded the `.class` file, provided me with the following Java code:

```Java
public class EKO {
    public static void main(String[] arrstring) {
        int n = 0;
        for (int i = 0; i < 1337; ++i) {
            n += i;
        }
        String string = "EKO{" + n + "}";
    }
}
```

You can run this code using Java, or by reading it, you can see the flag is simply all the numbers below `1337` added together. I wrote this quick Python script to get the output:

```Python
n = 0
for i in range(0, 1337):
  n += i
print("EKO{" + str(n) + "}")
```

`>>> EKO{893116}`

## Other write-ups and resources

* https://youtu.be/mjF3UY8VzVU
* https://github.com/Idomin/CTF-Writeups/tree/master/EKOCTF-2016
* [Tech Hacks](https://nacayoshi00.wordpress.com/2016/10/28/ekoparty-ctf-2016-writeup/)
* https://github.com/burlingpwn/writeups/tree/master/EKOPARTY-CTF-2016/Reversing/JVM
* https://specterdev.blogspot.com/2016/10/write-up-ekoparty-2016-ctf-reverse.html
