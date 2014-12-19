Generate ISO-8601 Dates From Date Strings
=========================================

Functionality
-------------
Given a human-readable date (e.g., 'June 16, 1904'), generate a date in the format 'YYYY-MM-DD', 'YYYY-MM', or 'YYYY', in conformance with the ISO-8601 date standard. Also performs some date validation, returning errors if the year has the wrong number of digits, the day is greater than 31, or a text term is present that does not match a month name or a form of 'circa'.

Input
-----
* dates_in.txt: Tab-delimited text file, with human-readable dates in second column (assumption is that first column will contain record IDs, but any value is acceptable).


Output
------
* dates_out.txt: Input lines successfully processed, with addition of column containing ISO dates.
* dates_errorlog.txt: Input lines generating errors or containing insufficient data, with addition of column containing error message.


Multiple date values
--------------------
The script will accommodate multiple date values in a single cell separated by a pipe ('|'), and will output multiple ISO dates in the same order with the same separator.

Date ranges or multiple date values with any other separator will generate an error.

Date forms handled
------------------
Any combination of a single capitalized English-language month term, day from 1 to 31, and four-digit year according to the Gregorian calendar, separated by a comma (',') and/or a space (' '), as well as the special case of a combined Old Style/New Style year, separated by a forward slash ('/'). (See Note below.)

If the date value does not contain a year, the error 'Insufficient data to generate ISO date' will result.

Forms of 'circa' ('c', 'c.', 'ca', 'ca.', 'circ', 'circ.', 'circa') are ignored, and the ISO date is generated (or error evaluated) as if the term were not present.

Examples of date input formats successfully transformed:
--------------------------------------------------------
* June 16, 1904 => 1904-06-16
* June 16 1904 => 1904-06-16
* June 16,1904 => 1904-06-16
* 16 June 1904 => 1904-06-16
* 1904, June 16 => 1904-06-16
* June 1904 => 1904-06
* June, 1904 => 1904-06
* 1904 => 1904
* c. June 16, 1904 => 1904-06-16
* ca. June 1904 => 1904-06
* circa 1904 => 1904
* February 1, 1660/1 => 1661-02-01
* February 1, 1660/61 => 1661-02-01
* February 1, 1660/1661 => 1661-02-01
* February 1660/1 => 1661-02
* February 1699/1700 => 1700-02
* February 1699/700 => 1700-02
* February 1, 1660/1|June 16, 1904 => 1661-02-01|1904-06-16

Examples of date input formats generating errors:
-------------------------------------------------
* approx June 16, 1904 => Month error (text term not recognized)
* june 16, 1904 => Month error (matching is case-sensitive)
* June 16, 19904 => Year error (more than 4 digits)
* June 161, 1904 => Day error (greater than 31)
* June 16 => Insufficient data to generate ISO date (year missing)
* June 15, 1904 - June 16, 1904 => Year error (multiple years without valid separator)
* circa 1904-1905 => Year error (multiple years without valid separator)
* 1904/1905 => Year error ('/' in year without month)
* 1904/June 16 => Year error (invalid separator between year and month)
* February 1, 1699/00 => Year error (N.S. year composed solely of zeroes)
* February 1, 1669/0 => Year error (N.S. year composed solely of zeroes)
* June16 1904 => Alphanumeric term error (no space between letter and number)

Note
----

England and Wales used the Julian calendar with the new year beginning on March 25 ('Old Style') from the 12th century until 1752, well after continental Europe switched to the Gregorian calendar beginning January 1 ('New Style'). It was common in many contexts for both calendars to be acknowledged when recording a date before March 25, in the form 'February 1, 1660/61' or similar.

Credit
------
Script by Arcadia Falcone, arcadiafalcone at gmail  
Updated 2014-05-16; reformatted 2014-12-19
