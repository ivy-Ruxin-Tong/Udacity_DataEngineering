import configparser
from datetime import datetime
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col
from pyspark.sql.functions import year, month, dayofmonth, hour, weekofyear, date_format


config = configparser.ConfigParser()
config.read('dl.cfg')

os.environ['AWS_ACCESS_KEY_ID']=config['AWS_ACCESS_KEY_ID']
os.environ['AWS_SECRET_ACCESS_KEY']=config['AWS_SECRET_ACCESS_KEY']


def create_spark_session():
    spark = SparkSession \
        .builder \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
        .getOrCreate()
    return spark


def process_song_data(spark, input_data, output_data):
    # get filepath to song data file
    song_data =  input_data + 'song_data/*/*/*/*.json'
    
    # read song data file
    df = spark.read.json(song_data)

    # extract columns to create songs table
    songs_table = df.createOrReplaceTempView("song_data_table")
    
    songs_table = spark.sql("""
                            SELECT song_id, 
                            title,
                            artist_id,
                            year,
                            duration
                            FROM song_data_table 
                            WHERE song_id IS NOT NULL
                        """)
    
    # write songs table to parquet files partitioned by year and artist
    songs_table.write.mode('overwrite').partitionBy("year", "artist_id").parquet(output_data+'songs_table/') 

    # extract columns to create artists table
        artists_table = spark.sql("""
                                SELECT DISTINCT artist_id, 
                                artist_name,
                                artist_location,
                                artist_latitude,
                                artist_longitude
                                FROM song_data_table 
                                WHERE artist_id IS NOT NULL
                            """)
    
    # write artists table to parquet files
    artists_table.write.mode('overwrite').parquet(output_data+'artists_table/')


def process_log_data(spark, input_data, output_data):
    # get filepath to log data file
    log_data = input_data + 'log_data/*.json'

    # read log data file
    df = spark.read.json(log_data)
    
    # filter by actions for song plays
    df = df.filter(df.page == 'NextSong')

    # extract columns for users table    
    df.createOrReplaceTempView("log_data_table")
    
    # write users table to parquet files
    users_table = spark.sql("""
                            SELECT DISTINCT userId as user_id, 
                            firstName as first_name,
                            lastName as last_name,
                            gender as gender,
                            level as level
                            FROM log_data_table 
                            WHERE userId IS NOT NULL
                        """)
    users_table.write.mode('overwrite').parquet(output_data+'users_table/')

    # extract columns to create time table
    time_table = spark.sql("""
                            SELECT 
                            start_time_sub as start_time,
                            hour(start_time_sub) as hour,
                            dayofmonth(start_time_sub) as day,
                            weekofyear(start_time_sub) as week,
                            month(start_time_sub) as month,
                            year(start_time_sub) as year,
                            dayofweek(start_time_sub) as weekday
                            FROM
                            (SELECT to_timestamp(ts/1000) as start_time_sub
                            FROM log_data_table
                            WHERE ts IS NOT NULL
                            ) t
                        """)
    
    # write time table to parquet files partitioned by year and month
    time_table.write.mode('overwrite').partitionBy("year", "month").parquet(output_data+'time_table/')

    # read in song data to use for songplays table
    song_df = spark.read.parquet(output_data+'songs_table/')

    # extract columns from joined song and log datasets to create songplays table 
    songplays_table =  spark.sql("""
                                SELECT monotonically_increasing_id() as songplay_id,
                                to_timestamp(l.ts/1000) as start_time,
                                month(to_timestamp(l.ts/1000)) as month,
                                year(to_timestamp(l.ts/1000)) as year,
                                l.userId as user_id,
                                l.level as level,
                                s.song_id as song_id,
                                s.artist_id as artist_id,
                                l.sessionId as session_id,
                                l.location as location,
                                l.userAgent as user_agent
                                FROM log_data_table l
                                JOIN song_data_table s on l.artist = s.artist_name and l.song = s.title
                            """)


    # write songplays table to parquet files partitioned by year and month
    songplays_table.write.mode('overwrite').partitionBy("year", "month").parquet(output_data+'songplays_table/')


def main():
    spark = create_spark_session()
    input_data = "s3a://udacity-dend/"
    output_data = "s3a://udacity-dend/dloutput/"
    
    process_song_data(spark, input_data, output_data)    
    process_log_data(spark, input_data, output_data)


if __name__ == "__main__":
    main()
