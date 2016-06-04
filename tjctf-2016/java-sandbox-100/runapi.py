#!/usr/bin/env python3
from threading import Timer
import os
import sys
import os.path
import tempfile
import subprocess
import time
import shutil
import traceback
import re

TIMEOUT = 2

def esc(s):
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")

def getJavaFileName(code):
    a = re.search(r"\s*(public|private)\s+class\s+(\w+)\s+((extends\s+\w+)|(implements\s+\w+( ,\w+)*))?\s*\{", code)
    if a:
        return a.group(2)
    return False

def runcode(code):
    try:
        tmpdir = tempfile.mkdtemp()
        tmpclass = getJavaFileName(code)
        if not tmpclass:
            print('<span style="color:red">Could not find class name in Java file! Do you have a public class in your code?</span>')
            return
        if tmpclass == "CustomSecurityManager" or "java" in tmpclass:
            print('<span style="color:red">Invalid class name!</span>')
        if len(code) > 10000:
            print('<span style="color:red">You have too much code! Please limit your code to be less than 10,000 characters.</span>')
            return
        filename = tmpdir + '/' + tmpclass + '.java'
        f = open(filename, 'w')
        f.write(code)
        f.close()
        jenv = os.environ.copy()
        appfolder = os.path.dirname(os.path.realpath(__file__))
        jars = []
        for jar in os.listdir(appfolder + "/web/libs"):
            if os.path.isfile(appfolder + "/web/libs/" + jar):
                jars.append(appfolder + "/web/libs/" + jar)
        shutil.copy(appfolder + "/Wrapper.java", tmpdir + "/Wrapper.java")
        p = subprocess.Popen(["javac", "-cp", ".:" + ":".join(jars), "Wrapper.java", filename], cwd=tmpdir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=jenv)
        outdata, errdata = p.communicate()
        if p.returncode != 0:
            print("<span style='color:red'>Error when compiling!</span>")
            if outdata:
                print(esc(outdata.decode('utf-8')))
            if errdata:
                print("<span style='color:red'>" + esc(errdata.decode('utf-8')) + "</span>")
            shutil.rmtree(tmpdir)
            return
        if not os.path.isfile(tmpdir + "/" + tmpclass + ".class"):
            print("<span style='color:red'>No class file generated from compile step!</span>")
            shutil.rmtree(tmpdir)
            return
        p = subprocess.Popen(["java", "-Xmx128m", "-cp", ".:" + ":".join(jars), "Wrapper", tmpclass, ":".join([tmpdir, appfolder + "/web/libs/"])], cwd=tmpdir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=jenv)
        timer = Timer(TIMEOUT, p.kill)
        timer.start()
        outdata, errdata = p.communicate()
        if timer.is_alive():
            timer.cancel()
        shutil.rmtree(tmpdir)
        print("<span style='color:green'>Program ran successfully!</span>")
        if outdata:
            print(esc(outdata.decode('utf-8')))
        if errdata:
            print("<span style='color:red'>" + esc(errdata.decode('utf-8')) + "</span>")
    except Exception as e:
        print('<span style="color:red">Unknown error when running code!</span>\n', esc(str(e)))

if __name__ == "__main__":
    if (len(sys.argv) < 2):
        print("Usage:", sys.argv[0], "<code>")
    runcode(sys.argv[1])
    exit()

