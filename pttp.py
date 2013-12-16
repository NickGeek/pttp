#Imports
import sys
import os
import subprocess
import urllib.request
import base64

#Make sure we are running in Python 3
if sys.version_info<(3,0,0):
	print("You need Python 3 to run PTTP.")
	sys.exit()

#Functions
def request(requestType, url, username, password):
	if username or password == "":
		#No authentication
		authentication = False
	else:
		#Basic Authentication
		authentication = True

	if requestType == "GET":
		#Make the request
		request = urllib.request.Request(url)
		request.add_header("User-Agent", "PTTP")
		output = urllib.request.urlopen(request)
		#Decode the output
		output = output.read().decode('utf-8');

		#Write output to a file
		outFile = open("response.txt", "w+")
		outFile.write(output)
		outFile.close()
	elif requestType == "POST": 
		print("I'll put this feature in later")

	return output

def get(option):
	if option == "No authentication":
		url = subprocess.getoutput("echo `zenity --entry --title='PTTP' --text='URL to send the request to:' --ok-label='Send request'`")
		url = url.split("\n")
		url = url[len(url) - 1]
		if url != "":
			print(request("GET", url, "", ""))
			os.system("zenity --text-info --html --title='PTTP' --filename='response.txt'")
			os.remove("response.txt")
			menu()
		else:
			menu()
	elif option == "Basic authentication":
		print("I'll put this feature in later")
	else:
		menu()

def menu():
	requestMenu = subprocess.getoutput("echo `zenity --list --title='PTTP' --text='What type of request do you want to make?' --column='Request type' 'GET' 'POST'`")
	requestMenu = requestMenu.split("\n")
	requestMenu = requestMenu[len(requestMenu) - 1]

	if requestMenu == "GET":
		#Do a GET request
		getMenu = subprocess.getoutput("echo `zenity --list --title='PTTP' --text='Authentication' --column='Option' 'No authentication' 'Basic authentication'`")
		getMenu = getMenu.split("\n")
		getMenu = getMenu[len(getMenu) - 1]
		get(getMenu)

	elif requestMenu == "POST":
		print("POST")
	else:
		sys.exit()

menu()