"""Updates the database of events

Takes the events returned by get_events and updates the database with the new information
"""


import MySQLdb
from get_events import get_all_events
from my_credentials import MyCredentials


db = MySQLdb.connect(MyCredentials.DB_URL,
                     MyCredentials.USERNAME,
                     MyCredentials.PASSWORD, 'findthebeat', charset='utf8', port=3306)

cursor = db.cursor()

cursor.execute("""
DROP TABLE IF EXISTS event;
DROP TABLE IF EXISTS venue;
DROP TABLE IF EXISTS artist;

CREATE TABLE venue (
    venue_id INT(10) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    venue_name TINYTEXT,
    venue_url TINYTEXT,
    venue_address TINYTEXT
   );

CREATE TABLE artist (
    artist_id INT(10) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    artist_name TINYTEXT,
    facebook_url TINYTEXT
   );

CREATE TABLE event (
    event_id INT(10) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    venue_id INT(10) UNSIGNED,
    artist_id INT(10) UNSIGNED,
    event_date_status TINYTEXT,    
    event_date TINYTEXT,
    event_time TINYTEXT,
    event_price TINYTEXT,
    CONSTRAINT FOREIGN KEY (venue_id) REFERENCES venue (venue_id),
    CONSTRAINT FOREIGN KEY (artist_id) REFERENCES artist (artist_id)
   );
""")

for event_info_list in get_all_events():

    cursor.executemany("""
INSERT INTO venue(venue_name, venue_url, venue_address) VALUES (%s, %s, %s);
SET @venue_id = LAST_INSERT_ID();
""", [tuple(event_info_list[2]['venue_info'].values())])
    cursor.executemany("""
INSERT INTO artist(artist_name, facebook_url) VALUES (%s, %s);
SET @artist_id = LAST_INSERT_ID();
""", [tuple(event_info_list[1]['artist_info'].values())])
    cursor.executemany("""
INSERT INTO event(venue_id, artist_id, event_date_status, event_date, event_time, event_price) 
VALUES (@venue_id, @artist_id, %s, %s, %s, %s);
""", [tuple(event_info_list[0]['event_info'].values())])

db.commit()

db.close()
