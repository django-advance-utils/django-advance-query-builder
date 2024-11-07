from django.db import models
from django.db.models import Sum, Max, Min, Count, Avg
from django.db.models.functions import TruncMonth, TruncQuarter, TruncYear, TruncWeek, TruncDay
from django_datatables.columns import CurrencyColumn, CurrencyPenceColumn, ColumnLink

from advanced_report_builder.columns import ColourColumn

NUMBER_FIELDS = (models.IntegerField,
                 models.PositiveSmallIntegerField,
                 models.PositiveIntegerField,
                 models.FloatField)
DATE_FIELDS = (models.DateTimeField, models.DateField)
BOOLEAN_FIELD = models.BooleanField
CURRENCY_COLUMNS = (CurrencyColumn, CurrencyPenceColumn)
LINK_COLUMNS = ColumnLink
COLOUR_COLUMNS = ColourColumn

ANNOTATION_VALUE_YEAR = 1
ANNOTATION_VALUE_QUARTER = 2
ANNOTATION_VALUE_MONTH = 3
ANNOTATION_VALUE_WEEK = 4
ANNOTATION_VALUE_DAY = 5

ANNOTATION_VALUE_CHOICES = [(ANNOTATION_VALUE_YEAR, 'Year'),
                            (ANNOTATION_VALUE_QUARTER, 'Quarter'),
                            (ANNOTATION_VALUE_MONTH, 'Month'),
                            (ANNOTATION_VALUE_WEEK, 'Week'),
                            (ANNOTATION_VALUE_DAY, 'Day')]

ANNOTATION_VALUE_FUNCTIONS = {ANNOTATION_VALUE_YEAR: TruncYear,
                              ANNOTATION_VALUE_QUARTER: TruncQuarter,
                              ANNOTATION_VALUE_MONTH: TruncMonth,
                              ANNOTATION_VALUE_WEEK: TruncWeek,
                              ANNOTATION_VALUE_DAY: TruncDay}

ANNOTATION_CHART_SCALE = {ANNOTATION_VALUE_YEAR: 'year',
                          ANNOTATION_VALUE_QUARTER: 'quarter',
                          ANNOTATION_VALUE_MONTH: 'month',
                          ANNOTATION_VALUE_WEEK: 'week',
                          ANNOTATION_VALUE_DAY: 'day'}

GENERATE_SERIES_INTERVALS = {ANNOTATION_VALUE_YEAR: '1 year',
                             ANNOTATION_VALUE_QUARTER: '3 month',
                             ANNOTATION_VALUE_MONTH: '1 month',
                             ANNOTATION_VALUE_WEEK: '1 week',
                             ANNOTATION_VALUE_DAY: '1 day'}

ANNOTATION_CHOICE_SUM = 1
ANNOTATION_CHOICE_MAXIMUM = 2
ANNOTATION_CHOICE_MINIMUM = 3
ANNOTATION_CHOICE_COUNT = 4
ANNOTATION_CHOICE_AVERAGE_SUM_FROM_COUNT = 5

ANNOTATIONS_CHOICES = [(ANNOTATION_CHOICE_SUM, 'Sum'),
                       (ANNOTATION_CHOICE_MAXIMUM, 'Maximum'),
                       (ANNOTATION_CHOICE_MINIMUM, 'Minimum'),
                       (ANNOTATION_CHOICE_COUNT, 'Count'),
                       (ANNOTATION_CHOICE_AVERAGE_SUM_FROM_COUNT, 'Average Sum from Count')]

ANNOTATION_FUNCTIONS = {ANNOTATION_CHOICE_SUM: Sum,
                        ANNOTATION_CHOICE_MAXIMUM: Max,
                        ANNOTATION_CHOICE_MINIMUM: Min,
                        ANNOTATION_CHOICE_COUNT: Count,
                        ANNOTATION_CHOICE_AVERAGE_SUM_FROM_COUNT: Avg}

ALIGNMENT_CHOICE_LEFT = 0
ALIGNMENT_CHOICE_CENTRE = 1
ALIGNMENT_CHOICE_RIGHT = 2

ALIGNMENT_CHOICES = [(ALIGNMENT_CHOICE_LEFT, 'Left'),
                     (ALIGNMENT_CHOICE_CENTRE, 'Centre'),
                     (ALIGNMENT_CHOICE_RIGHT, 'Right')]

ALIGNMENT_CLASS = {ALIGNMENT_CHOICE_LEFT: '',
                   ALIGNMENT_CHOICE_CENTRE: 'dt-center',
                   ALIGNMENT_CHOICE_RIGHT: 'dt-right'}

DATE_FORMAT_TYPE_DD_MM_YY_SLASH = 1
DATE_FORMAT_TYPE_DD_MM_YYYY_SLASH = 2
DATE_FORMAT_TYPE_MM_DD_YY_SLASH = 3
DATE_FORMAT_TYPE_MM_DD_YYYY_SLASH = 4
DATE_FORMAT_TYPE_DD_MM_YY_DASH = 5
DATE_FORMAT_TYPE_DD_MM_YYYY_DASH = 6
DATE_FORMAT_TYPE_MM_DD_YY_DASH = 7
DATE_FORMAT_TYPE_MM_DD_YYYY_DASH = 8
DATE_FORMAT_TYPE_WORDS_MM_DD_YYYY = 9
DATE_FORMAT_TYPE_WORDS_DD_MM_YYYY = 10
DATE_FORMAT_TYPE_SHORT_WORDS_MM_DD_YYYY = 11
DATE_FORMAT_TYPE_SHORT_WORDS_DD_MM_YYYY = 12
DATE_FORMAT_TYPE_YYYY = 13
DATE_FORMAT_TYPE_YY = 14
DATE_FORMAT_TYPE_MM_YY = 15
DATE_FORMAT_TYPE_MM_YYYY = 16
DATE_FORMAT_TYPE_WORDS_MM_YY = 17
DATE_FORMAT_TYPE_WORDS_MM_YYYY = 18
DATE_FORMAT_TYPE_SHORT_WORDS_MM_YY = 19
DATE_FORMAT_TYPE_SHORT_WORDS_MM_YYYY = 20
DATE_FORMAT_TYPE_MM = 21
DATE_FORMAT_TYPE_WORDS_MM = 22
DATE_FORMAT_TYPE_SHORT_WORDS_MM = 23
DATE_FORMAT_TYPE_WW = 24
DATE_FORMAT_TYPE_WW_YYYY_DASH = 25
DATE_FORMAT_TYPE_WW_YY_DASH = 26
DATE_FORMAT_TYPE_YYYY_MM = 27


DATE_FORMAT_TYPES_DJANGO_FORMAT = {DATE_FORMAT_TYPE_DD_MM_YY_SLASH: '%d/%m/%y',
                                   DATE_FORMAT_TYPE_DD_MM_YYYY_SLASH: '%d/%m/%Y',
                                   DATE_FORMAT_TYPE_MM_DD_YY_SLASH: '%m/%d/%y',
                                   DATE_FORMAT_TYPE_MM_DD_YYYY_SLASH: '%m/%d/%Y',
                                   DATE_FORMAT_TYPE_DD_MM_YY_DASH: '%d-%m-%y',
                                   DATE_FORMAT_TYPE_DD_MM_YYYY_DASH: '%d-%m-%Y',
                                   DATE_FORMAT_TYPE_MM_DD_YY_DASH: '%m-%d-%y',
                                   DATE_FORMAT_TYPE_MM_DD_YYYY_DASH: '%m-%d-%Y',
                                   DATE_FORMAT_TYPE_WORDS_MM_DD_YYYY: '%B %d %Y',
                                   DATE_FORMAT_TYPE_WORDS_DD_MM_YYYY: '%d %B %Y',
                                   DATE_FORMAT_TYPE_SHORT_WORDS_MM_DD_YYYY: '%b %d %Y',
                                   DATE_FORMAT_TYPE_SHORT_WORDS_DD_MM_YYYY: '%d %b %Y',
                                   DATE_FORMAT_TYPE_YYYY: '%Y',
                                   DATE_FORMAT_TYPE_YY: '%y',
                                   DATE_FORMAT_TYPE_MM_YY: '%m %y',
                                   DATE_FORMAT_TYPE_YYYY_MM: '%Y %m',
                                   DATE_FORMAT_TYPE_MM_YYYY: '%m %Y',
                                   DATE_FORMAT_TYPE_WORDS_MM_YY: '%B %y',
                                   DATE_FORMAT_TYPE_WORDS_MM_YYYY: '%B %Y',
                                   DATE_FORMAT_TYPE_SHORT_WORDS_MM_YY: '%b %y',
                                   DATE_FORMAT_TYPE_SHORT_WORDS_MM_YYYY: '%b %Y',
                                   DATE_FORMAT_TYPE_MM: '%m',
                                   DATE_FORMAT_TYPE_WORDS_MM: '%B',
                                   DATE_FORMAT_TYPE_SHORT_WORDS_MM: '%b',
                                   DATE_FORMAT_TYPE_WW: '%W',
                                   DATE_FORMAT_TYPE_WW_YYYY_DASH: '%W-%Y',
                                   DATE_FORMAT_TYPE_WW_YY_DASH: '%W-%y',

                                   }

DATE_FORMAT_TYPES = [
    (DATE_FORMAT_TYPE_DD_MM_YY_SLASH, 'dd/mm/yy'),
    (DATE_FORMAT_TYPE_DD_MM_YYYY_SLASH, 'dd/mm/yyyy'),
    (DATE_FORMAT_TYPE_MM_DD_YY_SLASH, 'mm/dd/yy'),
    (DATE_FORMAT_TYPE_MM_DD_YYYY_SLASH, 'mm/dd/yyyy'),
    (DATE_FORMAT_TYPE_DD_MM_YY_DASH, 'dd-mm-yy'),
    (DATE_FORMAT_TYPE_DD_MM_YYYY_DASH, 'dd-mm-yyyy'),
    (DATE_FORMAT_TYPE_MM_DD_YY_DASH, 'mm-dd-yy'),
    (DATE_FORMAT_TYPE_MM_DD_YYYY_DASH, 'mm-dd-yyyy'),
    (DATE_FORMAT_TYPE_WORDS_MM_DD_YYYY, 'MM d yyyy'),
    (DATE_FORMAT_TYPE_WORDS_DD_MM_YYYY, 'd MM yyyy'),
    (DATE_FORMAT_TYPE_SHORT_WORDS_MM_DD_YYYY, 'M d yyyy'),
    (DATE_FORMAT_TYPE_SHORT_WORDS_DD_MM_YYYY, 'd M yyyy'),
    (DATE_FORMAT_TYPE_YYYY, 'yyyy'),
    (DATE_FORMAT_TYPE_YY, 'yy'),
    (DATE_FORMAT_TYPE_MM_YY, 'mm yy'),
    (DATE_FORMAT_TYPE_MM_YYYY, 'mm yyyy'),
    (DATE_FORMAT_TYPE_YYYY_MM, 'yyyy mm'),
    (DATE_FORMAT_TYPE_WORDS_MM_YY, 'MM yy'),
    (DATE_FORMAT_TYPE_WORDS_MM_YYYY, 'MM yyyy'),
    (DATE_FORMAT_TYPE_SHORT_WORDS_MM_YY, 'b yy'),
    (DATE_FORMAT_TYPE_SHORT_WORDS_MM_YYYY, 'b yyyy'),
    (DATE_FORMAT_TYPE_MM, 'mm'),
    (DATE_FORMAT_TYPE_WORDS_MM, 'MM'),
    (DATE_FORMAT_TYPE_SHORT_WORDS_MM, 'd'),
    (DATE_FORMAT_TYPE_WW, 'WW'),
    (DATE_FORMAT_TYPE_WW_YYYY_DASH, 'WW-YYYY'),
    (DATE_FORMAT_TYPE_WW_YY_DASH, 'WW-YY'),
]

DISPLAY_OPTION_NONE = 0
DISPLAY_OPTION_1_PER_ROW = 1
DISPLAY_OPTION_2_PER_ROW = 2
DISPLAY_OPTION_3_PER_ROW = 3
DISPLAY_OPTION_4_PER_ROW = 4


DISPLAY_OPTION_CHOICES = [
    (DISPLAY_OPTION_NONE, 'None/Default'),
    (DISPLAY_OPTION_1_PER_ROW, '1 Report per Row'),
    (DISPLAY_OPTION_2_PER_ROW, '2 Reports per Row'),
    (DISPLAY_OPTION_3_PER_ROW, '3 Reports per Row'),
    (DISPLAY_OPTION_4_PER_ROW, '4 Reports per Row'),
]

DISPLAY_OPTION_CLASSES = {DISPLAY_OPTION_1_PER_ROW: ' col-12',
                          DISPLAY_OPTION_2_PER_ROW: ' col-12 col-md-12 col-lg-6',
                          DISPLAY_OPTION_3_PER_ROW: ' col-12 col-md-12 col-lg-4',
                          DISPLAY_OPTION_4_PER_ROW: ' col-12 col-md-12 col-lg-3',
                          }

DEFAULT_DATE_FORMAT = {ANNOTATION_VALUE_YEAR: DATE_FORMAT_TYPE_YYYY,
                       ANNOTATION_VALUE_QUARTER: DATE_FORMAT_TYPE_WORDS_MM_YY,
                       ANNOTATION_VALUE_MONTH: DATE_FORMAT_TYPE_WORDS_MM_YY,
                       ANNOTATION_VALUE_WEEK: DATE_FORMAT_TYPE_WW_YY_DASH,
                       ANNOTATION_VALUE_DAY: DATE_FORMAT_TYPE_DD_MM_YY_SLASH}
