"""Functions that convert an abbreviated weekday or month to their full name

Some websites use abbreviations for weekdays or months. These can allow me to easily convert the shorter
abbreviation to the longer version.
"""


from day_month_strings import WeekdayAbbreviations
from day_month_strings import MonthAbbreviations
from day_month_strings import WeekdayFullNames
from day_month_strings import MonthFullNames


def weekday_converter(weekday_abbreviation):
    """
    Takes a weekday abbreviation, converts to full name

    :param weekday_abbreviation: a three letter abbreviation for a day of the week
    :type: str

    :return: the full name of the given weekday
    :rtype: str
    """

    if weekday_abbreviation == WeekdayAbbreviations.MONDAY:
        return WeekdayFullNames.MONDAY
    elif weekday_abbreviation == WeekdayAbbreviations.TUESDAY:
        return WeekdayFullNames.TUESDAY
    elif weekday_abbreviation == WeekdayAbbreviations.WEDNESDAY:
        return WeekdayFullNames.WEDNESDAY
    elif weekday_abbreviation == WeekdayAbbreviations.THURSDAY:
        return WeekdayFullNames.THURSDAY
    elif weekday_abbreviation == WeekdayAbbreviations.FRIDAY:
        return WeekdayFullNames.FRIDAY
    elif weekday_abbreviation == WeekdayAbbreviations.SATURDAY:
        return WeekdayFullNames.SATURDAY
    elif weekday_abbreviation == WeekdayAbbreviations.SUNDAY:
        return WeekdayFullNames.SUNDAY


def month_converter(month_abbreviation):
    """
    Takes a month abbreviation, converts to full name

    :param month_abbreviation: a three letter abbreviation for a month
    :type: str

    :return: the full name of the given month
    :rtype: str
    """

    if month_abbreviation == MonthAbbreviations.JANUARY:
        return MonthFullNames.JANUARY
    elif month_abbreviation == MonthAbbreviations.FEBRUARY:
        return MonthFullNames.FEBRUARY
    elif month_abbreviation == MonthAbbreviations.MARCH:
        return MonthFullNames.MARCH
    elif month_abbreviation == MonthAbbreviations.APRIL:
        return MonthFullNames.APRIL
    elif month_abbreviation == MonthAbbreviations.MAY:
        return MonthFullNames.MAY
    elif month_abbreviation == MonthAbbreviations.JUNE:
        return MonthFullNames.JUNE
    elif month_abbreviation == MonthAbbreviations.JULY:
        return MonthFullNames.JULY
    elif month_abbreviation == MonthAbbreviations.AUGUST:
        return MonthFullNames.AUGUST
    elif month_abbreviation == MonthAbbreviations.SEPTEMBER:
        return MonthFullNames.SEPTEMBER
    elif month_abbreviation == MonthAbbreviations.OCTOBER:
        return MonthFullNames.OCTOBER
    elif month_abbreviation == MonthAbbreviations.NOVEMBER:
        return MonthFullNames.NOVEMBER
    elif month_abbreviation == MonthAbbreviations.DECEMBER:
        return MonthFullNames.DECEMBER
