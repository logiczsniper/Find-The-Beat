"""Uses the functions in scrapers.py

Returns the relevant data(the data for today or in a few days)
"""


from datetime import datetime
from scrapers import get_duffys_events
from scrapers import get_gibneys_events
from scrapers import get_old_school_house_events


def main():
    """
    Use the above functions to print to output.txt the relevant(by location and time) events and their details

    :return: dictionaries full of information on upcoming events
    :rtype: list
    """

    now = datetime.now()
    weekday = now.strftime("%A").lower()

    gibneys_events = get_gibneys_events()
    duffys_events = get_duffys_events()
    old_school_house_events = get_old_school_house_events()
    all_upcoming_events = []

    for counter in range(len(gibneys_events)+2):

        try:
            if weekday in gibneys_events.get(str(counter)).get('Date').lower():
                all_upcoming_events.append(gibneys_events.get(str(counter)))
        except AttributeError:
            continue

    for counter in range(len(duffys_events)+2):

        try:

            if weekday == duffys_events.get(str(counter)).get('Date').lower()[0:-2]:
                if now.day == int(duffys_events.get(str(counter)).get('Date').lower()[-2:]):
                    all_upcoming_events.append(duffys_events.get(str(counter)))
        except AttributeError:
            continue

    for counter in range(len(old_school_house_events)+2):

        try:
            if old_school_house_events.get(str(counter)).get('Date').lower() == weekday + f" {now.day}":
                all_upcoming_events.append(old_school_house_events.get(str(counter)))
        except AttributeError:
            continue

    return all_upcoming_events


if __name__ == '__main__':
    main()
