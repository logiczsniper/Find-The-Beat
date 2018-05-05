"""Reach the databases from the app

The function will be called so the app can reach the data(the events) in the databases
"""


import MySQLdb
from my_credentials import MyCredentials


def get_db_info():
    """
    Reaches the db tables. Iterates through the events of both today and future. For each event of each category,
    it finds the corresponding id venue and artist tables and appends these to one event info bundle (list).

    :return: one list containing two more lists, one for todays events, one for future events.
    :rtype: list
    """

    db = MySQLdb.connect(MyCredentials.DB_URL,
                         MyCredentials.USERNAME,
                         MyCredentials.PASSWORD, 'findthebeat', charset='utf8', port=3306)

    cursor = db.cursor()

    events_today = []
    events_future = []
    events_past = []

    for date_status in ['today', 'future', 'past']:

        cursor.execute(f"SELECT * FROM event WHERE event_date_status='{date_status}'")

        for event_listing in list(cursor.fetchall()):

            event_info_bundle = list()
            event_info_bundle.append(list(event_listing)[4:])
            cursor.execute("SELECT artist_name, facebook_url FROM artist WHERE artist_id=%s" % (event_listing[2]))
            event_info_bundle.append(list(cursor.fetchall()[0]))
            cursor.execute("""
            SELECT venue_name, venue_url, venue_address FROM venue WHERE venue_id=%s""" % (event_listing[1]))
            event_info_bundle.append(list(cursor.fetchall()[0]))

            if date_status == 'today':
                events_today.append(event_info_bundle)

            elif date_status == 'future':
                events_future.append(event_info_bundle)

            elif date_status == 'past':
                events_past.append(event_info_bundle)

    db.close()

    return [events_today, events_future, events_past]
