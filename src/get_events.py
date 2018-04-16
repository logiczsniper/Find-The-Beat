"""Uses the functions in the scrapers.py files

Returns the relevant data(the data for today and all foreseeable events)
"""


from datetime import datetime
from eventproperties import EventProperties
from scrapers_malahide import get_duffys_events
from scrapers_malahide import get_gibneys_events
from scrapers_swords import get_old_school_house_events


def get_all_events():
    """
    Uses the scraping functions to return two lists: one contains events that are happening today,
    the second contains all foreseeable events

    :return tonights_events: dictionaries full of information on tonights events
    :rtype: list

    :return all_upcoming_events: dictionaries full of information on all foreseeable events
    :rtype: list
    """

    now = datetime.now()
    weekday = now.strftime("%A").lower()

    gibneys_events = get_gibneys_events()
    duffys_events = get_duffys_events()
    old_school_house_events = get_old_school_house_events()
    tonights_events = []
    all_upcoming_events = []

    all_event_lists = [old_school_house_events, duffys_events, gibneys_events]

    for event_list in all_event_lists:

        for counter in range(len(event_list)+2):

            try:
                if event_list == gibneys_events:
                    all_upcoming_events.append(gibneys_events.get(str(counter)))
                    if weekday in gibneys_events.get(str(counter)).get(EventProperties.DATE).lower():
                        tonights_events.append(gibneys_events.get(str(counter)))

                if event_list == duffys_events:
                    all_upcoming_events.append(duffys_events.get(str(counter)))
                    if weekday in duffys_events.get(str(counter)).get(EventProperties.DATE).lower():
                        if str(now.day) in duffys_events.get(str(counter)).get(EventProperties.DATE).lower():
                            tonights_events.append(duffys_events.get(str(counter)))

                if event_list == old_school_house_events:
                    all_upcoming_events.append(old_school_house_events.get(str(counter)))
                    if old_school_house_events.get(str(counter)).get(EventProperties.DATE).lower() == weekday + \
                            f" {now.strftime('%B')} {now.day} {now.year}":
                        tonights_events.append(old_school_house_events.get(str(counter)))

            except AttributeError:
                continue

    return [tonights_events, all_upcoming_events]
