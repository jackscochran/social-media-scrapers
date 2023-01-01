from cmath import nan
import datetime

import pandas as pd

def format_instagram_date(date_string):
    if not isinstance(date_string, str) or date_string == 'N/A':
        return 'N/A'

    if 'AGO' in date_string:
        if 'MINUTE' in date_string or 'HOUR' in date_string:
            date = str(datetime.date.today())
        else:
            date = str(datetime.date.today() - datetime.timedelta(days=int(date_string.split(' ')[0])))
    else:
        if len(date_string.split(' ')) == 2:
            date_string += ', 2022'

        date = str(datetime.datetime.strptime(date_string, '%B %d, %Y').date())

    return date

def format_instagram_interactions(string):
    if string =='N/A' or len(string.split(' ')) > 2:
        return 'N/A'

    return int(string.replace(',','').split(' ')[0])

def format_tiktok_date(date_string):

    if not isinstance(date_string, str) or date_string == 'N/A':
        return 'N/A'

    date_string = date_string.split('\n')[2]

    if 'ago' in date_string:
        if date_string[1] == 'd':
            date = str(datetime.date.today() - datetime.timedelta(days=int(date_string[0])))
        elif date_string[1] == 'w':
            date = str(datetime.date.today() - datetime.timedelta(weeks=int(date_string[0])))
        else:
            date = str(datetime.date.today()) # hours or minutes
    else:
        if len(date_string.split('-')) == 2:
            date_string = '2022-' + date_string

        date = str(datetime.datetime.strptime(date_string, '%Y-%m-%d').date())

    return date

def format_big_num(num_string):

        if isinstance(num_string, float):
            return num_string
    
        if num_string == 'N/A' or num_string == '':
            return 'N/A'

        num_string = num_string.split(' ')[0]

        if num_string == "Vote":
            return 0
    
        if 'K' in num_string:
            num = int(float(num_string.replace('K','')) * 1000)
        elif 'k' in num_string:
            num = int(float(num_string.replace('k','')) * 1000)
        elif 'M' in num_string:
            num = int(float(num_string.replace('M','')) * 1000000)
        elif 'm' in num_string:
            num = int(float(num_string.replace('m','')) * 1000000)
        else:
            num = int(num_string.replace(',',''))
    
        return num

def format_youtube_date(date_string):
    if not isinstance(date_string, str) or date_string == 'N/A':
            return 'N/A'

    if 'day' in date_string:
        date = str(datetime.date.today() - datetime.timedelta(days=int(date_string.split(' ')[0])))

    elif 'week' in date_string:
        date = str(datetime.date.today() - datetime.timedelta(weeks=int(date_string.split(' ')[0])))

    elif 'month' in date_string:
        date = str(datetime.date.today() - datetime.timedelta(months=int(date_string.split(' ')[0])))

    elif 'year' in date_string:
        date = str(datetime.date.today() - datetime.timedelta(years=int(date_string.split(' ')[0])))

    return date

if __name__ == '__main__':
    df = pd.read_csv('instagram_data.csv')
    df['date_posted'] = df['date_posted'].apply(convert_instagram_date)
    df['num_of_likes'] = df['num_of_likes'].apply(convert_instagram_interactions)
    df.to_csv('instagram_data_clean.csv', index=False)
