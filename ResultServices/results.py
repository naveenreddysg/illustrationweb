from get_data import get_Month_data, total_sessions

class SessionsCategoryResults:

    def __init__(self, current_results, previous_results, option):
        self.current_results = current_results
        self.previous_results = previous_results
        self.option = option

    @staticmethod
    def fix_change(k, l):
        change = round((((float(k['TotalSessions']) - float(l['TotalSessions']))
                    /float(l['TotalSessions'])) * 100), 2)

        change = 100 if change > 100 else change
        return str(change)+'%'

    @staticmethod
    def mapping(results):
        i = 0
        new_results = []
        length = len(results[0])
        if len(results[0]) == 31:
            length = 30
        while i < length:
            new = [item[i] for item in results]
            new_results.append(new)
            i += 1
        return new_results

    @staticmethod
    def get_totalsessions_total(total_sessions):
        total = 0
        for data in total_sessions:
            total += int(data['TotalSessions'])
        total_sessions.append({'Country': 'Total', 'TotalSessions': total})
        return total_sessions

    @staticmethod
    def total(result, country):
        res_data = {'Country': country, 'Organic Search': 0, 'Direct': 0, 'Paid Search': 0, 'Referral': 0, 'Social': 0, 'Email': 0}
        for item in result:
            res_data['Organic Search'] += int(item.get('Organic Search', 0))
            res_data['Direct'] += int(item.get('Direct', 0))
            res_data['Paid Search'] += int(item.get('Paid Search', 0))
            res_data['Referral'] += int(item.get('Referral', 0))
            res_data['Social'] += int(item.get('Social', 0))
            res_data['Email'] += int(item.get('Email', 0))
        return res_data

    @staticmethod
    def change_cal(total1, total2):
        change_dict = {}
        keys = ['Organic Search', 'Direct', 'Paid Search', 'Referral' 'Social', 'Email']
        change_dict['Country'] = 'Change'
        for key, value in total1.items():
            try:
                change = round(((float(total1.get(key, 0))-float(total2.get(key, 0)))/float(total2.get(key,0))) * 100, 2)
                change_dict[key] = str(100 if change > 100 else change) + '%'
            except Exception as e:
                # print e
                pass
        return change_dict

    @staticmethod
    def result(results):
        main_result = [
            {'Country': i.get('Country', 0),
             'Direct': i.get('Direct', 0),
             'Paid Search': i.get('Paid Search', 0),
             'Organic Search': i.get('Organic Search', 0),
             'Referral': i.get('Social', 0),
             'Social': i.get('Referral', 0),
             'Email': i.get('Email', 0)
             }
            for i in results
        ]
        return main_result

    def main(self):
        pre_session_results = self.current_results.sessions(self.option)
        prev_sessions_results = self.previous_results.sessions(self.option)

        keys = ['Country', 'Organic Search', 'Direct', 'Referral', 'Social', 'Paid Search', 'Email']
        pre_total_data = get_Month_data(pre_session_results, keys)
        prev_total_data = get_Month_data(prev_sessions_results, keys)

        pre_TotalSessions_line = total_sessions(pre_session_results)
        prev_TotalSessions_line =total_sessions(prev_sessions_results)

        keys = ['Country', 'TotalSessions']
        pre_TotalSessions = get_Month_data(pre_TotalSessions_line, keys)
        prev_TotalSessions = get_Month_data(prev_TotalSessions_line, keys)
        total_current = self.total(pre_total_data, 'Total')
        total_previous = self.total(prev_total_data, 'Total(Prev)')

        change = self.change_cal(total_current, total_previous)
        pre_total_data.append(total_current)
        pre_total_data.append(total_previous)
        pre_total_data.append(change)

        pre_TotalSessions = self.get_totalsessions_total(pre_TotalSessions)
        prev_TotalSessions = self.get_totalsessions_total(prev_TotalSessions)

        sessions_main_result = [
            {'Country': i[0]['Country'],
             'Current': i[0]['TotalSessions'],
             'Previous': i[1]['TotalSessions'],
             'Change': str(round((((float(i[0]['TotalSessions']) - float(i[1]['TotalSessions']))
                                   / float(i[1]['TotalSessions'])) * 100), 2)) + '%'
             }
            for i in zip(pre_TotalSessions, prev_TotalSessions)
        ]

        new_pre_session_results = self.mapping(pre_session_results)
        new_prev_sessions_results = self.mapping(prev_sessions_results)
        source_change_percentage = []
        for i, j in zip(new_pre_session_results, new_prev_sessions_results):
            total_current = self.total(i, 'Total')
            total_previous = self.total(j, 'Total(Prev)')
            change = self.change_cal(total_current, total_previous)
            source_change_percentage.append([total_current, change])

        total_sessions_line_data = []
        for i, j in zip(pre_TotalSessions_line, prev_TotalSessions_line):
            new = []
            for k, l in zip(i, j):
                change = {
                    'Country': k['Country'],
                    'Total': k['TotalSessions'],
                    'Change': self.fix_change(k, l)
                    }
                new.append(change)
            total_sessions_line_data.append(new)

        return {
            'sessions': {'present': pre_total_data, 'previous': prev_total_data},
            'totalSessions': sessions_main_result,
            'session_category_line_data': source_change_percentage,
            'session_region_line_data': total_sessions_line_data
        }

class WebsiteTrafficResults:

    def __init__(self, current_results, previous_results, option):
        self.current_results = current_results
        self.previous_results = previous_results
        self.option = option

    def main(self):

        pre_Traffic = self.current_results.all_traffic(self.option)
        pre_MobileTabletTraffic = self.current_results.MobileTabletTraffic(self.option)
        pre_returningUsers = self.current_results.returning_users(self.option)

        prev_Traffic = self.previous_results.all_traffic(self.option)
        prev_MobileTabletTraffic = self.previous_results.MobileTabletTraffic(self.option)
        prev_returningUsers = self.previous_results.returning_users(self.option)

        return {
            'AllTraffic': {
                'present':  pre_Traffic,
                'previous': prev_Traffic
            },
            'MobileTabletTraffic': {
                'present': pre_MobileTabletTraffic,
                'previous': prev_MobileTabletTraffic
            },
            'returningusers': {
                'present': pre_returningUsers,
                'previous': prev_returningUsers
            }
        }


class BounceRateResults:

    def __init__(self, current_results, previous_results):
        self.current_results = current_results
        self.previous_results = previous_results

    def main(self):

        pre_bounceRate = self.current_results.bouncerate()
        prev_bounceRate = self.previous_results.bouncerate()

        return {"present": pre_bounceRate, 'previous': prev_bounceRate}

class AvgSessionDuration:

    def __init__(self, current_results, previous_results):
        self.current_results = current_results
        self.previous_results = previous_results

    def main(self):

        pre_AvgSessionDuration = self.current_results.avg_session_duration()
        prev_AvgSessionDuration = self.previous_results.avg_session_duration()

        return {"present": pre_AvgSessionDuration, 'previous': prev_AvgSessionDuration}

class Conversions:

    def __init__(self, current_results, previous_results, option):
        self.current_results = current_results
        self.previous_results = previous_results
        self.option = option

    @staticmethod
    def total(result):
        res_data = {'Organic Search': 0, 'Direct': 0, 'Paid Search': 0, 'Referral': 0, 'Social': 0, 'Email': 0}
        for item in result:
            res_data['Organic Search'] += int(item.get('Organic Search', 0))
            res_data['Direct'] += int(item.get('Direct', 0))
            res_data['Paid Search'] += int(item.get('Paid Search', 0))
            res_data['Referral'] += int(item.get('Referral', 0))
            res_data['Social'] += int(item.get('Social', 0))
            res_data['Email'] += int(item.get('Email', 0))
        return res_data

    def main(self):

        pre_conversions_data = self.current_results.totalConversions(self.option)
        prev_conversions_data = self.previous_results.totalConversions(self.option)

        pre_source = self.total(pre_conversions_data['sources'])
        prev_source = self.total(prev_conversions_data['sources'])

        pre_conversions_data['sources'] = pre_source
        prev_conversions_data['sources'] = prev_source

        return {
            'pre_conversions': pre_conversions_data,
            'prev_conversions': prev_conversions_data
        }