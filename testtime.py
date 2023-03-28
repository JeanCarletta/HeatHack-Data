import datetime
import pytz

utc = pytz.UTC
gmt = pytz.timezone('GMT')
#bst = pytz.timezone('BST')

london = pytz.timezone('Europe/London')

date1 = datetime.datetime(2023,3,15,9,00,00)
date2 = datetime.datetime(2023,4,15,9,00,00)
date3 = datetime.datetime(2023,4,15,9,00,00,tzinfo=gmt)

date1 = utc.localize(date1)
date2 = utc.localize(date2)

print(date1.astimezone(london))
print(date2.astimezone(london))
print(date3.astimezone(london))
print(date3)
#print(date4.astimezone(london))

#date2 = datetime('2023-04-15T09:00:00Z')
fmt = '%Y-%m-%d %H:%M:%S %Z%z'