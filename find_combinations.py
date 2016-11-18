#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import re
import datetime
from bisect import bisect, bisect_left
from collections import defaultdict


def parse_input(line):
    """
    Parse input line
    """
    column = line.split(',')
    source = column[0]
    if not re.match('^[A-Z]{3}$', source):
        sys.stderr.write('Line {0}: unexpected source format.\n'.format(line_number))
        return None
    destination = column[1]
    if not re.match('^[A-Z]{3}$', destination):
        sys.stderr.write('Line {0}: unexpected destination format.\n'.format(line_number))
        return None
    try:
        departure = datetime.datetime.strptime(column[2], "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        sys.stderr.write('Line {0}: unexpected departure format.\n'.format(line_number))
        return None
    try:
        arrival = datetime.datetime.strptime(column[3], "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        sys.stderr.write('Line {0}: unexpected arrival format.\n'.format(line_number))
        return None
    flight_number = column[4]
    if not re.match('^[A-Z0-9]{5}$', flight_number):
        sys.stderr.write('Line {0}: unexpected flight number format.\n'.format(line_number))
        return None
    price = column[5]
    if not re.match('^[0-9]{1,5}$', price):
        sys.stderr.write('Line {0}: unexpected price format.\n'.format(line_number))
        return None
    bags_allowed = column[6]
    if not re.match('^[0-9]{1}$', bags_allowed):
        sys.stderr.write('Line {0}: unexpected bags allowed format.\n'.format(line_number))
        return None
    bag_price = column[7][:-1]
    if not re.match('^[0-9]{1,5}$', bag_price):
        sys.stderr.write('Line {0}: unexpected bags price format.\n'.format(line_number))
        return None
    return Flight(source, destination, departure, arrival, flight_number, price,
                                    bags_allowed, bag_price)



class Flight:
    """
    Represents particular flight
    """
    def __init__(self, source, destination, departure, arrival,
                    flight_number, price, bags_allowed, bag_price):
        self._source = source
        self._destination = destination
        self._departure = departure
        self._arrival = arrival
        self._flight_number = flight_number
        self._price = int(price)
        self._bags_allowed = int(bags_allowed)
        self._bag_price = int(bag_price)

    def __repr__(self):
        data = [self._source, self._destination,
                self._departure.strftime('%Y-%m-%dT%H:%M:%S'),
                self._arrival.strftime('%Y-%m-%dT%H:%M:%S'),
                self._flight_number, str(self._price),
                str(self._bags_allowed), str(self._bag_price)]
        return ','.join(data)


class Itinerary:
    """
    Finds allowed itineraries
    """
    def __init__(self, flight):
        self.__min_connection_time = datetime.timedelta(hours=1)
        self.__max_connection_time = datetime.timedelta(hours=4)
        self.__flights = [flight]
        self.__source = flight._destination
        self.__time = flight._arrival
        self.__total_price = []
        for i in range(3):
            if i <= flight._bags_allowed:
                self.__total_price.append(flight._price + i*flight._bag_price)
            else:
                self.__total_price.append(None)
        self.__previous_path = [None, flight._source, flight._destination]
        self.__stack = []
        self.__find_connection()

    def __resume_itinerary(self):
        """
        Take last incomplete path from stack and set attributes
        """
        if self.__stack:
            itinerary = self.__stack.pop()
            self.__flights = itinerary[0]
            self.__previous_path = itinerary[1]
            self.__source = itinerary[2]
            self.__total_price = itinerary[3]
            self.__find_connection()

    def __find_connection(self):
        """
        Find connection
        """
        if len(self.__flights) > 1:
            self.__save_itinerary()
        flights = airports[self.__source]
        times = keys[self.__source]
        time_start = bisect_left(times, self.__time + self.__min_connection_time)
        time_stop = bisect(times, self.__time + self.__max_connection_time)
        connections = flights[time_start:time_stop]
        # No connecting flights found:
        if not connections:
            self.__resume_itinerary()
        # If there's at least one connecting flight:
        else:
            has_valid_connection = False
            for flight in connections:
                # Allowed connections (not ABAB):
                if (self.__previous_path[0], self.__previous_path[1]) != \
                            (self.__previous_path[2], flight._destination):
                    # Next allowed connection -> save uncomplete itinerary to stack:
                    if has_valid_connection:
                        self.__save_to_stack(flight)
                    # First allowed connection:
                    else:
                        first_allowed_flight = flight
                    has_valid_connection = True
            if has_valid_connection:
                self.__continue_itinerary(first_allowed_flight)
            # If only ABAB connections are found:
            if not has_valid_connection:
                self.__resume_itinerary()

    def __save_to_stack(self, flight):
        flights = self.__flights[:] + [flight]
        previous_path = self.__previous_path[1:] + [flight._destination]
        source = flight._destination
        total_price = []
        for i in range(3):
            if self.__total_price[i] != None and i <= flight._bags_allowed:
                total_price.append(self.__total_price[i] + flight._price +\
                                        i*flight._bag_price)
            else:
                total_price.append(None)
        self.__stack.append([flights, previous_path, source, total_price])

    def __continue_itinerary(self, flight):
        self.__flights.append(flight)
        self.__source = flight._destination
        self.__time = flight._arrival
        for i in range(3):
            if self.__total_price[i] != None and i <= flight._bags_allowed:
                self.__total_price[i] += flight._price + i*flight._bag_price
            else:
                self.__total_price[i] = None
        self.__previous_path = self.__previous_path[1:] + [flight._destination]
        self.__find_connection()

    def __save_itinerary(self):
        """
        Save current itinerary
        """
        first_flight = self.__flights[0]
        last_flight = self.__flights[-1]
        bag_price = []
        for i in range(2):
            if self.__total_price[i + 1] != None:
                bag_price.append(str(self.__total_price[i + 1]))
            else:
                bag_price.append('-')
        output = []
        for flight in self.__flights:
            output.append(flight._source)
        output = ['-'.join([f._source for f in self.__flights] + [last_flight._destination]),
                first_flight._departure.strftime('%Y-%m-%dT%H:%M:%S'),
                last_flight._arrival.strftime('%Y-%m-%dT%H:%M:%S'),
                '-'.join([f._flight_number for f in self.__flights]),
                str(self.__total_price[0]), bag_price[0], bag_price[1]]
        sys.stdout.write(','.join(output) + '\n')


### Read input and sort flights by source airport ###

airports = defaultdict(list)
with sys.stdin as Input:
    Input.readline()
    line_number = 1
    for line in Input:
        flight = parse_input(line)
        if isinstance(flight, Flight):
            airports[flight._source].append(flight)
        line_number += 1

### Sort flights by time of departure ###

keys = {}  # Precomputed list of keys -> flights' departure time
for airport in airports:
    airports[airport].sort(key=lambda x: x._departure)
    keys[airport] = [flight._departure for flight in airports[airport]]


### Print allowed itineraries ###
print ('itinerary,departure,arrival,flight_numbers,\
price_without_bag,price_with_1_bag,price_with_2_bags')

### Search all flights from all airports for allowed itineraries ###

itinerary = []
for airport in airports:
    for flight in airports[airport]:
        Itinerary(flight)
