from __future__ import print_function
import itertools
from operator import itemgetter
from chainmap import ChainMap
from functools import reduce

def get_Month_data(req_data, keys):
    res_data1 = req_data
    res_data = []
    for item in res_data1:
        new = {}
        for key in keys:
            if key != 'Country' and key != 'option':
                x = 0
                for data in item:
                    x += int(float(data.get(key, 0)))
                new[key] = x
            elif key == 'Country':
                new[key] = item[0][key]
        res_data.append(new)
    return res_data


#----------------------------------------------------------------------------------------------------



def get_profile_id(service):

  accounts = service.management().accounts().list().execute()

  if accounts.get('items'):
    firstAccountId = accounts.get('items')[0].get('id')

    webproperties = service.management().webproperties().list(
        accountId=firstAccountId).execute()

    if webproperties.get('items'):
      try:
          firstWebpropertyId = webproperties.get('items')[0].get('id')
          profiles_id = service.management().profiles().list(
              accountId=firstAccountId,
              webPropertyId=firstWebpropertyId).execute().get('items')[0].get('id')
          return profiles_id

      except Exception as e:
          print(e)
          pass

  return None


#-----------------------------------------------------------------------------------------------------------------------


def get_top_keywords(service, profile_id, startDate1, endDate1):

    results = service.data().ga().get(
      ids='ga:' + profile_id,
      start_date=startDate1,
      end_date=endDate1,
      metrics='ga:sessions',
      dimensions='ga:deviceCategory',
      segment='gaid::-11'
    ).execute()

    resultsb = service.data().ga().get(
      ids='ga:' + profile_id,
      start_date=startDate1,
      end_date=endDate1,
      metrics='ga:bouncerate',
      dimensions='ga:deviceCategory',
      segment='gaid::-11'
    ).execute()

    resultsc = service.data().ga().get(
      ids='ga:' + profile_id,
      start_date=startDate1,
      end_date=endDate1,
      metrics='ga:goalconversionrateall',
      dimensions='ga:deviceCategory',
      segment='gaid::-3'
    ).execute()

    resultsd = service.data().ga().get(
      ids='ga:' + profile_id,
      start_date=startDate1,
      end_date=endDate1,
      metrics='ga:goalconversionrateall',
      dimensions='ga:deviceCategory',
      segment='gaid::-2'
    ).execute()

    resultse = service.data().ga().get(
      ids='ga:' + profile_id,
      start_date=startDate1,
      end_date=endDate1,
      metrics='ga:avgsessionduration',
      dimensions='ga:deviceCategory',
      segment=None
    ).execute()

    return (results,resultsb,resultsc,resultsd,resultse)

def print_top_keywords(results):

    print(results)
    print('TopConversions')



#-----------------------------------------------------------------------------------------------------------------------



def get_agents(service, profile_id,pre_startDate,pre_endDate):
  pres_month = service.data().ga().get(
    ids='ga:' + profile_id,
    start_date=str(pre_startDate),
    end_date=str(pre_endDate),
    metrics='ga:uniqueEvents',
    dimensions='ga:eventCategory,ga:eventAction',
    filters='ga:eventCategory!=ArtistPortfolio;ga:eventCategory!=Newsletter;ga:eventCategory!=SideButtons;ga:eventCategory!=Social;ga:eventCategory!=YouMightAlsoLike;ga:eventCategory!=Artist Quote;ga:eventAction!=Impressions'
  ).execute()
  return pres_month


def print_agents(results):

    def dict_conversion(a):
        if len(a) > 2:
            a.pop(0)
        return a
    present_result = dict(map(dict_conversion, results.get('rows', [["", ""]])))
    # print('print_agents\n', present_result)
    return present_result

def get_sidebtn(service, profile_id,pre_startDate,pre_endDate):
  pres_month = service.data().ga().get(
    ids='ga:' + profile_id,
    start_date=str(pre_startDate),
    end_date=str(pre_endDate),
    metrics='ga:uniqueEvents',
    dimensions='ga:eventLabel',
    filters='ga:eventCategory==SideButtons'
  ).execute()

  return pres_month

def print_sidebtn(results):
    present_result = (dict(results.get('rows', [["", ""]])))
    # print('side_btn')
    # print(present_result)
    return present_result

def get_portpolio(service, profile_id,pre_startDate,pre_endDate):
  pres_month = service.data().ga().get(
    ids='ga:' + profile_id,
    start_date=str(pre_startDate),
    end_date=str(pre_endDate),
    metrics='ga:uniqueEvents',
    dimensions='ga:eventAction',
    filters='ga:eventCategory==ArtistPortfolio'
  ).execute()

  return pres_month

def print_portpolio(results):
    # print('portfolio')
    present_result = (dict(results.get('rows', [["", ""]])))
    # print(present_result)
    return present_result



#----------------------------------------------------------------------------------------------------------------



def get_sessions(service, type, profile_id, filters, startDate1, endDate1):

  dimensions = 'ga:channelGrouping'+"," + type
  try:
      if filters == 'SEA':
          filters = 'ga:subContinent==Southeast Asia'
          metrics = 'ga:sessions'
          dimensions = dimensions
      elif filters == 'ROW':
          filters = 'ga:country!=United Kingdom;ga:country!=India;ga:subContinent!=Southeast Asia;ga:continent!=Oceania'
          metrics = 'ga:sessions'
          dimensions = dimensions
      elif filters == 'ANZ':
          filters = 'ga:continent==Oceania'
          metrics = 'ga:sessions'
          dimensions = dimensions
      elif filters == 'ROWUSA':
          filters = 'ga:country!=United States;ga:country!=Canada'
          metrics = 'ga:sessions'
          dimensions = dimensions
      elif filters == 'France' or filters == 'China':
          filters = None
          metrics = 'ga:sessions'
          dimensions = dimensions
      else:
          metrics = 'ga:sessions'
          dimensions = dimensions
          filters = 'ga:country=={}'.format(filters)

  except Exception as e:
      print(e)
      pass

  pres_month = service.data().ga().get(
      ids='ga:' + profile_id,
      start_date=str(startDate1),
      end_date=str(endDate1),
      metrics=metrics,
      dimensions=dimensions,
      filters=filters
    ).execute()
  pres_month2 = service.data().ga().get(
      ids='ga:' + profile_id,
      start_date=str(startDate1),
      end_date=str(endDate1),
      metrics='ga:goalCompletionsAll',
      filters=filters
  ).execute()

  return pres_month,pres_month2

def print_sessions(results, country):

    if country == 'United States,ga:country==Canada':
        country = 'US'
    elif country == 'United Kingdom':
        country = 'UK'

    results = results.get('rows')

    def new_result(result):
        l = {"option": result[1], result[0]: result[2]}
        return l

    results = itertools.groupby(sorted(list(map(new_result, results)), key=itemgetter('option')), key=lambda x: x['option'])
    result = []
    for key, item in results:
        result.append(dict(ChainMap(*list(item)+[{'Country': country}])))

    key_lst = ['Referral', 'Direct', 'Social', 'Organic Search', 'Paid Search', 'Country', 'option']

    def merge_email(a):
        keys = list(a.keys())
        Email = 0
        for key in keys:
            if key not in key_lst:
                Email += int(a[key])
                del a[key]
        a['Email'] = str(Email)
        return a

    result = list(map(merge_email, result))
    return result

def total_sessions(res_data):

    totalSessions = []
    for i in res_data:
        new = []
        for j in i:
            k = {
                'Country': j['Country'],
                'TotalSessions': int(j.get('Paid Search', 0)) + int(j.get('Direct', 0)) + int(j.get('Social', 0)) +
                                 int(j.get('Organic Search', 0)) + int(j.get('Referral', 0)) + int(j.get('Email', 0))
            }
            new.append(k)
        totalSessions.append(new)
    return totalSessions


#-----------------------------------------------------------------------------


def get_events(service, profile_id, startDate1, endDate1):

    metrics = 'ga:uniqueEvents'
    dimensions = 'ga:eventLabel'
    filters = 'ga:eventLabel==HelloBar'
    pres_month = service.data().ga().get(
        ids='ga:' + profile_id,
        start_date=str(startDate1),
        end_date=str(endDate1),
        metrics=metrics,
        dimensions=dimensions,
        filters=filters
    ).execute()

    return pres_month

def print_events(results, country):
    try:
        result1 = (dict(results.get('rows')))
    except:
        result1 = {}

    result = {'Country': country.split('Events')[0], 'HelloBar Events': result1.get('HelloBar', '0')}

    # print("EVENTS:\n")
    # print(result)
    return result

#-----------------------------------------------------------------------------

def get_devices(service, profile_id, startDate1, endDate1):
    metrics = 'ga:uniqueEvents'
    dimensions = 'ga:deviceCategory'
    filters = 'ga:eventLabel=~Job Quote'
    pres_month = service.data().ga().get(
        ids='ga:' + profile_id,
        start_date=str(startDate1),
        end_date=str(endDate1),
        metrics=metrics,
        dimensions=dimensions,
        filters=filters
    ).execute()

    return pres_month

def print_devices(results):

    try:
        result1 = (dict(results.get('rows')))
    except:
        result1 = {}
    return result1

#-----------------------------------------------------------------------------------------------------------------------

def get_devices_sessions(service, profile_id, startDate1, endDate1):

    metrics = 'ga:sessions'
    dimensions = 'ga:deviceCategory'
    pres_month = service.data().ga().get(
        ids='ga:' + profile_id,
        start_date=str(startDate1),
        end_date=str(endDate1),
        metrics=metrics,
        dimensions=dimensions,
    ).execute()
    return pres_month

def print_devices_sessions(results, country):
    try:
        result1 = (dict(results.get('rows')))
    except:
        result1 = {}
    result1['Country'] = country
    return result1

#-----------------------------------------------------------------------------------------------------------------------

def get_CPC(service, profile_id, startDate1, endDate1):

    metrics = 'ga:goalCompletionsAll'
    dimensions = 'ga:source'
    filters = 'ga:medium==cpc'
    pres_month = service.data().ga().get(
        ids='ga:' + profile_id,
        start_date=str(startDate1),
        end_date=str(endDate1),
        metrics=metrics,
        dimensions=dimensions,
        filters=filters
    ).execute()

    return pres_month

def print_CPC(results):

    try:
        result1 = (dict(results.get('rows')))
    except:
        result1 = {}

    # print("CPC:\n")
    # print(result1, '\n')
    return result1

#=======================================================================================================================
def print_Trafiic(results):
    results = results.get('rows')
    def new_result(result):

        l = {"option": result[0], 'traffic': result[1]}
        return l
    results = itertools.groupby(sorted(list(map(new_result, results)), key=itemgetter('option')), key=lambda x: x['option'])
    result = []
    for key, item in results:
        result.append(dict(ChainMap(*list(item))))
    return result

def getAllTraffic(service,option, profile_id, startDate1, endDate1):

   metrics = 'ga:sessions'
   dimensions = option

   AllTraffic = service.data().ga().get(
       ids='ga:' + profile_id,
       start_date=str(startDate1),
       end_date=str(endDate1),
       metrics=metrics,
       dimensions=dimensions,
   ).execute()

   return AllTraffic

#=======================================================================================================================

def print_sourceTraffic(results):
    results = results.get('rows')
    def new_result(result):
        l = {"option": result[1], 'Email' if result[0]=='(Other)' else result[0]: result[2]}
        return l
    results = itertools.groupby(sorted(list(map(new_result, results)), key=itemgetter('option')), key=lambda x: x['option'])
    result = []
    for key, item in results:
        i = [j for j in item]
        result.append(dict(ChainMap(*list(i))))
    return result
#=======================================================================================================================

def get_MobileTabletTraffic(service, option, profile_id, startDate1, endDate1):

    dimensions = option
    results = service.data().ga().get(
     ids='ga:' + profile_id,
     start_date=startDate1,
     end_date=endDate1,
     metrics='ga:sessions',
     dimensions=dimensions,
     segment='gaid::-11'
    ).execute()

    return results

#=======================================================================================================================

def get_return_users(service, option, profile_id, pre_startDate, pre_endDate):

   dimensions = option
   pres_month = service.data().ga().get(
       ids='ga:' + profile_id,
       start_date=str(pre_startDate),
       end_date=str(pre_endDate),
       metrics='ga:sessions',
       dimensions=dimensions,
       segment='gaid::-3',
   ).execute()
   return pres_month

#-----------------------------------------------------------------------------------------------------------------------

def get_region_bouncerate(service, startDate, endDate):

    UK = service.data().ga().get(

            ids='ga:5110029',
            start_date=startDate,
            end_date=endDate,
            metrics='ga:bouncerate',
            dimensions='ga:deviceCategory',
            filters='ga:country==United Kingdom',

        ).execute()

    US = service.data().ga().get(

        ids='ga:84906789',
        start_date=startDate,
        end_date=endDate,
        metrics='ga:bouncerate',
        dimensions='ga:deviceCategory',
        filters='ga:country==United States,ga:country==Canada',
        ).execute()

    SEA = service.data().ga().get(
        ids='ga:5110029',
        start_date=startDate,
        end_date=endDate,
        metrics='ga:bouncerate',
        dimensions='ga:deviceCategory',
        filters='ga:subContinent==Southeast Asia',
    ).execute()

    ANZ = service.data().ga().get(
        ids='ga:5110029',
        start_date=startDate,
        end_date=endDate,
        metrics='ga:bouncerate',
        dimensions='ga:deviceCategory',
        filters='ga:continent==Oceania',

    ).execute()

    France = service.data().ga().get(
        ids='ga:85625764',
        start_date=startDate,
        end_date=endDate,
        metrics='ga:bouncerate',
        dimensions='ga:deviceCategory',
        filters='ga:country==France',

    ).execute()

    return {
            'UK': round(float(UK.get('totalsForAllResults')['ga:bouncerate']), 2),
            'US': round(float(US.get('totalsForAllResults')['ga:bouncerate']), 2),
            'SEA': round(float(SEA.get('totalsForAllResults')['ga:bouncerate']), 2),
            'ANZ': round(float(ANZ.get('totalsForAllResults')['ga:bouncerate']), 2),
            'France': round(float(France.get('totalsForAllResults')['ga:bouncerate']), 2)
        }

#-----------------------------------------------------------------------------------------------------------------------

def get_bouncerate_Bysource(service, profile_id, startDate, endDate):

    results = service.data().ga().get(
            ids='ga:' + profile_id,
            start_date=startDate,
            end_date=endDate,
            metrics='ga:bouncerate',
            dimensions='ga:channelGrouping',
        ).execute()

    return results

def print_bouncerate_Bysource(results):

    result = dict(results.get('rows', [[]]))
    result['Email'] = result.get('(Other)', 0)
    if result.get('(Other)', 0) != 0:
        del result['(Other)']
    return result

#-----------------------------------------------------------------------------------------------------------------------

def get_MobileTablet_bouncerate(service, profile_id, startDate, endDate):

    results = service.data().ga().get(
        ids='ga:' + profile_id,
        start_date=startDate,
        end_date=endDate,
        metrics='ga:bouncerate',
        dimensions='ga:deviceCategory',
        segment='gaid::-11'
    ).execute()

    return results

#-----------------------------------------------------------------------------------------------------------------------

def get_region_avgsession(service, startDate, endDate):

    UK = service.data().ga().get(

            ids='ga:5110029',
            start_date=startDate,
            end_date=endDate,
            metrics='ga:bouncerate',
            dimensions='ga:deviceCategory',
            filters='ga:country==United Kingdom',

        ).execute()

    US = service.data().ga().get(

        ids='ga:84906789',
        start_date=startDate,
        end_date=endDate,
        metrics='ga:bouncerate',
        dimensions='ga:deviceCategory',
        filters='ga:country==United States,ga:country==Canada',
        ).execute()

    SEA = service.data().ga().get(
        ids='ga:5110029',
        start_date=startDate,
        end_date=endDate,
        metrics='ga:bouncerate',
        dimensions='ga:deviceCategory',
        filters='ga:subContinent==Southeast Asia',
    ).execute()

    ANZ = service.data().ga().get(
        ids='ga:5110029',
        start_date=startDate,
        end_date=endDate,
        metrics='ga:bouncerate',
        dimensions='ga:deviceCategory',
        filters='ga:continent==Oceania',

    ).execute()

    France = service.data().ga().get(
        ids='ga:85625764',
        start_date=startDate,
        end_date=endDate,
        metrics='ga:bouncerate',
        dimensions='ga:deviceCategory',
        filters='ga:country==France',

    ).execute()

    return {
            'UK': round(float(UK.get('totalsForAllResults')['ga:bouncerate']), 2),
            'US': round(float(US.get('totalsForAllResults')['ga:bouncerate']), 2),
            'SEA': round(float(SEA.get('totalsForAllResults')['ga:bouncerate']), 2),
            'ANZ': round(float(ANZ.get('totalsForAllResults')['ga:bouncerate']), 2),
            'France': round(float(France.get('totalsForAllResults')['ga:bouncerate']), 2)
        }
#-----------------------------------------------------------------------------------------------------------------------

def get_avgsession_Bysource(service, profile_id, startDate, endDate):

    results = service.data().ga().get(
            ids='ga:' + profile_id,
            start_date=startDate,
            end_date=endDate,
            metrics='ga:avgsessionduration',
            dimensions='ga:channelGrouping',
        ).execute()

    return results

def print_avgsession_Bysource(results):

    result = dict(results.get('rows', [[]]))
    result['Email'] = result.get('(Other)', 0)
    if result.get('(Other)', 0) != 0:
        del result['(Other)']
    return result

#-----------------------------------------------------------------------------------------------------------------------

def get_MobileTablet_avgsession(service, profile_id, startDate, endDate):

    results = service.data().ga().get(
        ids='ga:' + profile_id,
        start_date=startDate,
        end_date=endDate,
        metrics='ga:avgsessionduration',
        dimensions='ga:deviceCategory',
        segment='gaid::-11'
    ).execute()

    return results
#-----------------------------------------------------------------------------------------------------------------------

def get_conversions(service, option, profile_id, startDate, endDate):
    AllTraffic = service.data().ga().get(
        ids='ga:' + profile_id,
        start_date=startDate,
        end_date=endDate,
        metrics='ga:goalCompletionsAll',
        dimensions='ga:channelGrouping' + "," + option,
    ).execute()

    MobileTablet = service.data().ga().get(
        ids='ga:' + profile_id,
        start_date=startDate,
        end_date=endDate,
        metrics='ga:goalCompletionsAll',
        dimensions=option,
        segment='gaid::-11'
    ).execute()

    ReturningUsers = service.data().ga().get(
        ids='ga:' + profile_id,
        start_date=startDate,
        end_date=endDate,
        metrics='ga:goalCompletionsAll',
        dimensions=option,
        segment='gaid::-3'
    ).execute()

    return {
        'Traffic': AllTraffic,
        'AllTraffic': AllTraffic.get('totalsForAllResults')['ga:goalCompletionsAll'],
        'MobileTablet': MobileTablet.get('totalsForAllResults')['ga:goalCompletionsAll'],
        'ReturningUsers': ReturningUsers.get('totalsForAllResults')['ga:goalCompletionsAll']
    }

#-----------------------------------------------------------------------------------------------------------------------

def print_conversions(results):
    def new_result(result):
        l = {"option": result[1], 'Email' if result[0] == '(Other)' else result[0]: result[2]}
        return l

    results = itertools.groupby(sorted(list(map(new_result, results)), key=itemgetter('option')),
                                key=lambda x: x['option'])
    result = []
    for key, item in results:
        result.append(dict(ChainMap(*list(item))))
    return result
#-----------------------------------------------------------------------------------------------------------------------

class mainClass:

    def __init__(self, start_date, end_date, service):

        self.start_date = start_date
        self.end_date = end_date
        self.service = service

    @staticmethod
    def group(res, keys):
        res_data = []
        new = {}
        for key in keys:
            if key != 'country' and key != 'date':
                x = 0
                for data in res:
                    x += int(float(data.get(key, 0)))
                new[key] = x
        res_data.append(new)
        return res_data

    def top_key_words(self):
        profile_ids = [('5110029', 'UK'), ('84906789', 'USA'), ('85625764', 'France'), ('88496086', 'China')]

        lst = [[], [], [], [], []]
        for profile_id in profile_ids:
            results = get_top_keywords(self.service, profile_id[0], self.start_date, self.end_date)
            lst[0].append(int(results[0].get('totalsForAllResults')['ga:sessions']))
            lst[1].append(float(results[1].get('totalsForAllResults')['ga:bouncerate']))
            lst[2].append(float(results[2].get('totalsForAllResults')['ga:goalconversionrateall']))
            lst[3].append(float(results[3].get('totalsForAllResults')['ga:goalconversionrateall']))
            lst[4].append(float(results[4].get('totalsForAllResults')['ga:avgsessionduration']))
        res_data = [
            {
                'MobileTablet': sum(lst[0]), 'BounceRate': sum(lst[1])/4,
                'ReturningConversions': sum(lst[2])/4, 'UniqueConversions': sum(lst[3])/4,
                'SessionDuration': sum(lst[4])/4
            }
        ]

        return res_data

    def sessions(self, option):
        session = [
            ('5110029', 'United Kingdom'),
            ('84906789', 'United States,ga:country==Canada'),
            ('85625764', 'France'),
            ('88496086', 'China'),
            ('5110029', 'India'),
            ('5110029', 'SEA'),
            ('5110029', 'ANZ'),
            ('5110029', 'ROW'),
            ('84906789', 'ROWUSA')
        ]

        option = "ga:" + option
        sessions_category = []
        goalconversions = []
        for profile_id in session:
            result = get_sessions(self.service, option, profile_id[0], profile_id[1], self.start_date, self.end_date)[0]
            result2 = get_sessions(self.service, option, profile_id[0], profile_id[1], self.start_date, self.end_date)[1]
            goalconversions.append(int(result2.get('totalsForAllResults')['ga:goalCompletionsAll']))
            sessions = print_sessions(result, profile_id[1])
            sessions_category.append(sessions)

        newlist = []
        for i, j in zip(sessions_category[-1], sessions_category[-2]):
            new_dict = {
                'Country': "ROW",
                'Paid Search': int(i.get('Paid Search', 0)) + int(j.get('Paid Search', 0)),
                'Direct': int(i.get('Direct', 0)) + int(j.get('Direct', 0)),
                'Social': int(i.get('Social', 0)) + int(j.get('Social', 0)),
                'Organic Search': int(i.get('Organic Search', 0)) + int(j.get('Organic Search', 0)),
                'Referral': int(i.get('Referral', 0)) + int(j.get('Referral', 0)),
                'Email': int(i.get('Email', 0)) + int(j.get('Email', 0)),
            }
            newlist.append(new_dict)

        del sessions_category[-1]
        del sessions_category[-1]
        sessions_category.append(newlist)
        return sessions_category,goalconversions

    def agents(self):
        agent = [
            ('5110029', 'UKPortfolio'),
            ('84906789', 'USAPortfolio'),
            ('85625764', 'FrancePortfolio'),
            ('88496086', 'ChinaPortfolio'),
        ]

        agent_list = []
        for profile_id in agent:
            result = get_agents(self.service, profile_id[0], self.start_date, self.end_date)
            result = print_agents(result)
            agent_list.append(result)
        keys = ['CallClick', 'EmailClick', 'Click']
        res_data = self.group(agent_list, keys)
        return res_data

    def side_button(self):
        sidebtn = [
            ('5110029', 'UKSideBtn'),
            ('84906789', 'USASideBtn'),
            ('85625764', 'FranceSideBtn'),
            ('88496086', 'ChinaSideBtn'),
        ]

        sidebtn_list = []
        for profile_id in sidebtn:
            result = get_sidebtn(self.service, profile_id[0], self.start_date, self.end_date)
            result = print_sidebtn(result)
            sidebtn_list.append(result)

        keys = ['Help', 'RecentlyViewedPortfolios']
        res_data = self.group(sidebtn_list, keys)
        return res_data

    def portfolio(self):
        portfolio = [
            ('5110029', 'UKPortfolio'),
            ('84906789', 'USAPortfolio'),
            ('85625764', 'FrancePortfolio'),
            ('88496086', 'ChinaPortfolio'),
        ]

        portfolio_list = []
        for profile_id in portfolio:
            result = get_portpolio(self.service, profile_id[0], self.start_date, self.end_date)
            result = print_portpolio(result)
            portfolio_list.append(result)
        keys = ['EmailClick', 'CallClick', 'VideoImgClick', 'PDFClick']
        res_data = self.group(portfolio_list, keys)
        return res_data

    def events(self):

        events = [('5110029', 'UKEvents'), ('84906789', 'USAEvents'), ('85625764', 'FranceEvents'),
                  ('88496086', 'ChinaEvents')]

        event_list = []
        for profile_id in events:
            result = get_events(self.service, profile_id[0], self.start_date, self.end_date)
            result = print_events(result, profile_id[1])
            event_list.append(result)

        return event_list

    def devices(self):
        devices = [('5110029', 'UKDevice'), ('84906789', 'USADevice')]

        device_list = []
        for profile_id in devices:
            result = get_devices(self.service, profile_id[0], self.start_date, self.end_date)
            result = print_devices(result)
            device_list.append(result)

        keys = ['mobile', 'desktop', 'tablet']
        res_data = self.group(device_list, keys)
        return res_data

    def device_sessions(self):
        devices_sessions = [('5110029', 'UK'), ('84906789', 'USA'), ('85625764', 'France'),
                            ('88496086', 'China')]

        session_list = []
        for profile_id in devices_sessions:
            result = get_devices_sessions(self.service, profile_id[0], self.start_date, self.end_date)
            result = print_devices_sessions(result, profile_id[1])
            session_list.append(result)
        return session_list

    def cpc(self):
        cpc = [('5110029', 'UKCPC'), ('84906789', 'USACPC')]

        cpc_list = []
        for profile_id in cpc:
            result = get_CPC(self.service, profile_id[0], self.start_date, self.end_date)
            result = print_CPC(result)
            cpc_list.append(result)
        keys = ['facebookads', 'google', 'Instagram', 'Bingads']
        res_data = self.group(cpc_list, keys)
        return res_data

    def all_traffic(self, option):

        option = "ga:" + option

        allTrafficSession = [
            ('5110029', 'United Kingdom'),
            ('84906789', 'United States,ga:country==Canada'),
            ('85625764', 'France'),
            ('88496086', 'China'),
        ]

        AllTraffic = []
        for profile_id in allTrafficSession:
            results = getAllTraffic(self.service, option, profile_id[0], self.start_date, self.end_date)
            all_traffic = print_Trafiic(results)
            AllTraffic.append(all_traffic)
        AllTraffic_data = []
        for i, j, k, l in zip(AllTraffic[0], AllTraffic[1], AllTraffic[2], AllTraffic[3]):
            new = {'option': i['option'], 'All Traffic': int(i['traffic'])+int(j['traffic'])+int(k['traffic'])+int(l['traffic'])}
            AllTraffic_data.append(new)
        return AllTraffic_data

    def MobileTabletTraffic(self, option):

        option = "ga:" + option

        profile_ids = [
            ('5110029', 'United Kingdom'),
            ('84906789', 'United States,ga:country==Canada'),
            ('85625764', 'France'),
            ('88496086', 'China'),
        ]

        traffic = []
        for profile_id in profile_ids:
            results = get_MobileTabletTraffic(self.service, option, profile_id[0], self.start_date, self.end_date)
            results = print_Trafiic(results)
            traffic.append(results)
        res_data = []
        for i, j, k, l in zip(traffic[0], traffic[1], traffic[2], traffic[3]):
            new = {'option': i['option'],
                   'traffic': int(i['traffic']) + int(i['traffic']) + int(i['traffic']) + int(i['traffic'])}
            res_data.append(new)

        return res_data

    def returning_users(self, option):

        option = "ga:" + option

        profile_ids = [
            ('5110029', 'United Kingdom'),
            ('84906789', 'United States,ga:country==Canada'),
            ('85625764', 'France'),
            ('88496086', 'China'),
        ]

        traffic = []
        for profile_id in profile_ids:
            results = get_return_users(self.service, option, profile_id[0], self.start_date, self.end_date)
            results = print_Trafiic(results)
            traffic.append(results)

        res_data = []
        for i, j, k, l in zip(traffic[0], traffic[1], traffic[2], traffic[3]):
            new = {'option': i['option'],
                   'traffic': int(i['traffic']) + int(i['traffic']) + int(i['traffic']) + int(i['traffic'])}
            res_data.append(new)

        return res_data

    def bouncerate(self):

        profile_ids = [
            ('5110029', 'United Kingdom'),
            ('84906789', 'United States,ga:country==Canada'),
            ('85625764', 'France'),
            ('88496086', 'China'),
        ]
        Byregion = get_region_bouncerate(self.service, self.start_date, self.end_date)
        BySource = []
        for profile_id in profile_ids:
            bysource = get_bouncerate_Bysource(self.service, profile_id[0], self.start_date, self.end_date)
            result = print_bouncerate_Bysource(bysource)
            BySource.append(result)
        keys = ['Direct', 'Organic Search', 'Paid Search', 'Referral', 'Social', 'Email']
        new = {}
        for key in keys:
            x = 0
            for data in BySource:
                x += int(float(data.get(key, 0)))
            new[key] = x/4

        BySource = new
        mobile_tablet = []
        for profile_id in profile_ids:
            MobileTablet = get_MobileTablet_bouncerate(self.service, profile_id[0], self.start_date, self.end_date)
            mobile_tablet.append(float(MobileTablet.get('totalsForAllResults')['ga:bouncerate']))
        mobile_tablet = {'MobileTablet': sum(mobile_tablet)/4}

        def update(d, other):
            d.update(other); return d
        result = reduce(update, (Byregion, BySource, mobile_tablet), {})
        return result

    def avg_session_duration(self):

        profile_ids = [
            ('5110029', 'United Kingdom'),
            ('84906789', 'United States,ga:country==Canada'),
            ('85625764', 'France'),
            ('88496086', 'China'),
        ]
        Byregion = get_region_avgsession(self.service, self.start_date, self.end_date)
        BySource = []
        for profile_id in profile_ids:
            bysource = get_avgsession_Bysource(self.service, profile_id[0], self.start_date, self.end_date)
            result = print_avgsession_Bysource(bysource)
            BySource.append(result)
        keys = ['Direct', 'Organic Search', 'Paid Search', 'Referral', 'Social', 'Email']
        new = {}
        for key in keys:
            x = 0
            for data in BySource:
                x += int(float(data.get(key, 0)))
            new[key] = x/4

        BySource = new
        mobile_tablet = []
        for profile_id in profile_ids:
            MobileTablet = get_MobileTablet_avgsession(self.service, profile_id[0], self.start_date, self.end_date)
            mobile_tablet.append(float(MobileTablet.get('totalsForAllResults')['ga:avgsessionduration']))
        mobile_tablet = {'MobileTablet': sum(mobile_tablet)/4}

        def update(d, other):
            d.update(other); return d
        result = reduce(update, (Byregion, BySource, mobile_tablet), {})
        return result

    def totalConversions(self, option):

        option = "ga:" + option

        profile_ids = [
            ('5110029', 'United Kingdom'),
            ('84906789', 'United States,ga:country==Canada'),
            ('85625764', 'France'),
            ('88496086', 'China'),
        ]

        AllTraffic, MobileTablet, ReturningUsers, conversion = [], [], [], []

        for profile_id in profile_ids:
            results = get_conversions(self.service, option, profile_id[0], self.start_date, self.end_date)
            conversions = print_conversions(results.get('Traffic')['rows'])
            conversion.append(conversions[0])
            AllTraffic.append(int(results.get('AllTraffic', [["", ""]])))
            MobileTablet.append(int(results.get('MobileTablet', [["", ""]])))
            ReturningUsers.append(int(results.get('ReturningUsers', [["", ""]])))

        return {
                "sources": conversion,
                'AllTraffic': sum(AllTraffic),
                'MobileTablet': sum(MobileTablet),
                'ReturningUsers': sum(ReturningUsers)
        }

