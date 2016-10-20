#Solution 

key = "themidathemidathemida"
brainf = ">----++++....<<<<."

initial_key =""
for i in range(18):
	initial_key += chr((ord(key[i]) ^ ord(brainf[i]))+22)

print "Initial key:",initial_key

secret_key = "".join([chr(ord(i)+9) for i in initial_key])

print "Secret:",secret_key

"""
f = open("C:\Users\CSAW2016\haha\flag_dir\flag.txt")
f.write(secret_key)
f.close()
"""
