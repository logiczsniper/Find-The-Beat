"""All the functions for website scraping

Functions that take the relevant information from the websites of local
pubs and bars, and returns them as a dictionary full of the details

Websites that have had data scraped from are given credit in README
"""


from eventhub import EventHub
from all_properties import EventProperties, ArtistProperties, VenueProperties
from datetime import datetime
from abbreviationconverter import weekday_converter
from abbreviationconverter import month_converter


now = datetime.now()
weekday = now.strftime("%A")


def get_duffys_events():
    """
    Creates an instance of EventHub for duffys pub and fills with information on events

    :return: duffys events with all the variables for the events
    :rtype: list
    """

    duffys = EventHub(
        'http://www.duffys.ie/best-bars-live-music-dublin/#more-1522',
        'div',
        {'class': 'blog-post-excerpt'})
    if len(duffys.events_info) > 0:

        for band_event in duffys.events_info[0].find_all('ul')[0].find_all('li'):

            duffys.add_data_dict({'event_info': {
                EventProperties.DATE_STATUS: None,
                EventProperties.DATE: band_event.text.split('>')[0][:-3] + f" {now.strftime('%B')} {now.year}",
                EventProperties.TIME: band_event.text.split('–')[-1].strip(),
                EventProperties.PRICE: '-'
            }})

            duffys.add_data_dict({'artist_info': {
                ArtistProperties.ARTIST_NAME: str(str(band_event.text.split('>')[-1]).split('–')[0]).strip(),
                ArtistProperties.FACEBOOK_URL: "-",
            }})

            duffys.add_data_dict({'venue_info': {
                VenueProperties.NAME: "Duffy's Pub",
                VenueProperties.ADDRESS: "Main St, Malahide, Co. Dublin",
                VenueProperties.WEBSITE_URL: duffys.url
            }})

    return duffys.get_events()


def get_gibneys_events():
    """
    Creates an instance of EventHub for gibneys pub and fills with information on events.
    In order to get all the information, it must first scrape the url to the more detailed page
    for each of the events, THEN take the event properties

    :return: gibneys events with all the variables for the events
    :rtype: list
    """

    gibneys = EventHub('https://www.ticketweb.ie/search?q=gibneys+malahide',
                       'div',
                       {'class': 'list-group search-result-list event theme-mod'})
    if len(gibneys.events_info) > 0:

        for band_event in gibneys.events_info[0].find_all('div', {
                'class': 'row list-group-item theme-separator-strokes'}):
            new_urls = []

            for link in band_event.find_all('a', {
                    'class': 'main-info theme-title theme-mod-bg mttext-ellipsis mttext-ellipsis-2'
                                                 }):
                if link.get('data-ng-href') is not None:
                    new_urls.append(link.get('data-ng-href')[:-13])

            for event_url in new_urls:

                new_band_event = EventHub(event_url, 'div', {'class': 'event-summary'})
                event_weekday = new_band_event.events_info[0].find_all('h4', {
                        'class': 'info-title theme-title'})[0].text[:3]
                event_month = new_band_event.events_info[0].find_all('h4', {
                        'class': 'info-title theme-title'})[0].text[4:7]
                rest_of_date = new_band_event.events_info[0].find_all('h4', {
                        'class': 'info-title theme-title'})[0].text[7:]

                gibneys.add_data_dict({'event_info': {
                    EventProperties.DATE_STATUS: None,
                    EventProperties.DATE: f"{weekday_converter(event_weekday)} "
                                          f"{month_converter(event_month)}{rest_of_date}",
                    EventProperties.TIME: new_band_event.events_info[0].find_all('h5', {
                        'class': 'info-content theme-content'})[0].text,
                    EventProperties.PRICE: new_band_event.events_info[0].find_all('h4', {
                        'class': 'info-title theme-title'})[1].text.strip()
                }})

                gibneys.add_data_dict({'artist_info': {
                    ArtistProperties.ARTIST_NAME: new_band_event.html.find_all('span', {'class': 'big'})[0].text[8:-7],
                    ArtistProperties.FACEBOOK_URL: "-",
                }})

                gibneys.add_data_dict({'venue_info': {
                    VenueProperties.NAME: "Gibney's Pub",
                    VenueProperties.ADDRESS: "6 New St, Malahide, Co. Dublin",
                    VenueProperties.WEBSITE_URL: gibneys.url
                }})

    return gibneys.get_events()
