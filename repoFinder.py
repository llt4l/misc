#!/usr/bin/python
from github import Github
import argparse

# Put in your personal access token here:
gitAPIKey = ""

userDB = []
repoDB = dict()


def getUsers(userFile):
	with open (userFile) as uF:
		lines = uF.read().splitlines()
	print "Got Users"
	return lines

def pullStarredRepos():	
	gitClient = Github(gitAPIKey)
	for user in userDB:
		for repo in gitClient.get_user(user).get_starred():
			if repo.name in repoDB:
				if user not in repoDB[repo.name]:
				    repoDB[repo.name].append(user)
			else:
				repoDB[repo.name] = [user]

		print "Pulled "+user+" starred repos"

	print "Got Starred Repos"



if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Interesting Github Repo Finder')
	parser.add_argument('-u','--users', help='List of users', required=True)
	parser.add_argument('-f','--fileout', help='Save results to file', required=False)
	parser.add_argument('-c','--count', help='Min number of passed users that starred the repo', required=False, default=2)
	args = vars(parser.parse_args())
	
	# Loads users from file into userDB
	userDB = getUsers(args['users'])

	# Get the list of repos each user starred
	pullStarredRepos()

	for k in sorted(repoDB, key=lambda k: len(repoDB[k]), reverse=True):
		if len(repoDB[k]) > args['count']:
			print k+" - Starred by: "+str(repoDB[k])
