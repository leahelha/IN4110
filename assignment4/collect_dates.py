"""
Task 2 (IN4110 only)

parsing dates from wikipedia
"""

from __future__ import annotations

import re
import numpy as np

# create array with all names of months
month_names = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]


def get_date_patterns() -> tuple[str, str, str]:
    """Return strings containing regex pattern for year, month, day
    arguments:
        None
    return:
        year, month, day (tuple): Containing regular expression patterns for each field
    """
    #Month names in regex
    Jan = r"\b[jJ]an(?:uary)?\b"
    Feb = r"\b[fF]eb(?:ruary)?\b"
    Mar = r"\b[mM]ar(?:ch)?\b"
    Apr = r"\b[aA]pr(?:il)?\b"
    May = r"\b[mM]ay\b"
    Jun = r"\b[jJ]un(?:e)?\b"
    Jul = r"\b[jJ]ul(?:y)?\b"
    Aug = r"\b[aA]ug(?:ust)?\b"
    Sep = r"\b[sS]ep(?:tember)?\b"
    Oct = r"\b[oO]ct(?:ober)?\b"
    Nov = r"\b[nN]ov(?:ember)?\b"
    Dec = r"\b[dD]ec(?:ember)?\b"

    
    iso_month_format = r"\b(?:0\d|1[0-2])\b"


    # Regex to capture days, months and years with numbers
    
    # year should accept a 4-digit number between at least 1000-2029
    year = r"\b(1\d{3}|20[01]\d|202[0-9])\b" #r"(?P<year>...)"
    
    # month should accept month names or month numbers
    month = rf"(?:{Jan}|{Feb}|{Mar}|{Apr}|{May}|{Jun}|{Jul}|{Aug}|{Sep}|{Oct}|{Nov}|{Dec}|{iso_month_format})" #r"(?P<month>...)"
   
   # day should be a number, which may or may not be zero-padded
    day = r"\b(0?[1-9]|[12]\d|3[01])\b"  #r"(?P<day>...)"



    return year, month, day





def convert_month(s: str) -> str:
    """Converts a string month to number (e.g. 'September' -> '09'.

    You don't need to use this function,
    but you may find it useful.

    arguments:
        month_name (str) : month name
    returns:
        month_number (str) : month number as zero-padded string
    """
    
    # If already digit do nothing
    if s.isdigit():
        return s

    # Convert to number as string
    else:
        s = s.capitalize()
        s = s[:3]
        i = 0
        month_nr = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
        for name in month_names:
            i += 1
            if name[:3] == s:
                s = month_nr[i-1]
        return s




def zero_pad(n: str):
    """zero-pad a number string

    turns '2' into '02'

    You don't need to use this function,
    but you may find it useful.
    """
    day = int(n)

    nr_list = ['01', '02', '03', '04', '05', '06', '07', '08', '09']

    if day<10 and day not in nr_list:
        day = nr_list[day-1]
    
    return day


def find_dates(text: str, output: str | None = None) -> list:
    """Finds all dates in a text using reg ex

    arguments:
        text (string): A string containing html text from a website
        output (str, Optional) : The file to write the output to if wanted
    return:
        results (List): A list with all the dates found
    """
    
    year, month, day = get_date_patterns()

    # Date on format YYYY/MM/DD - ISO
    # e.g. 2007-05-31
    ISO = rf"({year}-{month}-{day})"

    # Date on format DD/MM/YYYY
    # e.g. 31 May 2007
    DMY = rf"({day}\s{month}\s{year})"

    # Date on format MM/DD/YYYY
    # e.g. May 31, 2007
    MDY = rf"({month}\s{day},?\s{year})"

    # Date on format YYYY/MM/DD
    # e.g. 2007 May 31
    YMD = rf"({year}\s{month}\s{day})"

    # list with all supported formats
    formats = [ISO, DMY, MDY, YMD]
    dates = []

    # Sorting the matches in the order they appear in the text

    # List to store matches in correct position
    match_pos = []

    # Iterate through each format and capture matches with their positions
    for form in formats:
        match_iter = re.finditer(form, text, flags=re.IGNORECASE)

        for match in match_iter:
            match_pos.append((match.group(0), match.start()))

    # Sort matches based on their positions
    match_pos.sort(key=lambda x: x[1])
    
    # Iterate through each match and match it again with correct format
    for match in match_pos:
        for form in formats:
            match = str(match)
            
            matching = re.findall(form, match, flags=re.IGNORECASE)
            
            if form == ISO:
                if len(matching)==1:
                    #print(f'ISO: {matching[0][0]}')
                    full_format = matching[0][0]
                    Y, M, D = full_format.split('-')

            if form == DMY:
                if len(matching)==1:
                    #print(f'DMY: {matching[0][0]}')
                    full_format = matching[0][0]
                    D, M, Y = full_format.split()
                
            if form == MDY:
                if len(matching)==1:
                    #print(f'MDY: {matching[0][0]}')
                    full_format = matching[0][0]
                    M, D, Y = full_format.split()
                    if ',' in D:
                        D = D[:-1]
                        
                    #print(M, D, Y)

            if form == YMD:
                if len(matching)==1:
                    #print(f'YMD: {matching[0][0]}')
                    full_format = matching[0][0]
                    Y, M, D = full_format.split()

        
        M = convert_month(M)
        D = zero_pad(D)

        dates.append(f'{Y}/{M}/{D}')
            
    

    
    
    # print('LOOP IS DONE \n')
    # print(text)
    # print(f'DATE: {dates}')

    # Write to file if wanted
    
    if output:
        with open(output, 'w') as outfile:
            for date in dates:
                outfile.write(f'{date} \n')

    # Return dates in ISO format
    return dates

# text = "2020-10-01, October 02, 2020, 2020 October 03 lala 04 October 2020" #"04 October 2020 1 september 2012  "

# run = find_dates(text)
