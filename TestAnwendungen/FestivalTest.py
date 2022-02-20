import subprocess

text = '"Hello from a python program"'

filename = 'python_text.txt'

file=open(filename,'w')

file.write(text)

file.close()

subprocess.call('festival --tts '+filename, shell=True)

subprocess.call('rm -f '+filename, shell=True)

 