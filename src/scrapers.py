"""All the functions for website scraping

Functions that take the relevant information from the websites of local
pubs and bars, and returns them as a dictionary full of the details

Websites that have had data scraped from are given credit in README
"""


from eventhub import EventHub
from eventproperties import EventProperties
from datetime import datetime


now = datetime.now()
weekday = now.strftime("%A")


def get_duffys_events():
    """
    Creates an instance of EventHub for duffys pub and fills with information on events along with
    an id number

    :return: duffys events with all the variables for the events
    :rtype: dict
    """

    duffys = EventHub(
        'http://www.duffys.ie/best-pub-for-bands-playing-in-malahide-dublin-this-weekend/#more-1518',
        'div',
        {'class': 'blog-post-excerpt'})

    for counter, band_event in enumerate(duffys.events_info[0].find_all('ul')[0].find_all('li')):

        duffys.add_event(counter, {
            EventProperties.DATE: band_event.text.split('>')[0][:-3],
            EventProperties.TIME: band_event.text.split('–')[-1],
            EventProperties.ARTIST_NAME: str(str(band_event.text.split('>')[-1]).split('–')[0]),
            EventProperties.LOCATION: "Duffy's Pub",
            EventProperties.PRICE: '-'
        })

    return duffys.get_events()


def get_gibneys_events():
    """
    Creates an instance of EventHub for gibneys pub and fills with information on events along with
    an id number

    :return: gibneys events with all the variables for the events
    :rtype: dict
    """

    gibneys = EventHub('http://gibneys.com/whats-on.html',
                       'div',
                       {'class': 'menu-group'})

    for counter, band_event in enumerate(gibneys.events_info[0].find_all('div', {'class': 'day-info-wrapper'})):

        music_info = band_event.find_all('div', {'class': 'day-item-description light'})

        if 'from' not in music_info[-1].text:
            continue

        gibneys.add_event(counter, {
            EventProperties.DATE: band_event.find_all('h2', {'class': 'heading'})[0].text + ' ' + str(now.day),
            EventProperties.TIME: music_info[-1].text.split('from')[1],
            EventProperties.ARTIST_NAME: music_info[-1].text.split('from')[0],
            EventProperties.LOCATION: "Gibney's Pub",
            EventProperties.PRICE: '-'
        })

    return gibneys.get_events()


def get_old_school_house_events():
    """
    Creates an instance of EventHub for old school house bar and fills with information on events along
    with an id number
    :return: old school house events with all the variables for the events
    :rtype: dict
    """

    old_school_house = EventHub('https://theoldschoolhouse.ie/entertainment/',
                                'div',
                                {'id': 'panel-37-1-1-1'})

    for counter, band_event in enumerate(old_school_house.events_info[0].find_all('p')):

        if len(band_event.text.split('...')) <= 2:
            artist_name = band_event.text.split('-')[0]
        else:
            artist_name = band_event.text.split('...')[0]

        event_date = [i.text.split(' ')[0] +
                      ' ' +
                      i.text.split(' ')[1][:-2] for i in old_school_house.events_info[0].find_all('h5')][counter]

        old_school_house.add_event(counter, {
            EventProperties.DATE: event_date,
            EventProperties.TIME: band_event.text.split('...')[-1],
            EventProperties.ARTIST_NAME: artist_name,
            EventProperties.LOCATION: "Old School House Bar & Restaurant",
            EventProperties.PRICE: '-'
        })

    return old_school_house.get_events()
