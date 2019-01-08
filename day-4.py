'''
day4: response record


load data - convert timestamps *
sort logs *
filter logs in midnight
compile by guard
'''
from typing import NamedTuple
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import pandas as pd # kinda shameful
# ^ also didnt work
import re

reg = '([[0-9].*]) (.*[a-z])' 

with open('data/data-day4.txt') as f:
    data = [l.strip('\n') for l in f.readlines()]

class Event(NamedTuple):
    time_stamp: datetime
    desc: str

    @staticmethod
    def from_str(event):

        def parse_date(event):
            return datetime.strptime(event, '[%Y-%m-%d %H:%M]')

        timestamp,desc = re.match(reg, event).groups()
        return parse_date(timestamp), desc 

assert Event.from_str('[1518-11-01 23:58] Guard #907 begins shift') == \
        Event(datetime(1518,11,1,23,58),'Guard #907 begins shift')


events_raw = [Event.from_str(dat_str) for dat_str in data]

def sort_filter(events):
    ordered = sorted(events,key = lambda tup: tup[0])
    return list( ordered )
events = sort_filter(events_raw)

guards = defaultdict()
for (i,(timestamp, event)) in enumerate(events):
    if event.find('#') >= 0:
        i +=1
        # hack string extract
        guard = [int(i)  
                 for i in  event.replace('#','').split(' ') 
                 if i.isdigit() ==True][0]
        if guard not in guards.keys():
            guards[guard] = {'sleep':[],'wake':[]}
        try: 
            while events[i][1].find('#') < 1:
                evt = events[i][1]
                tmsp = events[i][0]
                if evt.find('sleep') >= 0:
                    guards[guard]['sleep'].append(tmsp)
                if evt.find('wake') >= 0:
                    guards[guard]['wake'].append(tmsp)
                i+=1
        except IndexError:
            pass

def guard_sleep(guard):
    g = guards[guard]
    sleep = g['sleep']
    wake = g['wake']
    for s,w in zip(sleep,wake):
        start = s.minute
        duration = (w - s).seconds // 60
        minutes = list(range(start,start+duration))
        m = list(filter(lambda x: x <= 59, minutes))
        # print(f'{s}----------duration: {(w - s)}')
        # print(m)

        if 'minutes' not in guards[guard].keys():
            guards[guard]['minutes'] = []
        
        [guards[guard]['minutes'].append(i) for i in m]

[ guard_sleep(guard) for guard in guards.keys() ]

answers = []
for guard in guards.keys():
    c = Counter(guards[guard]['minutes'])
    answers.append((guard,c.most_common(1),len(guards[guard]['minutes'])))

    print(f'''
        guard: {guard} 
        total: {len(guards[guard]['minutes'])}
        most asleep{c.most_common(3)}''')

answers = answers.sort(key=lambda x: x[2])

# use pandas to do filtering and aggregation
# def manipulate_dataframe(events):

#     df = pd.DataFrame.from_dict(
#         {'time': [e[0] for e in events],'event':[e[1] for e in events]} 
#     )
#     # df.index = df.time
#     # df['guard'] = df.event.str.extract('(Guard #[1-9]* )')
#     # df.guard.fillna(method='ffill',inplace=True)
#     # df['hour'] =  df.time.apply(lambda x: x.hour)
#     # df['minute']  = df.time.apply(lambda x: x.minute)
#     return df
# df = manipulate_dataframe(events)