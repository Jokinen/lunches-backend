# -*- coding: utf-8 -*-

import logging
from pymongo import MongoClient
import os
import pprint
from tzlocal import get_localzone
from datetime import datetime, timedelta


class DB_manager(object):

    def __init__(self):
        self.logger = logging.getLogger(" {0}".format(__name__))

    def init_db(self):
        mongo_db_url = os.environ.get('OPENSHIFT_MONGODB_DB_URL')

        if mongo_db_url:
            self.client = MongoClient(mongo_db_url)
        else:
            self.client = MongoClient('localhost', 27017)

        self.db = self.client.safkat
        self.logger.debug('mongodb connection opened')

    def close_db(self):
        self.client.close()
        self.logger.debug('mongodb connection closed')

    def handle_data(self, data):
        self.logger.debug(data)
        parser_info = {
            "parser_version": data["parser_version"],
            "parser_name": data["parser_name"].lower(),
            "parse_date": data["parse_date"]
        }
        restaurants = data['restaurants']
        self.insert_or_update_days(restaurants)

    def insert_or_update_days(self, restaurants):
        restaurants_dict = self.todict(restaurants)

        weekday = datetime.now().weekday()

        off_from_first_day_of_week = 6 - (6 - weekday)
        first_day_of_week = datetime.now() - timedelta(off_from_first_day_of_week)

        # The menus get updated during Sundays so we need to check that we are
        # not parsing an upcoming week; if we are, then set first_day_of_week
        # forwards by seven days
        current_weeknumber = int(first_day_of_week.strftime("%W"))
        # There's no week 0 in the system the restaurants use to display the
        # number for the current week
        if current_weeknumber == 0:
            current_weeknumber = 1

        week_number_from_source = restaurants_dict[0]['foodlist_date']['week_number']

        # Check whether weeknumber received from the source is ahead.
        # Handle the special during the change of the year when the weeknumber
        # received from the source is smaller. Expression
        # 'current_weeknumber >= 52' is used because the last week of the year
        # might be 52 or 53 depending on the system
        print(week_number_from_source)

        if week_number_from_source > current_weeknumber or (week_number_from_source == 1) and (current_weeknumber >= 52):
            first_day_of_week += timedelta(7)

        # timezone aware implementation
        # day_difference = timedelta(off_from_first_day_of_week)
        # local_tz = get_localzone()
        # now = datetime.now(local_tz)
        # day_ago = local_tz.normalize(now - day_difference)
        # naive = now.replace(tzinfo=None) - day_difference
        # first_day_of_week = local_tz.localize(naive, is_dst=None)

        pp = pprint.PrettyPrinter(indent=2)

        # Create a dictionary which represent the days belonging in the current
        # week.
        days = {}
        for i in range(7):
            this_date = first_day_of_week + timedelta(i)

            week_number = this_date.strftime("%W")
            if week_number == "00":
                week_number = "01"

            day = {
                'year': this_date.year,
                'month': this_date.month,
                'day': this_date.day,
                'week_number': week_number,
                'weekday': this_date.weekday(),
                'restaurants': []
            }

            days[i] = day

        # The received dict is of form:
        # {
        #   'restaurant_info': { ... }
        #   'weekly_foods': {
        #       '0': {
        #           'weekly_foods': [ ...foods ]
        #       }
        #   }
        # }
        # In this loop we go over the 'weekly_foods' array and create a new
        # dictionary whic consists of 'restaurant_info' with and extra field
        # of 'food_list' which in turn contains the food for one particular
        # date. After that we append that new dictionary in the correct 'day'
        # dictionary's (in days array) 'restaurants' field.
        for index, restaurant_dirty in enumerate(restaurants_dict):
            if type(restaurant_dirty['weekly_foods']) is list:
                continue

            for week_day_number, week_day in restaurant_dirty['weekly_foods'].items():
                restaurant = restaurant_dirty['restaurant_info'].copy()
                restaurant['food_list'] = week_day['daily_foods']
                days[int(week_day_number)]['restaurants']\
                    .append(restaurant)

        # Perform an insert operation on all the members of 'days' array
        for weekday_number, day in days.items():
            # Use these parameters to try and determine whether info for the
            # current day is already present.
            searched_day = {
                'year': day['year'],
                'month': day['month'],
                'day': day['day']
            }
            self.db.days.update(searched_day, day, upsert=True)

    def update_restaurant(self, restaurant):
        r_id = restaurant["restaurant_info"]["id"]
        chain = restaurant["restaurant_info"]["chain"]
        week = restaurant["foodlist_date"]["week_number"]
        year = restaurant["foodlist_date"]["year"]

        # restaurant foodlist
        searched_foodlist = {
            "foodlist_info.id": r_id,
            "foodlist_chain": chain,
            "foodlist_info.week_number": week,
            "foodlist_info.year": year
        }
        foodlist = {
            "foodlist_info": {
                "id": r_id,
                "chain": chain,
                "week_number": week,
                "year": year
            },
            "weekly_foods": restaurant["weekly_foods"],
            "debug": restaurant["parser_info"]
        }

        # restaurant info
        searched_info = {
            "restaurant_info.id": r_id
        }
        info = {
            "restaurant_info": restaurant["restaurant_info"],
            "debug": restaurant["parser_info"]
        }

        self.db.foods.update(searched_foodlist, foodlist, upsert=True)
        self.db.info.update(searched_info, info, upsert=True)

    def update_parser_version(self, version):
        self.db.parser.save({"version": version})

    def todict(self, obj, classkey=None):
        if isinstance(obj, dict):
            data = {}
            for (k, v) in obj.items():
                data[k] = self.todict(v, classkey)
            return data
        elif hasattr(obj, "_ast"):
            return self.todict(obj._ast())
        elif hasattr(obj, "__iter__"):
            return [self.todict(v, classkey) for v in obj]
        elif hasattr(obj, "__dict__"):
            data = dict(
                [(key, self.todict(value, classkey))
                 for key, value in obj.__dict__.iteritems()
                    if not callable(value) and not key.startswith('_')]
            )
            if classkey is not None and hasattr(obj, "__class__"):
                data[classkey] = obj.__class__.__name__
            return data
        else:
            return obj
