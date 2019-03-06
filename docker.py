#!/usr/bin/python3
import cgi,cgitb
import random
import json
cgitb.enable()
global subprocess
import subprocess

print("Content-type: application/json")
print ()

fs = cgi.FieldStorage()

lang = str(fs.getvalue('language'))
code = str(fs.getvalue('code'))
#lang = "CPP"
host = "http://localhost:"
result = {}
url = ""

# Filename: Random number between 1 and 10^19
filename = str(random.randint(1,10**19))

def Docker_RMI():
	# Clear the clutter, delete old Docker Images
	process = subprocess.Popen(['docker', 'images'], stdout=subprocess.PIPE)
	build_images = process.communicate()

	# Stop all stopped containers: docker rm $(docker ps -a -q)

	# TODO: kill containers running >= 1hr
	# kill all running containers and save the list in killed-containers.txt:
	# docker ps | awk {' print $1 '} | tail -n+2 > killed-containers.txt; for line in $(cat killed-containers.txt); do docker kill $line; done;
	# Kill ttyd processes to release ports
	# ps -e | grep ttyd | awk {' print $1 '} | tail -n+3 > ttyd.txt for line in $(cat ttyd.txt); do sudo kill $line; done;
	# ps -e | grep ttyd | awk {'print $1'} | tail -n+2 > ttyd.txt 
    # for PID in $(cat ttyd.txt); do ps -p $PID -o pid,args=ARGS; done;

	try:
		for i in range(1,len(build_images.split("\n"))):
			docker_image=build_images.split('\n')[i].split()[2]

			# Preserve important images used for building new images
			if(docker_image not in ['8357b3fcbe41', '8ac48589692a', 'efb6baa1169f', '8357b3fcbe41', '1b3de68a7ff8']):
				subprocess.getoutput("docker rmi -f {image}".format(image = docker_image))
	except:
		print ("")		

def Lang_C_CPP(lang):
		ext = "c" if lang == "c" else "cpp" 
		code_file = filename + ".{ext}".format(ext = ext)
		executable_file =  "myprog"
		
		program_code = "{0}".format(code)
		write_code_file = open("code_files/" + code_file, "w+")
		if program_code == "None":
			program_code = """
#include <iostream>
using namespace std;

int main(){
cout << "\033[1;31mForgot to type in some code,\033[0m \033[1;32m or is it intentional beta testing?\033[0m\\n";
cout << "\033[1;36mHere\'s a hello world program for you!\033[0m\\n\\n";
cout << "\\t\033[1;33m#include <iostream>\\n";
cout << "\\tusing namespace std;\\n\\n";
cout << "\\tint main() \\n";
cout << "\\t{\\n";
cout << "\\t    cout << \'Hello, World!\'\\n";
cout << "\\t    return 0;\\n";
cout << "\\t}\\n\033[0m";
cout << endl << endl;
cout << "\033[7;36mInstructions:\033[0m";
cout << "\\n\\t\033[1;32m*\033[0m Type \033[1;36mls\033[0m to list all the file available.";
cout << "\\n\\t\033[1;32m*\033[0m Use \033[1;36mnano/vim {filename}\033[0m to edit file.";
cout << "\\n\\t\\tEg. \033[1;36mnano main.cpp\033[0m";
cout << "\\n\\t\\\t  \033[1;36mctrl + x\033[0m to write changes made in the file.\\n\\t\\t  Press \033[1;36my\033[0m to save the file.";
cout << "\\n\\t\033[1;32m*\033[0m Compile it manually: \'\033[1;36mg++ main.cpp -o myprog\033[0m\'.";
cout << "\\n\\t\033[1;32m*\033[0m Execute: \'\033[1;36m./myprog\033[0m\'.\\n\\n";
cout << "\\n\033[1;32m>> \033[0mCode from textarea is saved in \033[1m\033[1;30;47m main.cpp \033[0m\033[0m and compiled to \033[1m\033[1;30;47m myprog \033[0m\033[0m";
cout << "\\n\033[1;32m>> \033[0mEdit the code in  terminal \033[1m\033[1;30;47m nano main.cpp \033[0m\033[0m";
cout << "\\n\033[1;32m>> \033[0mRun the compiled program: \033[1m\033[1;30;47m ./myprog \033[0m\033[0m";
cout << "\\n\033[1;32m>> \033[0mUse command \033[1m\033[1;30;47m howto \033[0m\033[0m to display these instructions again\\n\\n\\n";
cout << "\033[1;37mEnjoy!";
cout << "\\n-Abhishek\033[0m\\n\\n";
return 0;
}"""
		write_code_file.write(program_code)
		write_code_file.close()

		# Generate random number within userable port range, check whether the port is avaialable for use, loop until available
		available = 0
		while available == 0:
			for i in range (1,200):
				port = random.randint(1234,65535)
				if PortCheck(port) == "available":
					port = port
					break
				break
			break

		compiler = "gcc" if lang == "c" else "g++"

		# Container ID to be smaller in digits and hash to be always positive
		container_id = abs(hash(filename))

		# "docker build -t gcc-nano -f GCCDockerfile ." to custom build gcc:7.3 docker image with nano and vim 
		launch_container = "docker run -itd --rm --stop-timeout 120 --name {container} gcc-nano howto && \
		docker cp code_files/{codefile} {container}:/home/main.{ext} && \
		docker exec {container} {compiler} main.{ext} -o {exec}".format(codefile = code_file,container = container_id, ext = ext, compiler = compiler, exec = executable_file)
		web_shell = "ttyd -p {port} -r 2 -d 0 docker attach {container}".format(container = container_id, port = port)
		
		# Execute the commands specified in the string commands above	
		subprocess.Popen(launch_container, shell=True, close_fds=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
		subprocess.Popen(web_shell, shell=True, close_fds=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
		
		# The ttyd URL
		url = host + str(port)
		
		# Return JSON back to index.py
		result['url'] = url
		result['success'] = True
		print (json.dumps(result))		

def Lang_Python(ver):
	# To use Python2 or 3 Docker container
	Dockerfile = """
	FROM python:{ver}
	COPY {File} /usr/src/mypy
	WORKDIR /usr/src/mypy
	CMD ["{PyVer} {File}"]
	""".format(File = File, ver = ver, PyVer = "Python2" if ver == 2 else "Python3")	
	print (Dockerfile)

def ttyOverBrowser(port, docker_cmd):
	subprocess.getoutput("ttyd -p {port} --once {cmd} &".format(port = port, cmd = docker_cmd))

def PortCheck(port):
	p1 = subprocess.Popen(["netstat", "-an"], stdout=subprocess.PIPE)
	p2 = subprocess.Popen(["grep", "{port}".format(port = port)], stdin=p1.stdout, stdout=subprocess.PIPE)
	p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
	output = p2.communicate()[0]
	if (output):
		return ("unavailable")
	else:
		return ("available")

def choice():
	if (lang == "c" or lang == "cpp"):
		l = "c" if lang == "c" else "cpp"
		Lang_C_CPP(l)
	elif (lang == "Python2" or lang == "Python3"):
		ver = ("{ver}").format(ver = 2 if lang == "Python2" else "3")
		Lang_Python(ver)

def main():
	#Docker_RMI()
	Lang_C_CPP(lang)
main()

