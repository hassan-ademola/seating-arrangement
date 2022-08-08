from config import client_id, client_secret
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from datetime.datetime import strptime,strftime
from datetime import timedelta

EXAM_ENDPOINT = "https://api.intra.42.fr/v2/exams"
USER_ENDPOINT = "https://api.intra.42.fr/v2/users"

parse = lambda x: strptime(x,'%Y-%m-%dT%H:%M:%S.%fZ')

def get_lab_freqs(locations):
    labs = [(location.split('r')[0]).title() for location in locations]
    freqs = {lab: round(labs.count(lab)/len(labs),2) for lab in labs}
    ordered = sorted(freqs,key=lambda x: freqs[x],reverse=True)
    ordered_freqs = {lab:freqs[lab] for lab in ordered}
    return ordered_freqs


client = BackendApplicationClient(client_id=client_id)
oauth = OAuth2Session(client=client)

token = oauth.fetch_token(token_url="https://api.intra.42.fr/oauth/token",
                          client_id=client_id,
                          client_secret=client_secret)

class Exam:
    def __init__(self,exam_id, session):
        self.exam_id = exam_id
        self.session = session
        self.exam_details = session.get(f"{EXAM_ENDPOINT}/{exam_id}").json()
        self.subscribers = {}
        

    def get_subscribers_details(self):
        page = 1
        response = self.session.get(f"{EXAM_ENDPOINT}/{self.exam_id}/exam_users?per_page=100")
        while (len(response.json()) != 0):
            for subscriber in response:
                self.subscribers[str(subscriber['id'])] = subscriber['user']
            page+=1
            response = self.session.get(f"{EXAM_ENDPOINT}/{self.exam_id}/exam_users?page={page}&per_page=100")
        return self
    
    def get_recent_locations(self):
        max_value = self.exam_details['begin_at']
        min_value = strftime(parse('2022-08-07T12:35:36.508Z') - timedelta(weeks=1),'%Y-%m-%dT%H:%M:%S.%fZ')
        for subscriber_id in subscribers.keys():
            subscribers[subscriber_id]['recent_locations'] = self.session.get(f"{USER_ENDPOINT}/{subscriber_id}/locations?per_page=100&range[begin_at]=min_value,max_value
            subscribers[subscriber_id]['last_location'] = subscribers[subscriber_id]['recent_location'][0]
            subscribers[subscriber_id]['lab_freqs'] = get_lab_freqs(subscribers[subscriber_id]['recent_locations'])                                                                
        return self

# get exam locations
labs = exam.exam_details['location'].replace(',','').split()

# get ids of most frequent users for each lab
most_frequent_users = {lab:[] for lab in labs}
for lab in most_frequent_users:
    for user_id in exam.subscribers:
        if exam.subscribers[user_id]['lab_freqs'][0] == lab:
            most_frequent_users[lab].append(user_id)
import numpy as np
rows = {'Lab1':6,'Lab2':4,'Lab3':8}
columns = 14
labs = ['Lab1','Lab2']

# create empty spaces
arrangement = {lab:np.zeros((rows[lab],columns),int) for lab in labs }

# create assigned and unassigned subscribers
assigned = []
unassigned = list(exam.keys())

# put lab most_frequent users in others
for lab in labs:
    temp = set(labs) - set(lab)
    choice = random.choice(temp)
    empty = arrangement[lab][:,::2]
    for column in range(empty.shape[1]):
        for row in range(rows[choice]):
            subscriber = random.choice(most_frequent_users[lab])
            empty[row,column] = int(subscriber)
            assigned.append(subscriber)
            unassigned.remove(subscriber)
            if (len(most_frequent_users[lab]) == 0):
                break
        if (row != (rows[choice] - 1)):
            break

# assign other subscribers to remaining seats
for lab in arrangement:
    if (arrangement[lab].any() == 0):
        continue
    for column in range(columns):
        for row in range(rows):
            subscriber = random.choice(unassigned)
            arrangement[lab][row,column] = int(subscriber)
            assigned.append(subscriber)
            unassigned.remove(subscriber)
            if (len(unassigned) == 0):
                break
        if (len(unassigned) == 0):
                break
    if (len(unassigned) == 0):
                break

#print arrangements
print(arrangement)
