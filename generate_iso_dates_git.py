#!/usr/bin/env python

# Script by Arcadia Falcone, arcadiafalcone at gmail
# Updated 2014-05-16

import re

def deriveYear(date_created):
# Identify year
    if re.search(year, date_created):
        iso_year_match = re.findall(year, date_created)
# Check if more than one year found
        if len(iso_year_match) > 1:
            evalError('Year error')
            return 'error'
        else:
            iso_year = iso_year_match[0]
# Handle Old Style/New Style split years
        if '/' in iso_year:
# Handle YYYY/YYYY and YYYY/YY as error
            if iso_year == date_created:
                evalError('Year error')
                return 'error'
            else:
                iso_year_osns = iso_year.split('/')
# Handle e.g. 1699/00 and 1609/0, or 1904/June, as error
                if re.match(zero, iso_year_osns[1]) \
                        or not iso_year_osns[1].isdigit():
                    evalError('Year error')
                    return 'error'
                else:
                    sub_digits = len(iso_year_osns[1])
                    iso_year = iso_year_osns[0][:4-sub_digits] + \
                        iso_year_osns[1]
# Check for right number of digits
        if len(iso_year) != 4:
            evalError('Year error')
            return 'error'
        else:
            return iso_year
# If no year value identified by regex
    else:
        iso_year = ''
        return iso_year

def deriveMonth(date_created):
# Handle month-only value
    if date_created in month_list:
        iso_month = month_list[date_created]
# Identify month and remove circa terms
    elif re.search(date_sep, date_created):
        date_terms = date_sep.split(date_created)
        date_terms_alpha = [t for t in date_terms \
                                if t.isalpha() and not re.match(circa, t)]
# Handle multiple text terms
        if len(date_terms_alpha) > 1:
            evalError('Month error')
            return 'error'
# Handle circa term + YYYY
        elif len(date_terms_alpha) == 0:
            iso_month = ''
            return iso_month
# Return month if present
        elif date_terms_alpha[0] in month_list:
            iso_month = month_list[date_terms_alpha[0]]
            return iso_month
# Handle non-month text term
        else:
            evalError('Month error')
            return 'error'
# If no month value identified
    else:
        iso_month = ''
        return iso_month

def deriveDay(date_created):
# Identify day
    if re.search(date_sep, date_created):
        date_terms = date_sep.split(date_created)
        date_terms_digit = [t for t in date_terms if t.isdigit() and len(t) < 4]
# Handle day not present
        if len(date_terms_digit) == 0:
            iso_day = ''
            return iso_day
# Handle multiple numbers of less than 4 digits
        elif len(date_terms_digit) > 1:
            evalError('Day or Year error')
            return 'error'
# Check that day is 31 or less
        elif int(date_terms_digit[0]) < 32:
            iso_day = date_terms_digit[0]
# Add leading zero if necessary
            if len(iso_day) == 1:
                iso_day = '0' + iso_day
            return iso_day
# Handle day with value greater than 31
        else:
            evalError('Day error')
            return 'error'
# If no day value identified
    else:
        iso_day = ''
        return iso_day

def evalError(error_type):
    line_out = line + '\t' + error_type + '\n'
    error_log.write(line_out)

def makeISODate(iso_year, iso_month, iso_day):
# Combine available data to generate ISO date
    if iso_year:
        if iso_year and iso_month and iso_day:
            iso_date = iso_year + '-' + iso_month + '-' + iso_day
        elif iso_year and iso_month:
            iso_date = iso_year + '-' + iso_month
        elif iso_year:
            iso_date = iso_year
        return iso_date
# Return error if year is not present
    else:
        evalError('Insufficient data to generate ISO date')
        return 'error'


### Variables

month_list = {'January':'01', 'February':'02', 'March':'03', 'April':'04', 
'May':'05', 'June':'06', 'July':'07', 'August':'08', 'September':'09', 
'October':'10', 'November':'11', 'December':'12'}

# Regex
day = re.compile(r'[\d]{1,2}')
year = re.compile(r'[\d]{4}/?[\d]{0,4}')
year_valid = re.compile(r'[\d]{4}]')
pipe = re.compile(r'\|')
date_sep = re.compile(r'[, ]+')
blank_line = re.compile(r'^$')
circa = re.compile(r'c(irc)?[a.]?')
zero = re.compile(r'0+')
alphanum = re.compile(r'(\d[A-Za-z])|([A-Za-z]\d)')

### Files
# Input file should be tab-delimited text with dates in second column;
# assumption is that first column will have record IDs.
# Output file will contain all data from each successfully processed record, 
# plus the ISO date.
# Error file will contain all data from each record generating an error, plus 
# an error message.

file_in = 'dates_in.txt'
file_out = 'dates_out.txt'
file_error = 'dates_errorlog.txt'

data_in = open(file_in, 'r')
data_out = open(file_out, 'w')
error_log = open(file_error, 'w')

### Process

for line in data_in:
# Reset iso_date
    iso_date = ''
# Skip blank line
    if re.match(blank_line, line):
        continue
# Remove new line, divide into fields, set date_created value
    line = line.rstrip('\n')
    fields = line.split('\t')
    date_created = fields[1]
# Check for single terms containing both letters and digits
    if re.search(alphanum, date_created):
        evalError('Alphanumeric term error')
        continue
# Handle multiple date values in field
    if re.search(pipe, date_created):
        date_list = date_created.split('|')
        date_list_iso = []
        set_error = False
# Derive ISO date for each date in list
        for d in date_list:
            if deriveYear(d) != 'error':
                iso_year = deriveYear(d)
            else:
                set_error = True
                continue
            if deriveMonth(d) != 'error':
                iso_month = deriveMonth(d)
            else:
                set_error = True
                continue
            if deriveDay(d) != 'error':
                iso_day = deriveDay(d)
            else:
                set_error = True
                continue                
            if makeISODate(iso_year, iso_month, iso_day) != 'error':
                iso_date = makeISODate(iso_year, iso_month, iso_day)
            else:
                continue
            date_list_iso.append(iso_date)
# Do not write to data_out if any date in the field produces errors
        if set_error:
            continue
# Output results with values separated by |
        iso_date = '|'.join(date_list_iso)
# Handle single date value in field
# Do not write to data_out if any part of the date produces errors, or if 
# there is insufficient data to generate ISO date
    else:
        if deriveYear(date_created) != 'error':
            iso_year = deriveYear(date_created)
        else:
            continue
        if deriveMonth(date_created) != 'error':
            iso_month = deriveMonth(date_created)
        else:
            continue
        if deriveDay(date_created) != 'error':
            iso_day = deriveDay(date_created)
        else:
            continue
        if makeISODate(iso_year, iso_month, iso_day) != 'error':
            iso_date = makeISODate(iso_year, iso_month, iso_day)
        else:
            continue
# Output result
    output_line = line + '\t' + iso_date + '\n'
    data_out.write(output_line)

data_in.close()
data_out.close()
error_log.close()
