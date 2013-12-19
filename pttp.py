#Imports
import sys
#Make sure we are running in Python 3 before importing more stuff
if sys.version_info<(3,0,0):
	print("You need Python 3 to run PTTP.")
	sys.exit()

import os
import subprocess
import urllib.request
import urllib.parse
import base64

parameters = {}

#Functions
def request(requestType, url, username, password, parameters):
	if username == "" or password == "":
		#No authentication
		authentication = False
	else:
		#Basic Authentication
		authentication = True

	if requestType == "GET":
		#Encode the arguments
		parse = urllib.parse.urlparse(url)
		urlArgs = parse[4]
		if urlArgs != "":
			urlArgs = urlArgs.split("&")
			arguments = []
			for argument in urlArgs:
				argument = argument.split("=", 1)
				name = urllib.parse.quote_plus(argument[0])
				value = urllib.parse.quote_plus(argument[1])
				argument = name+"="+value
				arguments.append(argument)
			urlArgs = "&".join(arguments)
			url = parse[0]+"://"+parse[1]+parse[2]+parse[3]+"?"+urlArgs+parse[5]

		#Make the request
		request = urllib.request.Request(url)
		request.add_header("User-Agent", "PTTP")

		#Do we need to add authentication to this request?
		if authentication:
			request.add_header('Authorization', b'Basic ' + base64.b64encode(str.encode(username)+b':'+str.encode(password)))

		output = urllib.request.urlopen(request)
		#Decode the output
		output = output.read().decode('utf-8')

		#Write output to a file
		outFile = open("response.txt", "w+")
		outFile.write(output)
		outFile.close()
	elif requestType == "POST":
		#Set the headers
		host = urllib.parse.urlparse(url)
		host = host[1]
		headers = {
			"User-Agent" : "PTTP",
			"Content-type": "application/x-www-form-urlencoded",
			"Host" : host,
			"Referer" : "https://github.com/NickGeek/pttp"
		}

		#Do we need to add authentication to this request?
		if authentication:
			headers['Authorization'] = b'Basic ' + base64.b64encode(str.encode(username)+b':'+str.encode(password))

		#Encode the parameters
		parameters = urllib.parse.urlencode(parameters)
		parameters = parameters.encode('utf-8')

		#Make the request
		request = urllib.request.Request(url, parameters, headers)
		output = urllib.request.urlopen(request)
		output = output.read().decode('utf-8')

		#Write output to a file
		outFile = open("response.txt", "w+")
		outFile.write(output)
		outFile.close()

def get(option):
	if option == "No authentication":
		url = subprocess.getoutput("echo `zenity --entry --title='PTTP' --text='URL to send the request to (must start with http:// or https://. Your arguments will be encoded, don't encode them yourself):' --ok-label='Send request'`")
		url = url.split("\n")
		url = url[len(url) - 1]
		if url != "":
			request("GET", url, "", "", "")
			os.system("zenity --text-info --html --title='PTTP' --filename='response.txt'")
			os.remove("response.txt")
			menu()
		else:
			menu()
	elif option == "Basic authentication":
		credentials = subprocess.getoutput("echo `zenity --forms --title='PTTP' --text='HTTP Basic Authentication' --add-entry='Username' --add-password='Password'`")
		credentials = credentials.split("\n")
		credentials = credentials[len(credentials) - 1]
		if credentials != "":
			credentials = credentials.split("|")
			username = credentials[0]
			password = credentials[1]
			url = subprocess.getoutput("echo `zenity --entry --title='PTTP' --text='URL to send the request to (must start with http:// or https://. Your arguments will be encoded, don't encode them yourself):' --ok-label='Send request'`")
			url = url.split("\n")
			url = url[len(url) - 1]
			if url != "":
				request("GET", url, username, password, "")
				os.system("zenity --text-info --html --title='PTTP' --filename='response.txt'")
				os.remove("response.txt")
				menu()
			else:
				menu()
		else:
			menu()
	elif option == "No authentication (plain text)":
		url = subprocess.getoutput("echo `zenity --entry --title='PTTP' --text='URL to send the request to (must start with http:// or https://. Your arguments will be encoded, don't encode them yourself):' --ok-label='Send request'`")
		url = url.split("\n")
		url = url[len(url) - 1]
		if url != "":
			request("GET", url, "", "", "")
			os.system("zenity --text-info --title='PTTP' --filename='response.txt'")
			os.remove("response.txt")
			menu()
		else:
			menu()
	elif option == "Basic authentication (plain text)":
		credentials = subprocess.getoutput("echo `zenity --forms --title='PTTP' --text='HTTP Basic Authentication' --add-entry='Username' --add-password='Password'`")
		credentials = credentials.split("\n")
		credentials = credentials[len(credentials) - 1]
		if credentials != "":
			credentials = credentials.split("|")
			username = credentials[0]
			password = credentials[1]
			url = subprocess.getoutput("echo `zenity --entry --title='PTTP' --text='URL to send the request to (must start with http:// or https://. Your arguments will be encoded, don't encode them yourself):' --ok-label='Send request'`")
			url = url.split("\n")
			url = url[len(url) - 1]
			if url != "":
				request("GET", url, username, password, "")
				os.system("zenity --text-info --title='PTTP' --filename='response.txt'")
				os.remove("response.txt")
				menu()
			else:
				menu()
		else:
			menu()
	else:
		menu()

def addParameter():
	parameter = subprocess.getoutput("echo `zenity --forms --title='PTTP' --text='Add parameter' --add-entry='Name' --add-entry='Value'`")
	parameter = parameter.split("\n")
	parameter = parameter[len(parameter) - 1]
	return parameter

def postPrams(option, url, username, password):
	global parameters

	requestMenu = subprocess.getoutput("echo `zenity --list --title='PTTP' --text='Build your request:' --column='Option' 'Add parameter' 'Send request'`")
	requestMenu = requestMenu.split("\n")
	requestMenu = requestMenu[len(requestMenu) - 1]

	if requestMenu == "Add parameter":
		parameter = addParameter()
		if parameter != "":
			parameter = parameter.split("|")
			name = parameter[0]
			value = parameter[1]
			parameters[name] = value
			postPrams(option, url, username, password)
		else:
			postPrams(option, url, username, password)
	elif requestMenu == "Send request":
		request("POST", url, username, password, parameters)
		if option == "No authentication (plain text)" or option == "Basic authentication (plain text)":
			os.system("zenity --text-info --title='PTTP' --filename='response.txt'")
		else:
			os.system("zenity --text-info --html --title='PTTP' --filename='response.txt'")
		os.remove("response.txt")
		parameters = {}
		menu()
	else:
		menu()

def post(option):
	if option == "No authentication":
		url = subprocess.getoutput("echo `zenity --entry --title='PTTP' --text='URL to send the request to (must start with http:// or https://):' --ok-label='Send request'`")
		url = url.split("\n")
		url = url[len(url) - 1]
		if url != "":
			postPrams(option, url, "", "")
		else:
			menu()
	elif option == "Basic authentication":
		credentials = subprocess.getoutput("echo `zenity --forms --title='PTTP' --text='HTTP Basic Authentication' --add-entry='Username' --add-password='Password'`")
		credentials = credentials.split("\n")
		credentials = credentials[len(credentials) - 1]
		if credentials != "":
			credentials = credentials.split("|")
			username = credentials[0]
			password = credentials[1]
			url = subprocess.getoutput("echo `zenity --entry --title='PTTP' --text='URL to send the request to (must start with http:// or https://):' --ok-label='Send request'`")
			url = url.split("\n")
			url = url[len(url) - 1]
			if url != "":
				postPrams(option, url, username, password)
			else:
				menu()
		else:
			menu()
	elif option == "No authentication (plain text)":
		url = subprocess.getoutput("echo `zenity --entry --title='PTTP' --text='URL to send the request to (must start with http:// or https://):' --ok-label='Send request'`")
		url = url.split("\n")
		url = url[len(url) - 1]
		if url != "":
			postPrams(option, url, "", "")
		else:
			menu()
	elif option == "Basic authentication (plain text)":
		credentials = subprocess.getoutput("echo `zenity --forms --title='PTTP' --text='HTTP Basic Authentication' --add-entry='Username' --add-password='Password'`")
		credentials = credentials.split("\n")
		credentials = credentials[len(credentials) - 1]
		if credentials != "":
			credentials = credentials.split("|")
			username = credentials[0]
			password = credentials[1]
			url = subprocess.getoutput("echo `zenity --entry --title='PTTP' --text='URL to send the request to (must start with http:// or https://):' --ok-label='Send request'`")
			url = url.split("\n")
			url = url[len(url) - 1]
			if url != "":
				postPrams(option, url, username, password)
			else:
				menu()
		else:
			menu()
	else:
		menu()

def menu():
	requestMenu = subprocess.getoutput("echo `zenity --list --title='PTTP' --text='What type of request do you want to make?' --column='Request type' 'GET' 'POST'`")
	requestMenu = requestMenu.split("\n")
	requestMenu = requestMenu[len(requestMenu) - 1]

	if requestMenu == "GET":
		#Do a GET request
		getMenu = subprocess.getoutput("echo `zenity --list --title='PTTP' --text='Authentication/response:' --column='Option' 'No authentication' 'Basic authentication' 'No authentication (plain text)' 'Basic authentication (plain text)'`")
		getMenu = getMenu.split("\n")
		getMenu = getMenu[len(getMenu) - 1]
		get(getMenu)
	elif requestMenu == "POST":
		#Do a POST request
		postMenu = subprocess.getoutput("echo `zenity --list --title='PTTP' --text='Authentication/response:' --column='Option' 'No authentication' 'Basic authentication' 'No authentication (plain text)' 'Basic authentication (plain text)'`")
		postMenu = postMenu.split("\n")
		postMenu = postMenu[len(postMenu) - 1]
		post(postMenu)
	else:
		sys.exit()

menu()