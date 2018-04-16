"""All the functions for website scraping

Functions that take the relevant information from the websites of local
pubs and bars, and returns them as a dictionary full of the details

Websites that have had data scraped from are given credit in README
"""


from eventhub import EventHub
from eventproperties import EventProperties
from datetime import datetime
from abbreviationconverter import weekday_converter
from abbreviationconverter import month_converter


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
        'http://www.duffys.ie/best-bars-live-music-dublin/#more-1522',
        'div',
        {'class': 'blog-post-excerpt'})

    for counter, band_event in enumerate(duffys.events_info[0].find_all('ul')[0].find_all('li')):

        duffys.add_event(counter, {
            EventProperties.DATE: band_event.text.split('>')[0][:-3] + f" {now.strftime('%B')} {now.year}",
            EventProperties.TIME: band_event.text.split('–')[-1],
            EventProperties.ARTIST_NAME: str(str(band_event.text.split('>')[-1]).split('–')[0]),
            EventProperties.LOCATION: "Duffy's Pub",
            EventProperties.PRICE: '-'
        })

    return duffys.get_events()


def get_gibneys_events():
    """
    Creates an instance of EventHub for gibneys pub and fills with information on events along with
    an id number. In order to get all the information, it must first scrape the url to the more detailed page
    for each of the events, THEN take the event properties

    :return: gibneys events with all the variables for the events
    :rtype: dict
    """

    gibneys = EventHub('https://www.ticketweb.ie/search?q=gibneys+malahide',
                       'div',
                       {'class': 'list-group search-result-list event theme-mod'})

    for counter, band_event in enumerate(gibneys.events_info[0].find_all('div', {
            'class': 'row list-group-item theme-separator-strokes'})):
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

            gibneys.add_event(counter, {
                EventProperties.DATE: f"{weekday_converter(event_weekday)} "
                                      f"{month_converter(event_month)}{rest_of_date}",
                EventProperties.TIME: new_band_event.events_info[0].find_all('h5', {
                    'class': 'info-content theme-content'})[0].text,
                EventProperties.ARTIST_NAME: new_band_event.html.find_all('span', {'class': 'big'})[0].text[8:-7],
                EventProperties.LOCATION: "Gibney's Pub",
                EventProperties.PRICE: '-'
            })

    return gibneys.get_events()
