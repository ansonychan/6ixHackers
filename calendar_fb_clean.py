import facebook
import requests
import httplib2
import os
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import datetime

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    # Refresh from: https://developers.facebook.com/tools/explorer/
    try:
        import argparse
        flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    except ImportError:
        flags = None

    # If modifying these scopes, delete your previously saved credentials
    # at ~/.credentials/calendar-python-quickstart.json
    SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
    CLIENT_SECRET_FILE = 'client_secret.json'
    APPLICATION_NAME = 'Google Calendar API Python Quickstart'

    access_token = 'EAACEdEose0cBAMabFA1uTsSv8R62ncKTBrLUEIk7qbMOvABedZCzyXcOL1W82mJMYnFI6h64yZBDDBaJ7DBQL5NGkeWZAhJ6cv9MLhKth7NqQZAoflX0sqTpnsoNLHTwNIOEG83pyCRY530nctxAWwEgyvuZBFqBZB2j4x7YkF8AZDZD'

    feed_id = '181150768971663'

    graph = facebook.GraphAPI(access_token)
    feed = graph.get_object(feed_id)

    details = graph.get_connections(feed['id'], 'feed')
    LinkList = list()
    PostIDList = list()
    EventsDictionary = dict()

    while True:
        try:
            for data in details['data']:
                link = linkgetter(data=data)
                LinkList.append(link)
            # Attempt to make a request to the next page of data, if it exists.
            details = requests.get(details['paging']['next']).json()
        except KeyError:
            # When there are no more data in feed break
            break
    for EachLink in LinkList:
        PostIDList.append(check_link(feed_id, EachLink))

    for PostID in PostIDList:
        if isLink(graph.get_object(PostID)) == 1:
            if getDetails(graph.get_object(PostID)['link']) != "#":
                event_id = getDetails(graph.get_object(PostID)['link'])

                try:
                    location = graph.get_object(event_id)['location']
                except KeyError:
                    location = ''

                name = graph.get_object(event_id)['name']
                start = graph.get_object(event_id)['start_time']
                end = graph.get_object(event_id)['end_time']
                description = graph.get_object(event_id)['description']

                EventsDictionary[name] = [location, start, end, description]

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    for info in EventsDictionary:
        for name in EventsDictionary[info]:
            event = {
                'summary': info,
                'location': name[0],
                'description': name[3],
                'start': {
                    'dateTime': name[1]
                },
                'end': {
                    'dateTime': name[2]
                }
            }
            event = service.events().insert(calendarId='primary', body=event).execute()
            print('Event created: %s' % (event.get('htmlLink')))

def getDetails(EachLink):
    # (Str) -> Str
    # Iterate through the list of links
    # Check to make sure that the link is of Facebook.com/events
    # If it is not, then we do not care about it.
    if (EachLink[0:32] == "https://www.facebook.com/events/"):
        # check to make sure that it is of a HTTPS facebook.com/events/ link
        # Get the Event ID
        EventID = EachLink[32:-1]
    else:
        EventID = "#"

    return EventID


def check_link(FeedID, EachLink):
    # (Str) -> Str
    # Iterate through the list of links
    # Check to make sure that the link is of Facebook.com/events
    # If it is not, then we do not care about it.
    if(EachLink[0:47] == "https://www.facebook.com/"+FeedID+"/posts/"):
    # check to make sure that it is of a HTTPS facebook.com/events/ link
    # Get the Event ID
        EventID = EachLink[47:]
    else:
        EventID = "#"

    return EventID


def isMultimedia(string):
    '''
    check for photo in link key
    :param string:
    :return: check
    '''

    photostatus = 0
    if ("photo" in string) or ("video" in string):
        photostatus = 1
    return photostatus


def isLink(dict):
    """
    checks for link key
    :param dict:
    :return: check
    """
    test = 0
    for key in dict.keys():
        if key == 'link':
            test =+ 1

    return(test)

def linkgetter(data):
    """
    Access the link of a post
    """
    return (data['actions'][0]['link'])

if __name__ == '__main__':
    main()