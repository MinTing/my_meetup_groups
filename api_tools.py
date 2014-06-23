'''
To run this tool
you need to have a meetup.com account
and get your own API key from 
https://secure.meetup.com/meetup_api/key/

'''

import requests
import json
import sys
import time

myApiKey='*******' # Put your own api key here
myMemberId='*******' # Put your own member id here

page=200

def get_my_groups(myMemberId):
    url_names=[]
    url='https://api.meetup.com/2/groups/?member_id=%s&sign=true&key=%s&page=%s' % (myMemberId,myApiKey,page)
    r=requests.get(url)
    # print r.text
    data=json.loads(r.text)
    if not 'results' in data:
        print 'something is not right'
        return
    results=data['results']
    for item in results:
        url_names.append(item['urlname'])
    print url_names
    return url_names

def get_member_records(groupURLName,field='joined'):
    records=[]
    offset=0
    no_error=True
    while no_error:
        try:        
            url='https://api.meetup.com/2/members/?group_urlname=%s&sign=true&key=%s&page=%s&offset=%s' % (groupURLName,myApiKey,page,offset)
            r=requests.get(url)
            data=json.loads(r.text)
            if not 'results' in data:
                print 'something is not right'
                return records.sort()
            results=data['results']
            if not len(results):
                break
            # field='bio'
            for item in results:
                records.append(item.get(field))
            offset+=1
        except TypeError:
            no_error=False
    records.sort()
    return records

def get_monthly_join(groupURLName):
    month_length=1000*3600*24*30
    join_times=get_member_records(groupURLName,'joined')
    start_time=join_times[0]
    current_month=start_time+month_length
    count=0
    cur_year=display_yr_mth(join_times[0]/1000)[0]
    cur_month=display_yr_mth(join_times[0]/1000)[1]
    for join_time in join_times:
        if join_time>current_month:
            print 'Year: ',cur_year, 'Month:',cur_month,'Joined:', count
            current_month+=month_length
            count=0
            cur_year=display_yr_mth(join_time/1000)[0]
            cur_month=display_yr_mth(join_time/1000)[1]
        else:
            count+=1

def display_yr_mth(sec):
    T=time.gmtime(sec)
    yr=T[0]
    mth=T[1]
    return [yr, mth]


def main():
    # print get_member_records('karaoke-88')
    url_names=get_my_groups(myMemberId)
    for group_name in url_names:
        print '\n',group_name
        get_monthly_join(group_name)

if __name__ == '__main__':
    main()