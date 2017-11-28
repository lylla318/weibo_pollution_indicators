import pandas as pd
import re
import json
import io
import csv
import sys
from pprint import pprint
from collections import defaultdict
from bs4 import UnicodeDammit


class Parser:

    def __init__(self):

        #self.day_data = defaultdict(dict)
        #self.parse_sample_data()
        #self.checkin_records = self.parse_checkin_data()

        # Data structure for getting city name from a poiid.
        # Format: {poiid: citycode, poiid2, citycode2, ...}
        #self.poiid_to_city = self.parse_poiid_data()

        # Data structure for number of tweets in city, by day.
        # Format: {citycode: {day: tweet_count, day2: tweet_count ...}, citycode2 : {...} ...}
        #self.tweets_by_day = self.parse_tweet_numbers()

        # Data structure for air pollution by city, by day.
        # Format: {citycode: {day: pollution_stat, day2: pollution_stat2 ...}, citycode2 : {...} ...}
        #self.pollution_by_day = self.parse_pollution_data()

        # Data structure for city code to city name.
        # Format: {citycode: cityname, citycode2 : cityname2 ...}
        #self.code_to_city = self.get_city_name()

        # Data structure for tweet counts by week, by city
        # Format: {citycode: tweet_count, citycode2: tweet_count2}
        #self.tweets_by_year = self.get_yearly_tweets()

        # Data structure for tweet counts by week, by city
        # Format: {citycode: {week: tweet_count, week2: tweet_count2, ...}, citycode2: {...} ...}
        self.tweets_by_week = self.get_weekly_tweets()

        # Data structure for tweet counts by week, by city
        # Format: {citycode: {week: tweet_count, week2: tweet_count2, ...}, citycode2: {...} ...}
        self.pollution_by_year = self.get_yearly_pollution()

        # Data structure for tweet counts by week, by city
        # Format: {citycode: {week: tweet_count, week2: tweet_count2, ...}, citycode2: {...} ...}
        self.pollution_by_week = self.get_weekly_pollution()



    # Generate data structure for pollution values by year, by city.
    # Returns data structure with format: {citycode: pollution_value, citycode2: pollution_value2}
    def get_yearly_pollution(self):

        processed_data = {}

        data = json.load(open('data/pollution_by_city.json'))
        
        for citycode in data:
            tweet_count = 0
            for day in data[citycode]:
                tweet_count += data[citycode][day]
            processed_data[citycode] = tweet_count


        j = json.dumps(processed_data, indent=4)
        f = open('updated_data/tweet_totals.json', 'w')
        print >> f, j
        f.close()

        return processed_data


    # Generate data structure for pollution values by week, by city.
    # Returns data structure with format: {citycode: {week: pollution_value, week2: pollution_value2, ...}, citycode2: {...} ...}
    def get_weekly_pollution(self):

        processed_data = {}

        return processed_data


    # Generate data structure for tweet counts by year, by city.
    # Returns data structure with format: {citycode: tweet_count, citycode2: tweet_count2}
    def get_yearly_tweets(self):

        processed_data = {}

        data = json.load(open('data/media_by_city.json'))
        
        for citycode in data:
            tweet_count = 0
            for day in data[citycode]:
                tweet_count += data[citycode][day]
            processed_data[citycode] = tweet_count


        j = json.dumps(processed_data, indent=4)
        f = open('updated_data/tweet_totals.json', 'w')
        print >> f, j
        f.close()

        return processed_data



    # Generate data structure for tweet counts by week, by city.
    # Returns data structure with format: {citycode: {week: tweet_count, week2: tweet_count2, ...}, citycode2: {...} ...}
    def get_weekly_tweets(self):

        processed_data = {}

        return processed_data



    # Generate data structure for city code to city name.
    # Returns data structure with format: {citycode: cityname, citycode2 : cityname2 ...}
    def get_city_name(self):

        parsed_data = {}

        with open("china_cities.txt") as f:

            for line in f: 

                info = line.split(",")
                code = info[2].rstrip()
                city = info[1].rstrip()
                #parsed_data[code] = city
                parsed_data[code] = city

        return parsed_data




    # Generate data structure for number of tweets in city, by day.
    # Returns data structure with format: {citycode: {day: tweet_count, day2: tweet_count ...}, citycode2 : {...} ...}
    def parse_tweet_numbers(self):

        parsed_data = defaultdict(dict)
        checkin_records = "raw_data/all_checkinrecords.csv"
        
        csv.field_size_limit(sys.maxsize)

        with open(checkin_records, 'rU') as datafile:
            
            reader = csv.reader(datafile)

            COUNTER = 0

            for row in reader:

                data = re.split(r'\t+', row[0])
                date = data[2]
                poiid = data[0]

                try:
                    citycode = self.poiid_to_city[poiid]
                    if(citycode in parsed_data):
                        if(date in parsed_data[citycode]):
                            parsed_data[citycode][date] += 1
                        else:
                            parsed_data[citycode][date] = 1
                    else:
                        parsed_data[citycode] = {date:1}

                except:
                    print("City code does not exist.")

                COUNTER += 1
           
        j = json.dumps(parsed_data, indent=4)
        f = open('updated_data/media_by_city.json', 'w')
        print >> f, j
        f.close()

        print("Exiting parse tweet numbers.")

        return parsed_data



    # Generate data structure for air pollution by city, by day.
    # Returns data structure with format: {citycode: {day: pollution_stat, day2: pollution_stat2 ...}, citycode2 : {...} ...}
    def parse_pollution_data(self):
        parsed_data = defaultdict(dict)
        pollution_data = "raw_data/pollution_data.csv"

        csv.field_size_limit(sys.maxsize)

        with open(pollution_data, 'rU') as datafile:
            
            reader = csv.reader(datafile)

            for row in reader:

                citycode = row[0]
                date = row[1]
                pollution = row[20]

                if(citycode in parsed_data):
                    if(date in parsed_data[citycode]):
                        parsed_data[citycode] = pollution
                    else:
                        parsed_data[citycode][date] = pollution
                else:
                    parsed_data[citycode] = {date:pollution}

        j = json.dumps(parsed_data, indent=4)
        f = open('updated_data/pollution_by_city.json', 'w')
        print >> f, j
        f.close()

        print("Exiting parse pollution data.")

        return parsed_data


    def parse_poiid_data(self):

        parsed_data = defaultdict(dict)
        #poiid_locations = "raw_data/poiid_locations.csv"
        poiid_locations = "raw_data/poiid_locations_fixed.csv"

        csv.field_size_limit(sys.maxsize)

        with open(poiid_locations, 'rU') as datafile:
            
            reader = csv.reader(datafile)
            for row in reader:
                parsed_data[row[0]] = row[7]

        j = json.dumps(parsed_data, indent=4)
        f = open('updated_data/poiid_to_citycode.json', 'w')
        print >> f, j
        f.close()

        print("Exiting parse poiid data.")

        return parsed_data


    def parse_checkin_data(self):

        parsed_data = defaultdict(dict)
        checkin_records = "raw_data/all_checkinrecords.csv"

        csv.field_size_limit(sys.maxsize)

        with open(checkin_records, 'rU') as datafile:
            
            reader = csv.reader(datafile)
            for row in reader:
                
                data = re.split(r'\t+', row[0])
                date = data[2]
                poiid = data[0]

                if(date in parsed_data):
                    if(poiid in parsed_data[date]):
                        parsed_data[date][poiid]+=1
                    else:
                        parsed_data[date][poiid] = 1
                else:
                    parsed_data[date][poiid] = 1

        return parsed_data



    def parse_sample_data(self):

        parsed_data = defaultdict(dict)

        csvfile = "raw_data/all_checkinrecords_sample.csv"

        column_names = ["poiid","userid","date","time"]

        csv.field_size_limit(sys.maxsize)

        with open(csvfile, 'rU') as datafile:
            
            reader = csv.DictReader(datafile)
            for row in reader:

                if(parsed_data[row['date']]):
                    if(parsed_data[row['date']][row['poiid']]):
                        parsed_data[row['date']][row['poiid']]+=1
                    else:
                        parsed_data[row['date']][row['poiid']] = 1
                else:
                    parsed_data[row['date']][row['poiid']] = 1

        j = json.dumps(parsed_data, indent=4)
        f = open('updated_data/sample.json', 'w')
        print >> f, j
        f.close()

        return 0




if __name__ == '__main__':
    
    p = Parser();






