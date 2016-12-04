import facebook
import requests


#access_token = 'EAACEdEose0cBABGnarZCO3fV7qLGGqijBAVo8VzLWQaPx0SXfba7rn1iDYj4Am0AZBmazE6OPRzYixVTUy0EZCT9OK1FHL2tZBA4mzn4NQ4WZBxZC94CAnpnTKxLbGlUhGJy1ZBCvpsZAOctVJqVIT5WKm7AA3slJ997lMqS3ZAmYYwZDZD'
#user = '181150768971663'
#URL = 'https://graph.facebook.com/'+user+'/groups?access_token='+access_token+'/posts'

#page = requests.get(URL).text

#print(page)

def some_action(post):
    """ Here you might want to do something with each post. E.g. grab the
    post's message (post['message']) or the post's picture (post['picture']).
    In this implementation we just print the post's created time.
    """
    print(post['caption'])
    print(post['link'])

# You'll need an access token here to do anything.  You can get a temporary one
# here: https://developers.facebook.com/tools/explorer/
access_token = 'EAACEdEose0cBABCbUewODuzivXXlIbYVoLb96np8CMHMzW780NLJWUZCEEXqZCoZB4ZBFLd4KFPOFN9ceO0sZC7LXHmai26Ew0nj879suvffNOmD10Dc7f0bJi171xMZAmHjDMaLYg02K4ijdhAUZCZAa7p04o5IxLmQcORV6qWxJAZDZD'
# 6ix hackers ID
#user = 'BillGates'

#graph = facebook.GraphAPI(access_token)
#profile = graph.get_object(user)
#print(profile)
#print(profile['id'])
#posts = graph.get_connections(profile['id'], 'posts')
#print(posts)

user = '181150768971663' #1350093841689852

graph = facebook.GraphAPI(access_token)
profile = graph.get_object(user)
print(profile)
print(profile['id'])
posts = graph.get_connections(profile['id'], 'feed')
print(posts)

# Wrap this block in a while loop so we can keep paginating requests until
# finished.
while True:
    try:
        # Perform some action on each post in the collection we receive from
        # Facebook.
        [some_action(post=post) for post in posts['data']]
        # Attempt to make a request to the next page of data, if it exists.
        posts = requests.get(posts['paging']['next']).json()
    except KeyError:
        # When there are no more pages (['paging']['next']), break from the
        # loop and end the script.
        break
# Refer to the Python quickstart on how to setup the environment:
# https://developers.google.com/google-apps/calendar/quickstart/python
# Change the scope to 'https://www.googleapis.com/auth/calendar' and delete any
# stored credentials.

event = {
  'summary': 'Google I/O 2015',
  'location': '800 Howard St., San Francisco, CA 94103',
  'description': 'A chance to hear more about Google\'s developer products.',
  'start': {
    'dateTime': '2015-05-28T09:00:00-07:00',
    'timeZone': 'America/Los_Angeles',
  },
  'end': {
    'dateTime': '2015-05-28T17:00:00-07:00',
    'timeZone': 'America/Los_Angeles',
  },
  'recurrence': [
    'RRULE:FREQ=DAILY;COUNT=2'
  ],
  'attendees': [
    {'email': 'lpage@example.com'},
    {'email': 'sbrin@example.com'},
  ],
  'reminders': {
    'useDefault': False,
    'overrides': [
      {'method': 'email', 'minutes': 24 * 60},
      {'method': 'popup', 'minutes': 10},
    ],
  },
}

event = service.events().insert(calendarId='primary', body=event).execute()
print 'Event created: %s' % (event.get('htmlLink'))