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
        self.event_info = []
        self.all_events_info = []

    def add_data_dict(self, data_dict):
        """
        Add to the events dictionary for the location

        :param data_dict: date, time, and price of the event
        :type: dict
        """
        self.event_info.append(data_dict)

        try:
            if data_dict['venue_info']:
                self.all_events_info.append(self.event_info)
                self.event_info = []
        except KeyError:
            pass

    def get_events(self):
        """
        Makes the EventHub's events dictionary available

        :return: the EventHub's events and their details
        :rtype: dict
        """
        return self.all_events_info
