# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS SONGPLAYS"
user_table_drop = "DROP TABLE IF EXISTS USERS"
song_table_drop = "DROP TABLE IF EXISTS SONGS"
artist_table_drop = "DROP TABLE IF EXISTS ARTISTS"
time_table_drop = "DROP TABLE IF EXISTS TIME"

# CREATE TABLES

songplay_table_create = ("""

CREATE TABLE IF NOT EXISTS SONGPLAYS
(
SONGPLAY_ID SERIAL PRIMARY KEY,
START_TIME TIMESTAMP REFERENCES TIME(START_TIME),
USER_ID INTEGER REFERENCES USERS(USER_ID),
LEVEL VARCHAR,
SONG_ID VARCHAR REFERENCES SONGS(SONG_ID),
ARTIST_ID VARCHAR REFERENCES ARTISTS(ARTIST_ID),
SESSION_ID INTEGER,
LOCATION VARCHAR,
USER_AGENT VARCHAR
);
""")


user_table_create = ("""

CREATE TABLE IF NOT EXISTS USERS
(
USER_ID INTEGER PRIMARY KEY,
FIRST_NAME VARCHAR NOT NULL,
LAST_NAME VARCHAR NOT NULL,
GENDER CHAR(1),
LEVEL VARCHAR
);
""")

song_table_create = ("""

CREATE TABLE IF NOT EXISTS SONGS
(
SONG_ID VARCHAR PRIMARY KEY,
TITLE VARCHAR NOT NULL,
ARTIST_ID VARCHAR NOT NULL,
YEAR INTEGER CHECK (YEAR>=0),
DURATION DECIMAL NOT NULL
);
""")

time_table_create  = ("""

CREATE TABLE IF NOT EXISTS TIME
(
START_TIME TIMESTAMP PRIMARY KEY,
HOUR INTEGER NOT NULL CHECK (HOUR>=0),
DAY INTEGER NOT NULL CHECK (DAY>=0),
WEEK INTEGER NOT NULL CHECK (WEEK>=0),
MONTH INTEGER NOT NULL CHECK (MONTH>=0 AND MONTH <= 12),
YEAR INTEGER NOT NULL CHECK (YEAR>=0),
WEEKDAY INTEGER NOT NULL
);
""")

artist_table_create = ("""

CREATE TABLE IF NOT EXISTS ARTISTS 
(
ARTIST_ID VARCHAR PRIMARY KEY,
NAME VARCHAR NOT NULL,
LOCATION VARCHAR,
LATITUDE DECIMAL,
LOGITUDE DECIMAL
);
""")



# INSERT RECORDS

songplay_table_insert = ("""

INSERT INTO SONGPLAYS (
    START_TIME,
    USER_ID,
    LEVEL,
    SONG_ID,
    ARTIST_ID,
    SESSION_ID, 
    LOCATION,
    USER_AGENT
)


VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
ON CONFLICT (SONGPLAY_ID)
DO NOTHING;

""")

#  level might change, so we hsould update the level
user_table_insert = ("""

INSERT INTO USERS VALUES
(%s,%s,%s,%s,%s)
ON CONFLICT (USER_ID)
DO UPDATE
    SET LEVEL = EXCLUDED.LEVEL;
    
""")

song_table_insert = ("""

INSERT INTO SONGS VALUES
(%s,%s,%s,%s,%s)
ON CONFLICT (SONG_ID)
DO NOTHING;
    
""")

artist_table_insert = ("""

INSERT INTO ARTISTS VALUES
(%s,%s,%s,%s,%s)
ON CONFLICT (ARTIST_ID)
DO NOTHING;
    
""")


time_table_insert = ("""

INSERT INTO TIME VALUES
(%s,%s,%s,%s,%s,%s,%s)
ON CONFLICT (START_TIME)
DO NOTHING
    
""")

# FIND SONGS
# song_select query in sql_queries.py to find the song ID and artist ID based on the title, artist name, and duration of a song.

song_select = ("""
select s.song_id, s.artist_id
from songs s
join artists a
on s.artist_id = a.artist_id
where s.title = %s
and a.name = %s
and s.duration = %s
""")

# QUERY LISTS

# create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
# create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create]
create_table_queries = [time_table_create,user_table_create,artist_table_create,song_table_create,songplay_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]