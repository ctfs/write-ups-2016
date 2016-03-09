# Cyber Security Challenge 2016: Phishing is not a crime

**Category:** Mobile Security  
**Points:** 100  
**Challenge designer:** Jeroen Beckers
**Description:**
> Can you get into Dexter's laboratory?

[Application file](challenge-source-files/dexter.apk)

## Write-up
When launching the application, you see a countdown going from 60 to 0, an input field and a submit button. Let's see what this application does:

Unzip the APK, Dex2jar the embedded “classes.dex” file and decompile the resulting JAR back to java code:
```
$ unzip dexter.apk
  Archive:  dexter.apk
    inflating: AndroidManifest.xml     
    extracting: assets/app.apk          
    inflating: assets/classes.dex      
    inflating: assets/classes_original.dex  
    (…)
$ ./d2j-dex2jar.sh classes.dex
    dex2jar classes.dex -> ./classes-dex2jar.jar
```
We can then decompile and view the .jar using JD-GUI. The application flow of the MainActivity class can be described as follows:
1. It downloads an APK file from `/chall.php` and saves it as tf2.apk
2. It extracts the tf2.apk file and loads the contained classes.dex file
3. When submitting a code, the application first verifies the code using the `open()` method loaded from the external classes.dex file
4. If the code is correct, it submits this code to the webserver by calling `sol.php?key=" + paramString1 + "&id=" + paramString2`
5. When 60 seconds are over, a new APK is requested from the server.

Two things still need to be figured out: What is the `id` parameter, and how does the `open()` method work. The id parameter can be found by looking at the FileDownloader class:
```java
public static void downloadFile(String paramString, File paramFile)
  {
    int i;
    for (;;)
    {
      try
      {
        Object localObject = (HttpURLConnection)new URL(paramString).openConnection();
        ((HttpURLConnection)localObject).connect();
        paramString = ((HttpURLConnection)localObject).getInputStream();
        paramFile = new FileOutputStream(paramFile);
        ((HttpURLConnection)localObject).getContentLength();
        String str = ((HttpURLConnection)localObject).getHeaderField("Content-Disposition");
        if ((str != null) && (str.indexOf("=") != -1))
        {
          id = str.split("=")[1];
          id = id.split("\\.")[0];
          id = id.split("\"")[1];
          time = Date.parse(((HttpURLConnection)localObject).getHeaderField("Date")) / 1000L;
          localObject = new byte[1048576];
          i = paramString.read((byte[])localObject);
          if (i <= 0) {
            break;
          }
          paramFile.write((byte[])localObject, 0, i);
          continue;
        }
        Log.d("dexter", "ID IS NULLL");
      }
      catch (Exception paramString)
      {
        failed = true;
        return;
      }
    }
    Log.d("dexter", "Written file! bytes = " + i);
    paramFile.close();
  }
  ```
We can see that the ID is actually the filename of the downloaded APK file, without the .apk extension. The next step is to get a hold of a loaded APK file, which can easily be done by surfing to /chall.php and saving the generated file. Using the same decompilation steps as before, we can see the following code:

```java
public static boolean open(String paramString)
  {
    if (paramString.length() != 10) {}
    for (;;)
    {
      return false;
      if ((paramString.substring(0, 2).equals("2b")) && (paramString.charAt(2) == '8') && (new StringBuilder(paramString).reverse().toString().substring(4, 7).equals("72f"))) {}
      try
      {
        MessageDigest localMessageDigest = MessageDigest.getInstance("SHA1");
        localMessageDigest.reset();
        localMessageDigest.update(paramString.getBytes(Charset.forName("UTF8")));
        boolean bool = "50566615ff8e8e8eec6e8d60539dd4eb6f44a1ad".equals(new BigInteger(1, localMessageDigest.digest()).toString(16));
        if (!bool) {}
      }
      catch (NoSuchAlgorithmException paramString)
      {
        for (;;)
        {
          paramString.printStackTrace();
        }
      }
    }
    return true;
  }
  ```
There are two parts to this small method. First, some static checks are occuring. In the example above, the following conditions have to be met:
1. The key length is 10
2. The first two characters needs to be "2b"
3. The third character needs to be "8"
4. Characters 4 to 6 need to be f27

Next, the SHA1 hash of the key has to equal a given string, in this case `50566615ff8e8e8eec6e8d60539dd4eb6f44a1ad`. As there is no more information available, we will need to brute-force this. If we download a few more generated APK files, we'll see that the characters change in every APK, but also that sometimes MD5 is used instead of SHA1. All of the characters do fall in the hex range, so it would be a good guess to only bruteforce the four remaining characters in the [0-9A-F] range. 

The following python script solves the challenge by extracting all the conditions and bruteforcing the hash:

```python
import subprocess, os, re, hashlib, time
import urllib2
import shlex
from subprocess import Popen, PIPE

def get_exitcode_stdout_stderr(cmd):
    """
    Execute the external command and get its exitcode, stdout and stderr.
    """
    args = shlex.split(cmd)

    proc = Popen(args, stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()
    exitcode = proc.returncode
    #
    return exitcode, out, err

def getFlag(key, id):
  url = 'http://dexter.challenges.cybersecuritychallenge.be/sol.php?key=%s&id=%s' % (key, id)
  response = urllib2.urlopen(url)
  print response.read()

def getValue(str, text):

  regex = re.search(str, text, re.IGNORECASE)

  if regex:
    return regex.group(1)

  print "ERROR: %s not found!" % str

  return ""

def solve():
  FNULL = open(os.devnull, 'w')

  exitcode, str, err = get_exitcode_stdout_stderr(" ".join(["rm", "-rf", "./unpacked"]))

  exitcode, str, err = get_exitcode_stdout_stderr('wget --server-response -q -O vault.apk "http://dexter.challenges.cybersecuritychallenge.be/chall.php"')
  filename = getValue('"(\w*).apk', err);
  exitcode, str, err = get_exitcode_stdout_stderr(" ".join(["apktool", "d", "-f", "./vault.apk", "-o", "./unpacked"]))

  cmd = "grep const ./unpacked/smali/be/nviso/vault/Vault.smali"
  exitcode, str, err = get_exitcode_stdout_stderr(cmd)

  #fdff675780 fd 102 76f 67 SHA1 3093eb9177eacd03224c036cc7396ddeb095a9b2 6b63f8ad18c31f5b7344a5450c94a3f4 1453878508 56a86cec

  
  ALGO = getValue('const-string v3, "([^"]*)"', str)
  part1 = getValue('const-string v0, "([^"]*)"', str)

  part2 = getValue('const/16 v1, (.*)', str)
  part2 = int(part2, 16)

  part3 = getValue('const-string v2, "([^"]*)"', str)

  HASH = getValue('const-string v5, "([^"]*)"', str)

  partialSolution = part1 + chr(part2) + part3[::-1]


  hexchars = "abcdef0123456789"

  for a in hexchars:
    for b in hexchars:
      for c in hexchars:
        for d in hexchars:

          potentialSolution = partialSolution + a + b + c + d

          m = hashlib.new(ALGO)
          m.update(potentialSolution)
          h = "%s" % m.hexdigest()
          
          if h == HASH:
            return potentialSolution, filename, ALGO

  print "NO JOY"

sol, filename, algo = solve()
getFlag(sol, filename)

```



## Solution
DeeDeeGetOutOfMyL4Borat0ry!

## Other write-ups and resources
- None yet.
