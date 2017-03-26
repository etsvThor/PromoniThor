from datetime import datetime

import requests
from lxml import html
from requests_ntlm import HttpNtlmAuth

from index.calendar_login import username, password


def activity_parser():
    """
    Load activities from the thor calendar and return them as json data
    """
    r = requests.get('https://sites.ee.tue.nl/studentenverenigingen/thor/Lists/Calendar/MyItems.aspx',
                     auth=HttpNtlmAuth("TUE\\"+username, password))
    print(r.status_code)
    if r.status_code != 200:
        return {"error": "Wrong status code"}

    tree = html.fromstring(r.content)

    events = tree.xpath('//tr[contains(@class,"itmhover")]')

    events_json = []

    for event in events:

        #4th TD contains title
        title = event[4].text_content().strip()
        titlel = title.lower()
        # skip all options and intern activities. If title starts with [option][optie][internal][intern] or so
        if "[opt" in titlel or "[int" in titlel:
            continue

        #5th TD has the location, 6th the starttime, 7 th the endtime and 8 whether the event is all - day
        location = event[5].text_content().strip()
        starttime = event[6].text_content().strip()
        endtime = event[7].text_content().strip()
        allday = True if len(event[8].text_content().strip()) > 1 else False

        if starttime:
            starttime = int(datetime.strptime(starttime, "%m/%d/%Y %I:%M %p").timestamp())
        else:
            starttime = False

        if endtime:
            endtime = int(datetime.strptime(endtime, "%m/%d/%Y %I:%M %p").timestamp())
        else:
            endtime = False

        now = int(datetime.now().timestamp())

        if endtime and endtime < now:
            #event already finished
            continue

        #give classes according to association
        if 'ieee' in titlel:
            ass = 'ieee'
        elif 'waldur' in titlel:
            ass = 'waldur'
        elif 'odin' in titlel:
            ass = 'odin'
        elif 'thor' in titlel or 'walhalla' in titlel or 'kvasir' in titlel or 'acci' in titlel or 'ivaldi' in titlel:
            ass = 'thor'
        else:
            ass = 'gen'

        events_json.append({"tit": title,
                            "ass": ass,
                            "loc": location,
                            "sta": starttime,
                            "end": endtime,
                            "ald": allday
                            })
    return events_json