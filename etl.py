import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    Description: This function is responsible for reading the JSON file in the given directory as a dataframe,
    and then inserting the first record of the song data and artist data to the songs and artists tables respectively.

    Arguments:
        cur: the cursor object.
        filepath: log data or song data file path.

    Returns:
        None
    """
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = df[['song_id', 'title', 'artist_id', 'year', 'duration']].values[0].tolist()
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']].values[0].tolist()
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    Description: This function is responsible for reading the JSON file in the given directory as a dataframe, filtering the dataframe to include only
    the records matching the NextSong page value, creating different time granurality features from the timestamp feature
    and then inserting and loading the relevant dataframe features into their corresponding tables such as songplay and users tables.

    Arguments:
        cur: the cursor object.
        filepath: log data or song data file path.

    Returns:
        None
    """
    
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df['page'] == 'NextSong']

    # convert timestamp column to datetime
    df['ts'] = pd.to_datetime(df['ts'], unit='ms')
    t = df
    t['hour'] = t['ts'].dt.hour
    t['day'] = t['ts'].dt.day
    t['week'] = t['ts'].dt.week
    t['weekday_name'] = t['ts'].dt.weekday_name
    t['month'] = t['ts'].dt.month
    t['year'] = t['ts'].dt.year
    
    # insert time data records
    time_data = ('ts', 'hour', 'day', 'week', 'month', 'year', 'weekday_name')
    column_labels = ('start_time', 'hour', 'day', 'week', 'month', 'year', 'weekday')
    time_df = t[['ts', 'hour', 'day', 'week', 'month', 'year', 'weekday_name']]

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (row.ts, row.userId, row.level, songid, artistid, row.itemInSession, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)



def process_data(cur, conn, filepath, func):
    """
    Description: This function is responsible for looping over all the JSON files in the data directories, calculating the total number of files found
    and applying the func function to all the files listed for the transformation and database insetion purposes.

    Arguments:
        cur: the cursor object.
        conn: connection to the database.
        filepath: log data or song data file path.
        func: function that transforms the data and inserts it into the database.

    Returns:
        None
    """
    
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()