"""All the functions for website scraping in Swords

Functions that take the relevant information from the websites of local
pubs and bars, and returns them as a dictionary full of the details

Websites that have had data scraped from are given credit in README
"""


from eventhub import EventHub
from all_properties import EventProperties, ArtistProperties, VenueProperties
from datetime import datetime


now = datetime.now()
weekday = now.strftime("%A")


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
                      i.text.split(' ')[2] +
                      ' ' +
                      i.text.split(' ')[1][:-2] +
                      ' ' +
                      str(now.year) for i in old_school_house.events_info[0].find_all('h5')][counter]

        old_school_house.add_data_dict({'event_info': {
            EventProperties.DATE_STATUS: None,
            EventProperties.DATE: event_date,
            EventProperties.TIME: band_event.text.split('...')[-1],
            EventProperties.PRICE: '-'
        }})

        old_school_house.add_data_dict({'artist_info': {
            ArtistProperties.ARTIST_NAME: artist_name,
            ArtistProperties.FACEBOOK_URL: "-"
        }})

        old_school_house.add_data_dict({'venue_info': {
            VenueProperties.NAME: "Old School House Bar & Restaurant",
            VenueProperties.ADDRESS: "Church Rd, Swords Glebe, Swords, Co. Dublin",
            VenueProperties.WEBSITE_URL: old_school_house.url
        }})

    return old_school_house.get_events()
