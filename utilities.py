from dateutil.relativedelta import relativedelta
import calendar
import datetime
from collections import defaultdict


def group(req_data, group_by=None):
    groups = defaultdict(list)
    res_data = req_data

    def del_key(d):
        del d['id']
        return d

    res_data = map(del_key, res_data)
    if group_by is not None:
        for obj in res_data:
            groups[obj[group_by]].append(obj)
        res_data1 = groups.values()
        res_data = []
        for item in res_data1:
            keys = item[0].keys()
            new = {}
            for key in keys:
                if key != 'country' and key != 'date':
                    x = 0
                    for data in item:
                        x += int(float(data[key]))
                    new[key] = x
                elif key == 'country':
                    new[key] = item[0][key]
            res_data.append(new)
    return res_data

def credentials_to_dict(credentials):
  return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}


def date_converter(dates):
    newdates = {}
    for key, value in dates.iteritems():
        date = dates[key].split('/')
        newdates[key] = date[2]+'-'+date[0]+'-'+date[1]
    return newdates

def get_dates(N):

    pre_end = datetime.datetime.now() + relativedelta(days=-2)
    pre_start = datetime.datetime.now() + relativedelta(days=-N-1)
    prv_end = pre_start + relativedelta(days=-1)
    prv_start = prv_end + relativedelta(days=-(N-1))
    return (
            {
                'pre_start': pre_start.strftime('%Y-%m-%d'),
                'pre_end': pre_end.strftime('%Y-%m-%d'),
                'prv_start': prv_start.strftime('%Y-%m-%d'),
                'prv_end': prv_end.strftime('%Y-%m-%d')
            },
            {
                'pre_start': pre_start.strftime('%d-%b-%y'),
                'pre_end': pre_end.strftime('%d-%b-%y'),
                'prv_start': prv_start.strftime('%d-%b-%y'),
                'prv_end': prv_end.strftime('%d-%b-%y')
            }
            )

def get_two_month_dates():

    prev_month = int(datetime.datetime.now().strftime('%m')) - 1
    year = int((datetime.datetime.now().strftime('%Y-%m')).split('-')[0])
    num_days = calendar.monthrange(year, prev_month)
    pre_start = datetime.date(year, prev_month, 1)
    pre_end = datetime.date(year, prev_month, num_days[1])
    year = year if prev_month != 1 else year - 1
    prev_month = (prev_month - 1) if prev_month != 1 else 12
    num_days = calendar.monthrange(year, prev_month)
    prv_start = datetime.date(year, prev_month, 1)
    prv_end = datetime.date(year, prev_month, num_days[1])

    return ({
                'pre_start': pre_start.strftime('%Y-%m-%d'),
                'pre_end': pre_end.strftime('%Y-%m-%d'),
                'prv_start': prv_start.strftime('%Y-%m-%d'),
                'prv_end': prv_end.strftime('%Y-%m-%d')
            },
            {
                'pre_start': pre_start.strftime('%d-%b-%y'),
                'pre_end': pre_end.strftime('%d-%b-%y'),
                'prv_start': prv_start.strftime('%d-%b-%y'),
                'prv_end': prv_end.strftime('%d-%b-%y')
            })

def prev_month_last_year():

    prev_month = int(datetime.datetime.now().strftime('%m')) - 1
    year = int((datetime.datetime.now().strftime('%Y-%m')).split('-')[0])
    num_days = calendar.monthrange(year, prev_month)
    pre_start = datetime.date(year, prev_month, 1)
    pre_end = datetime.date(year, prev_month, num_days[1])
    print(pre_start, pre_end)
    prv_start = datetime.date(year - 1, prev_month, 1)
    prv_end = datetime.date(year - 1, prev_month, num_days[1])

    return ({
                'pre_start': pre_start.strftime('%Y-%m-%d'),
                'pre_end': pre_end.strftime('%Y-%m-%d'),
                'prv_start': prv_start.strftime('%Y-%m-%d'),
                'prv_end': prv_end.strftime('%Y-%m-%d')
            },
            {
                'pre_start': pre_start.strftime('%d-%b-%y'),
                'pre_end': pre_end.strftime('%d-%b-%y'),
                'prv_start': prv_start.strftime('%d-%b-%y'),
                'prv_end': prv_end.strftime('%d-%b-%y')
            })

def last_year():
    year = int((datetime.datetime.now().strftime('%Y-%m')).split('-')[0])
    pre_start = datetime.date(year - 1, 1, 1)
    pre_end = datetime.date(year - 1, 12, 31)
    prv_start = datetime.date(year - 2, 1, 1)
    prv_end = datetime.date(year - 2, 12, 31)

    return ({
                'pre_start': pre_start.strftime('%Y-%m-%d'),
                'pre_end': pre_end.strftime('%Y-%m-%d'),
                'prv_start': prv_start.strftime('%Y-%m-%d'),
                'prv_end': prv_end.strftime('%Y-%m-%d')
            },
            {
                'pre_start': pre_start.strftime('%d-%b-%y'),
                'pre_end': pre_end.strftime('%d-%b-%y'),
                'prv_start': prv_start.strftime('%d-%b-%y'),
                'prv_end': prv_end.strftime('%d-%b-%y')
            })

def get12months():

    prev_month = datetime.date.today().month - 1
    year = int((datetime.datetime.now().strftime('%Y-%m')).split('-')[0])
    num_days = calendar.monthrange(year, prev_month)
    pre_end = datetime.date(year, prev_month, num_days[1])
    pre_start = pre_end + relativedelta(days=1) + relativedelta(months=-12)
    prv_end = pre_start + relativedelta(days=-1)
    prv_start = prv_end + relativedelta(days=1) + relativedelta(months=-12)

    return ({
                 'pre_start': pre_start.strftime('%Y-%m-%d'),
                 'pre_end': pre_end.strftime('%Y-%m-%d'),
                 'prv_start': prv_start.strftime('%Y-%m-%d'),
                 'prv_end': prv_end.strftime('%Y-%m-%d')
             },
             {
                 'pre_start': pre_start.strftime('%d-%b-%y'),
                 'pre_end': pre_end.strftime('%d-%b-%y'),
                 'prv_start': prv_start.strftime('%d-%b-%y'),
                 'prv_end': prv_end.strftime('%d-%b-%y')
             })

def change(source, result):

    present, previous = [], []
    for item in result['present']:
        present.append(item.get(source, 0))
    for item in result['previous']:
        previous.append(item.get(source,0))
    Change = []
    for i in range(len(previous)):
        change = round(((float(present[i]) - float(previous[i])) / float(previous[i])) * 100, 2) if previous[i] != 0 else 100
        if change>100:
            change = 100
        Change.append(change)
    return Change

def get_month_names(date1, date2):

    month1 = calendar.month_name[int(date1.split("-")[1])]
    month2 = calendar.month_name[int(date2.split("-")[1])]
    return month1, month2

