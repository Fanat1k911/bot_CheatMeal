import datetime

TODAY = datetime.datetime.today()
CURRENT_YEAR = TODAY.year
CURRENT_MONTH = TODAY.month
NEXT_MONTH = CURRENT_MONTH + 1
DAYS_COUNT_OF_MONTH = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30,
                           12: 31}  # не весокосный год
# print(TODAY, CURRENT_MONTH, NEXT_MONTH)
