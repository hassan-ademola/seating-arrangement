from config import client_id, client_secret
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

client = BackendApplicationClient(client_id=client_id)
oauth = OAuth2Session(client=client)

token = oauth.fetch_token(token_url="https://api.intra.42.fr/oauth/token",
 						  client_id=client_id,
 						  client_secret=client_secret)

# import time
# i = 1
# results = 0
# while True:
# 	r = oauth.get(f"https://api.intra.42.fr/v2/campus/43/users?page={i}")
# 	print(i)
# 	results += len(r.json())
# 	if 'next' not in r.links.keys():
# 		break
# 	if 'ademola' in [s['last_name'].lower() for s in r.json()]:
# 		print(r.json())
# 		break
# 	time.sleep(3)
# 	i+=1
# print(results)
#lab3r8s6
#lab3r2s5
#id128306
r = oauth.get("https://api.intra.42.fr/v2/campus/43")
print(r.json())
# print([s for s in r.json() if (s['user']['location'] != s['host'])])
# hosts = [s['host'] for s in r.json()]
# print(hosts)
# counts = {i:hosts.count(i) for i in set(hosts)}
# print(sorted(counts.items(),key = lambda x:x[1],reverse=True))
