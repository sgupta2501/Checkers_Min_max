
import subprocess
print("choose:")
print("1:AI")
print("2:RANDOM")
a=int(input())
#print(a)
file=open('geek.txt','w')
pm=str('')
if(a==1):
    pm='AI'
if(a==2):
    pm='RANDOM'
file.write(pm)
#print(pm)
file.close()

subprocess.call('python3 main.py', shell=True)
