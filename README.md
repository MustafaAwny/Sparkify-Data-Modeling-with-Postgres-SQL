# Data Modeling with Postgres SQL

This project is part of Udacity Data Engineer Nanodegree

## Introduction

A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs users are listening to. Currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

They'd like a data engineer to create a Postgres database with tables designed to optimize queries on song play analysis. The main goal of this project is to create a database schema and ETL pipeline for this analysis. After that, we need to test the database and ETL pipeline by running given queries by the analytics team from Sparkify and compare the results with the expected ones.

## Data

**Song Dataset**: it is in the format of JSON files and each file attributes are: num_songs, artist_id, artist_latitude, artist_longitude, artist_location, artist_name, song_id, title, duration, and year.

**Log Dataset**: it is in the format of JSON files and each file attributes are: artist, auth, firstName, gender, itemInSession, lastName, length, level, location, method, page, registration, sessionId, song, status, ts, userAgent, and userId.

## Data Model

The star schema data model was used with 1 fact table and 4 dimensional tables. 

### Fact Table: songplays
Records in log data associated with song plays i.e. records with page NextSong
songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent.

### Dimension Tables
1. **users**: users in the app.
Attributes: user_id, first_name, last_name, gender, level.

2. **songs**: songs in music database.
Attributes: song_id, title, artist_id, year, duration.

3. **artists**: artists in music database
Attributes: artist_id, name, location, latitude, longitude

4. **time**: timestamps of records in songplays broken down into specific units.
Attributes: start_time, hour, day, week, month, year, weekday.

## Project Structure

### sql_queries.py

This file contain the create, insert and drop statements for all the 5 tables.

### create_tables.py

This file imports the **sql_queries** file, establish the database connection and run the queries in **sql_queries** file.

### etl.ipynb

As the name implies, this file extracts, loads and transforms the data in the JSON files by first connecting to the database, processing and transforming both the datasets, running simple queries and closing the connection.

### etl.py

A python file wrapper for the **etl.ipynb**.

### test.ipynb

This file contains different test units for each phase of the project provided by Udacity.


## How to run the project

First you need to have Python3, Jupyter Notebook and Postgres SQL database installed on your machine or VM. After that you need to run the **create_tables** file by opening your terminal, navigating to the file directory and running `` python3 create_tables.py `` or by simply running the command `` !python create_tables.py `` in any of the notebooks. Then, you can follow the same procedures to run the etl.py file. Finally, you can verify the results by running the sanity test scetion cells in the **test.ipynb**.