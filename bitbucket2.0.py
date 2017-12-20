from model import Authorization



def bitbucketPr():
	# method with logic for the PR fetching
	team, username, password, repos = '', '', '', ''
	# inquiring user credentials
	while not username:
		username =  input("Please enter your BitBucket account username:")
	# while not email:
	# 	email    =  input("Please enter your BitBucket account email:")
	while not password:
		password =  input("Please enter your BitBucket account password:")
	while not team:
		team     =   input('Please enter your Bitbucket team name:')
	# specifying the repository
	repos = input("Indicate either a reposiory or a list of repositories"+ \
								 "dividing each by space and press enter." + \
								 " Leave empty if you want to search in all team repositories:")
	
	# new instance of Authorisation class
	newAuth = Authorization(username, password, team, repos)

	links = [] 

	if not newAuth.repos: # method for handling no repo situationA
		links = newAuth.PrLinksNoRep()
		# handling PR's opening according to links' length
		if newAuth.CheckLinksLen(links) == True:  
			newAuth.openInBrowser(links)

		elif newAuth.CheckLinksLen(links) == False:
			print("")
			print("Two many pull requests. Try to filter by repository.")
			print("")
		elif newAuth.CheckLinksLen(links) == None:
			print("")
			print("Nothing was found. Try checking your credentials")
			print("")

	else: # if repo is specified
		links = newAuth.PRlinksWithRep()
		if newAuth.CheckLinksLen(links) == True:
			newAuth.openInBrowser(links)

		elif newAuth.CheckLinksLen(links) == False:
			print("")
			print('Two many PRs.')
			print('Opening 10 of them')
			print("*" *20)

			newAuth.openTenInBrowser(links)

		elif newAuth.CheckLinksLen(links) == None:
			print("")
			print("Nothing was found. Try checking your credentials")
			print("")
	

	

bitbucketPr()