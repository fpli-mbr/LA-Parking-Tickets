"""
    "Exploring Los Angeles Parking Citations Data"

    Data source: City of Los Angeles Open Data Portal
    https://data.lacity.org/A-Well-Run-City/Parking-Citations/wjz9-h9np

    Nathan @nate_somewhere

    Warning:

    The dataset downloaded has 9.5 million plus rows
    and takes several minutes to download.

    By default, a smaller dataset is in the exercises/data folder that you should
    use for development until you are ready to run the whole batch.

    Class notes:

    Python3 required, python2 not guaranteed to work completely
    Internet connection required
    Text editor required
"""

import matplotlib.pyplot as plt
import numpy as np
import time
import csv
import os
import functools
from operator import itemgetter
from collections import OrderedDict
#import pdb
#pdb.set_trace()
from datetime import datetime

try:
    # python3 functionality
    from urllib.request import urlretrieve
except ImportError as ex:
    from urllib import urlretrieve
    # python2 compability

CURRENT_DIR_PATH = os.path.dirname(__file__)

def file_downloader(url, filename):
    """Downloads and names a file given a filename and download_url"""

    if not os.path.isfile(filename):
        urlretrieve(url, filename)
        print("File: %s downloaded" % filename)
    if os.path.isfile(filename):
        print("File: %s present and ready to go!" % filename)

    return os.path.abspath(filename)

def open_file_list_loop(file_path, start, end):
    """Opens a file and returns the data"""
    data = []
    with open(file_path, "r", encoding="utf-8-sig") as csvfile:
        csv_file_data = csv.DictReader(csvfile)
        for row in csv_file_data:
            if filter_by_date_range(start, end, row) is True:
                data.append(row)
    return data

def open_file_filter_object(file_path, start, end):
    """Opens a file and returns the data"""
    # I first attempted to generate the filter object by opening the file using a With statement
    # This approach threw the following exception 'ValueError: I/O operation on closed file'
    csvfile = open(file_path, "r", encoding="utf-8-sig")
    csv_file_data = csv.DictReader(csvfile)
    my_func = functools.partial(filter_by_date_range, start, end)
    data = filter(my_func,csv_file_data)
    return data

def open_file_generator(file_path, start, end):
    """Opens a file and returns the data"""
    with open(file_path, "r", encoding="utf-8-sig") as csvfile:
        csv_file_data = csv.DictReader(csvfile)
        for row in csv_file_data:
            if filter_by_date_range(start, end, row) is True:
                yield row

def filter_by_date_range(start, end, citation_row):
    """Filters a citation by the issue date in a date range.
    Returns True or False if date falls in the range.
    """
    #Corresponds to "10/31/2018" format
    date_format = "%m/%d/%Y"

    # strptime is creating a datetime object
    date_start = datetime.strptime(start, date_format)
    date_end = datetime.strptime(end, date_format)

    try:
        citation_date_str = citation_row['Issue Date']
        citation_date_obj = datetime.strptime(citation_date_str, date_format)

        # Checks to see if the citation falls between the start and end date.
        if date_start <= citation_date_obj <= date_end:
            return True
        else:
            return False
    except:
        # except statement included in case the date is omitted or submitted with the wrong format
        return False

def calculate_total_by_citation(file_data, count_type='fine_amount'):
    '''Calculate either the total fine amount or number of citations for each citation type.
    type = 'fine_amount' calculates the total fine amount, type = 'number_count' calculates the number of citations'''
    # Store the fine amount format - key: violation description & value: fine_amount
    total_fine_by_citation = {}
    count_by_citation = {}
    # citation_row is a dictionary
    tot_sum = 0
    for citation_row in file_data:
        violation_description = citation_row["Violation Description"]
        try:
            fine_amount = int(citation_row["Fine amount"])
            tot_sum += fine_amount
        except:
            fine_amount = 0
        # If the violation_desciption doesn't exist, then add it
        if violation_description in total_fine_by_citation.keys():
            # Add fine_amount to the rolling total for the existing violation description
            total_fine_by_citation[violation_description] += fine_amount
            count_by_citation[violation_description] += 1
        else:
            total_fine_by_citation[violation_description] = fine_amount
            count_by_citation[violation_description] = 1

    if count_type == 'fine_amount':
        return total_fine_by_citation
    elif count_type == 'number_count':
        return count_by_citation
    else:
        return 'Error - type_count not appropriately specified.'

def count_total_fine(total_fine_by_citation):
    '''Using the total_fine_by_citation dictionary, calculate the overall total fine amount'''
    fine_total = 0
    for key, value in total_fine_by_citation.items():
        fine_total += value
    return fine_total

def count_total_citations(count_of_each_citation):
    '''Using the total_fine_by_citation dictionary, calculate the overall total fine amount'''
    citation_total = 0
    for key, value in count_of_each_citation.items():
        citation_total += value
    return citation_total

def plot(dictionary):
    #fig = plt.figure() # an empty figure with no axis
    #fig.suptitle('No axes on this figure') # Add a title so we know which it is
    #fig, ax_lst = plt.subplots(2,2) # a figure with a 2x2 grid of axes
    d = {}
    lst = list(dictionary.values())
    lst.sort(reverse=True)
    # Number of parking violations to include in bar plot
    num_of_entries = 5
    cutoff_value = lst[num_of_entries - 1]
    for key, value in dictionary.items():
        if value >= cutoff_value:
            d[key] = value
    l = OrderedDict(sorted(d.items(), key=itemgetter(1), reverse=True))
    plt.bar(l.keys(), l.values())
    plt.ylabel("Dollars Collected in Fines")
    plt.title("Top Five Parking Citations in Los Angeles, by Total Citation Amount")
    plt.show()

if __name__ == "__main__":
    url = "https://data.lacity.org/api/views/wjz9-h9np/rows.csv?accessType=DOWNLOAD"
    start_date = "1/1/2018"
    end_date = "12/31/2018"

    data_file_path = os.path.join(CURRENT_DIR_PATH, "la_parking_citations_full.csv")
    file_location = file_downloader(url, data_file_path)

    #file_data_filter = open_file_filter_object(file_location, start_date, end_date)
    #file_data_generator = open_file_generator(file_location, start_date, end_date)

    total_fine_by_citation = calculate_total_by_citation(open_file_generator(file_location, start_date, end_date))
    count_of_each_citation = calculate_total_by_citation(open_file_generator(file_location, start_date, end_date), count_type='number_count')
    total_fine = count_total_fine(total_fine_by_citation)
    total_citations = count_total_citations(count_of_each_citation)

    print('Total Fine', total_fine)
    print('Total Citation', total_citations)
    plot(total_fine_by_citation)
