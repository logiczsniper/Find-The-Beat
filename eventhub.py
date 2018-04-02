"""A base class for each location that holds an event, eg, live music

I created this class in order to make the task of getting the html with requests, using BeautifulSoup, and
being able to filter through the page, trivial.
"""


from requests import get
from bs4 import BeautifulSoup


class EventHub:

    def __init__(self, url, repeated_element, repeated_ds):
        """
        Construct an EventHub object
        :param url: the url to the location's web page
        :type: str

        :param repeated_element: the html element of the page that contains the relevant data
        :type: str

        :param repeated_ds: the exact name, class, or id of the element with it's corresponding value
        :type: dict
        """

        self.url = url
        self.page = get(url)
        self.html = BeautifulSoup(self.page.content, 'html5lib')
        self.events_info = self.html.find_all(repeated_element, repeated_ds)
        self.events = {}

    def add_event(self, number, event_details):
        """
        Add to the events dictionary for the location
        :param number: the new id number to correspond with the event it labels
        :type: str

        :param event_details: date, time, artist_name, location and price of the event
        :type: dict
        """
        self.events[f'{number}'] = event_details

    def get_events(self):
        """
        Makes the EventHub's events dictionary available
        :return: the EventHub's events and their details
        :rtype: dict
        """
        return self.events
