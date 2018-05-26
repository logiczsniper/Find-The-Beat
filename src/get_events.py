"""Uses the functions in the scrapers.py files

Returns the relevant data(the data for today and all foreseeable events)
"""


from datetime import datetime
from scrapers_malahide import get_duffys_events
from scrapers_malahide import get_gibneys_events
from scrapers_swords import get_old_school_house_events
from scrapers_swords import get_theestuary_events


now = datetime.now()
weekday = now.strftime("%A")


def locate_month_string(split_date_list):
    """
    Takes the split list of an events date and locates the month as a string. Returns this value.

    :param split_date_list: the event date property.split(' ') to form a list
    :type: list

    :return: the string value of the month
    :rtype: str

    :return: upon not successfully finding the day value, return '0'
    :rtype: str
    """

    for counter, value in enumerate(split_date_list):

        if counter == 0:
            continue

        try:
            if int(value):
                continue
        except ValueError:
            return value.lower()


def locate_day_number(split_date_list):
    """
    Takes the split list of an events date and locates the day number. Returns this value.

    :param split_date_list: the event date property.split(' ') to form a list
    :type: list

    :return: the int value of the day
    :rtype: int

    :return: upon not successfully finding the day value, return 0
    :rtype: int
    """

    for value in split_date_list:

        try:
            if not int(value) == now.year:
                return int(value)
            else:
                return 0
        except ValueError:
            continue


def edit_date_status(events_list):
    """
    Takes a certain venue's lists and edits their date status property to define it as future or today or past.

    :param events_list: list of all events in a certain venue with 'event_date_status' set to 'None'
    :type: list

    :return new_all_events: dictionaries full of information on all events with updated 'event_date_status'
    :rtype: list
    """
    new_all_events = []

    for data_dict_list in events_list:

        date_of_event = data_dict_list[0].get('event_info').get('event_date')
        if data_dict_list not in new_all_events:

            try:
                if weekday in date_of_event and str(now.day) in date_of_event[:-4]:
                    data_dict_list[0].get('event_info')['event_date_status'] = 'today'
                elif locate_day_number(date_of_event.split(' ')) != 0 \
                        and now.day > locate_day_number(date_of_event.split(' ')) \
                        and now.strftime("%B").lower() in locate_month_string(date_of_event.split(' ')):
                    data_dict_list[0].get('event_info')['event_date_status'] = 'past'
                else:
                    data_dict_list[0].get('event_info')['event_date_status'] = 'future'
            except ValueError:
                pass

            new_all_events.append(data_dict_list)

    return new_all_events


def get_all_events():
    """
    Uses the scraping functions to return a list of all events with proper 'event_date_status' properties

    :return all_events: dictionaries full of information on all events
    :rtype: list
    """

    gibneys_events = get_gibneys_events()
    duffys_events = get_duffys_events()
    old_school_house_events = get_old_school_house_events()
    theestuary_events = get_theestuary_events()
    all_events = []

    for event_list in [duffys_events, gibneys_events, old_school_house_events, theestuary_events]:

        try:
            if event_list == duffys_events:
                new_duffys_list = edit_date_status(duffys_events)
                all_events.extend(new_duffys_list)

            elif event_list == gibneys_events:
                new_gibneys_list = edit_date_status(gibneys_events)
                all_events.extend(new_gibneys_list)

            elif event_list == old_school_house_events:
                new_old_school_house_list = edit_date_status(old_school_house_events)
                all_events.extend(new_old_school_house_list)

            elif event_list == theestuary_events:
                new_theestuary_list = edit_date_status(theestuary_events)
                all_events.extend(new_theestuary_list)

        except AttributeError:
            continue

    return all_events
