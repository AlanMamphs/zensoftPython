import urllib.request
import urllib.error
import base64
import json
import webbrowser
import sys

class Authorization:
	""" Class for handling authorization and PR fetching"""

	def __init__(self, username, password, team, repos = ''):
	 # initiating class entities
	  self.username = username
	  self.password = password
	  self.team = team
	  self.repos = repos
	  self.url  = "https://api.bitbucket.org/2.0/repositories/"
	  
	
	def encryption(self): # method for encryption

		credentials = base64.b64encode("{0}:{1}".
			format(self.username, self.password).encode()).decode("ascii")

		header = {}
		header["Authorization"] = 'Basic %s'% (credentials)

		return header


	def request(self, url): # method for sending request to bitbucket server

		req = urllib.request.Request(url=url, headers = self.encryption())
		resp = urllib.request.urlopen(req)
		return resp		 



	def jsonify(self, data): # method for converting bytes to dicts

		  my_json = data.decode('utf8')
		  data = json.loads(my_json)
		 
		  return data




	def checkStatusCode(self, url): # method for catching HTTP errors
		try:
		  self.request(url)
		except urllib.error.HTTPError as err:
		  if err.code == 401:
		  	print ("")
		  	print ("Unauthorized. Access Denied. Check your credentials."
		  		,"If your Bitbucket account has two-step verification,"
		  		,"switch it off in your settings.")
		  	sys.exit(1)
		  elif err.code ==400:
		  	print("")
		  	print ( "Could not find the pull requests.")
		  	print("")
		  	sys.exit(1)
		  else:
		  	raise

	

	def response(self, url): # method for returning responses from requests
		# self.checkStatusCode(url)
		resp = self.request(url)
		data = resp.read()
		data = self.jsonify(data)
		return data



	def PRlinksWithRep(self): # method for opening PR links with repos specified
		repo = self.repos.split(" ")
		links= []
			
		for element in repo:
			url = self.url+'%s/%s/pullrequests'%(self.team, element)
				
			data = self.response(url)
			
			for value in data['values']:   # iterating over repo's pull requests
				url = self.url+'%s/%s/pullrequests/%d'%(self.team, element, value['id'])
					
				data = self.response(url)
				for i in data['participants']:   
				# checking if prs are addressed to user for reviewing
					if i['user']['username'] == self.username \
					and i['role'] == 'REVIEWER' and i['approved'] == False \
					and data['state']=='OPEN':
						links.append(data['links']['html']['href']) # appending filtered prs
		return links

	def PrLinksNoRep(self): # method for opening PR links with no repos specified
		url = self.url+self.team
		data = self.response(url)
		repositories = []
		for r in data['values']:
			repositories.append(r['slug'])
		links = []  # list for appropriate pull requests urls
		
		for rep in repositories:      
		# iterating over found repositories for pull requests
			url = self.url+'%s/%s/pullrequests'%(self.team, rep)
			data = self.response(url)

			for value in data['values']:    # accessing each pull request
				url = self.url+'%s/%s/pullrequests/%d'%(self.team, rep, value['id'])
					
				data = self.response(url)

				for i in data['participants']:  
				  # checking if prs are addressed to user for reviewing
					if i['user']['username'] == self.username \
						and i['role'] == 'REVIEWER' \
						and i['approved'] == False \
						and	data['state']=='OPEN':
						

						links.append(data['links']['html']['href']) # appending filtered prs

		return links
	


	def CheckLinksLen(self, links): # method for cheching qty of PRs
		links = links
	
		if len(links)>0 and len(links)<11: # 

			return True
		elif len(links)> 10:
			return False
		else:
			return None


	def openInBrowser(self, links): 
		# iterating over links to open them in the browser
		links = links
		for i in links:
			print ("Opening pull request in default browser....")

			webbrowser.open(i)

	def openTenInBrowser(self, links): 
		# iterating over links to open 10 of them in the browser
		links = links
		print('Two many PRs.')
		print('Opening 10 of them')
		for i in range(9):
			print ("Opening pull request in default browser....")
			webbrowser.open(links[i])


