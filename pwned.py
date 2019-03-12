from hashlib import sha1
from urllib.request import Request, urlopen
import sys

passwordsToCheck = sys.argv[1:]
if len(passwordsToCheck) == 0:
	print("No passwords provided")
	quit()

apiURL = "https://api.pwnedpasswords.com/range/"

def checkPassword(password):
	passwordHash = sha1(password.encode("utf-8")).hexdigest().upper()
	hashPrefix, hashSufix = passwordHash[:5], passwordHash[5:]
	request = Request(apiURL + hashPrefix, headers = {'User-Agent': 'Mozilla/5.0'})
	retrievedHashes = str(urlopen(request).read(), "utf-8")
	retrievedHashesList = list(map(lambda x: x.split(":"), retrievedHashes.splitlines()))
	for hash in retrievedHashesList:
		if hashSufix == hash[0]:
			print("{0} was found!\nHash: {1}, Occurences: {2}\n".format(password, passwordHash, hash[1]))
			return
	print("{0} was not found\n".format(password))

for password in passwordsToCheck:
	checkPassword(password)