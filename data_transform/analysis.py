from os import stat
import pandas as pd

import math

import util

def convert_date_to_years(date):

    if not isinstance(date, str):
        return "N/A"

    if "Streamed" in date:
        return int(date[9])

    if "year" in date:
        return int(date.split(" ")[0])

    return 0

def aggregate_reddit_data():

    def get_stats(filename):
        df = pd.read_csv(filename)

        df = df[df.promotion == False]

        df["upvotes"] = df.apply(lambda row : util.format_big_num(row["upvotes"]), axis=1)
        df["comments"] = df.apply(lambda row : util.format_big_num(row["comments"]), axis=1)

        stats = {}

        stats['average_upvotes'] = [df['upvotes'].mean()]
        stats['median_upvotes'] = [df['upvotes'].median()]
        stats['max_upvotes'] = [df['upvotes'].max()]
        stats['num_of_posts'] = [len(df)]
        stats['num_of_athors'] = [len(df['author'].unique())]
        stats['average_comments'] = [df['comments'].mean()]
        stats['median_comments'] = [df['comments'].median()]
        stats['max_comments'] = [df['comments'].max()]
        stats['sort'] = [filename.split("/")[3]]
        stats['keyword'] = [filename.split("/")[4]]
        stats['years_back'] = ['all']

        df['years_ago'] = df.apply(lambda row: convert_date_to_years(row["date"]), axis=1)
        
        for i in range(12):
            yearly_df = df[df["years_ago"] == i]

            stats['average_upvotes'].append(yearly_df['upvotes'].mean())
            stats['median_upvotes'].append(yearly_df['upvotes'].median())
            stats['max_upvotes'].append(yearly_df['upvotes'].max())
            stats['num_of_posts'].append(len(yearly_df))
            stats['num_of_athors'].append(len(yearly_df['author'].unique()))
            stats['average_comments'].append(yearly_df['comments'].mean())
            stats['median_comments'].append(yearly_df['comments'].median())
            stats['max_comments'].append(yearly_df['comments'].max())
            stats['sort'].append(filename.split("/")[3])
            stats['keyword'].append(filename.split("/")[4])
            stats['years_back'].append(i)

        return pd.DataFrame(stats)


    platform = 'reddit'
    filters = ['top', 'new']
    forums = ['fitness', 'nutrition', 'personaltraining']
    searches = ['fitness', 'nutrition', 'personal%20training']

    stats_df = get_stats('output/reddit/home_page/top/explore.csv')

    for forum in forums:
        for filter in filters:
            current_file = f'output/{platform}/forum_page/{filter}/{forum}.csv'
            stats_df = stats_df.append(get_stats(current_file))

    # for search in searches:
    #     for filter in filters:
    #         current_file = f'output/{platform}/search_page/{filter}/{search}.csv'
    #         stats_df = stats_df.append(get_stats(current_file))

    stats_df.to_csv(f'analysis/{platform}/keyword_comparision.csv', index=False)

def aggregate_youtube_data():

    def get_stats(filename):

        df = pd.read_csv(filename)

        stats = {}

        stats['num_of_videos'] = [len(df)]
        stats['num_of_views'] = [df['views'].sum()]
        stats["avg_views_per_video"] = [df['views'].mean()]
        stats["median_views_per_video"] = [df['views'].median()]
        stats["max_views_per_video"] = [df['views'].max()]
        stats['num_of_channels'] = [len(df['channel_name'].unique()) ]
        stats["page"] = [filename.split("/")[2]]
        stats["keyword"] = [filename.split("/")[3]]
        stats['years_back'] = ['all']
        
        df["years_ago"] = df.apply(lambda row: convert_date_to_years(row["date_posted"]), axis=1)

        for i in range(12):
            yearly_df = df[df["years_ago"] == i]

            stats['num_of_videos'].append(len(yearly_df))
            stats['num_of_views'].append(yearly_df['views'].sum())
            stats["avg_views_per_video"].append(yearly_df['views'].mean())
            stats["median_views_per_video"].append(yearly_df['views'].median())
            stats["max_views_per_video"].append(yearly_df['views'].max())
            stats['num_of_channels'].append(len(yearly_df['channel_name'].unique()) )
            stats["page"].append(filename.split("/")[2])
            stats["keyword"].append(filename.split("/")[3])
            stats['years_back'].append(i)

        return pd.DataFrame(stats)


    platform = 'youtube'
    pages = ['upload_date', 'top_viewed']
    keywords = ['fitness', 'fitness+certification', 'fitness+certification+training', 'nutrition', 'nutrition+certification', 'nutrition+certification+training']

    stats_df = get_stats('output/youtube/explore/explore.csv')

    for keyword in keywords:
        for page in pages:
            current_file = f'output/{platform}/{page}/{keyword}.csv'
            stats_df = stats_df.append(get_stats(current_file))

    stats_df.to_csv(f'analysis/{platform}/keyword_comparision.csv', index=False)

def aggregate_instagram_data():

    def convert_date_to_years(date):
        if not isinstance(date, str):
            return 'N/A'

        return 2022 - int(date[:4])

    def get_stats(filename):
        
        df = pd.read_csv(filename)

        stats = {}

        stats['num_of_posts'] = [len(df)]
        stats['num_of_videos'] = [len(df[df['is_video'] == True])]
        stats['num_of_images'] = [len(df[df['is_video'] == False])]
        stats['num_of_accounts'] = [len(df['account'].unique())]

        stats['avg_num_of_likes'] = [df[df['is_video'] == False]['num_of_interactions'].mean()]
        stats['median_num_of_likes'] = [df[df['is_video'] == False]['num_of_interactions'].median()]

        stats['avg_num_of_views'] = [df[df['is_video'] == True]['num_of_interactions'].mean()]
        stats['median_num_of_views'] = [df[df['is_video'] == True]['num_of_interactions'].median()]

        stats['page'] = [filename.split("/")[2]]
        stats['keyword'] = [filename.split("/")[3]]
        stats['years_back'] = ['all']

        df["years_ago"] = df.apply(lambda row: convert_date_to_years(row["date_posted"]), axis=1)

        for i in range(12):
            yearly_df = df[df["years_ago"] == i]

            stats['num_of_posts'].append(len(yearly_df))
            stats['num_of_videos'].append(len(yearly_df[yearly_df['is_video'] == True]))
            stats['num_of_images'].append(len(yearly_df[yearly_df['is_video'] == False]))
            stats['num_of_accounts'].append(len(yearly_df['account'].unique()))

            stats['avg_num_of_likes'].append(yearly_df[yearly_df['is_video'] == False]['num_of_interactions'].mean())
            stats['median_num_of_likes'].append(yearly_df[yearly_df['is_video'] == False]['num_of_interactions'].median())

            stats['avg_num_of_views'].append(yearly_df[yearly_df['is_video'] == True]['num_of_interactions'].mean())
            stats['median_num_of_views'].append(yearly_df[yearly_df['is_video'] == True]['num_of_interactions'].median())

            stats['page'].append(filename.split("/")[2])
            stats['keyword'].append(filename.split("/")[3])
            stats['years_back'].append(i)

        return pd.DataFrame(stats)

    platform = 'instagram'
    pages = ['explore', 'search']
    keywords = ['fitness', 'nutrition']

    stats_df = get_stats('output/instagram/explore/explore.csv')

    for keyword in keywords:
        for page in pages:
            current_file = f'output/{platform}/{page}/{keyword}.csv'
            stats_df = stats_df.append(get_stats(current_file))

    stats_df.to_csv(f'analysis/{platform}/keyword_comparision.csv', index=False)

def gather_youtube_data():

    def format_df(file):
        df = pd.read_csv(file)
        df['page'] = file.split("/")[2]
        df['keyword'] = file.split("/")[3]
        return df
    
    platform = 'youtube'
    pages = ['upload_date', 'top_viewed']
    keywords = ['fitness', 'fitness+certification', 'fitness+certification+training', 'nutrition', 'nutrition+certification', 'nutrition+certification+training']

    stats_df = format_df('output/youtube/explore/explore.csv')

    for keyword in keywords:
        for page in pages:
            current_file = f'output/{platform}/{page}/{keyword}.csv'
            stats_df = stats_df.append(format_df(current_file))

    stats_df["years_ago"] = stats_df.apply(lambda row: convert_date_to_years(row["date_posted"]), axis=1)

    stats_df.to_csv(f'analysis/{platform}/keyword_comparision.csv', index=False)

def gather_reddit_data():
    
        def format_df(file):
            df = pd.read_csv(file)
            df['page'] = file.split("/")[2]
            df['sort'] = file.split("/")[3]
            df['keyword'] = file.split("/")[4]
            return df
        
        platform = 'reddit'
        filters = ['top', 'new']
        forums = ['fitness', 'nutrition', 'personaltraining']
        searches = ['fitness', 'nutrition', 'personal%20training']
    
        stats_df = format_df('output/reddit/home_page/top/explore.csv')
        stats_df = stats_df.append(format_df('output/reddit/home_page/new/explore.csv'))
    
        for forum in forums:
            for filter in filters:
                current_file = f'output/{platform}/forum_page/{filter}/{forum}.csv'
                stats_df = stats_df.append(format_df(current_file))

        for search in searches:
            for filter in filters:
                current_file = f'output/{platform}/search_page/{filter}/{search}.csv'
                stats_df = stats_df.append(format_df(current_file))
    
        stats_df["years_ago"] = stats_df.apply(lambda row: convert_date_to_years(row["date"]), axis=1)
        stats_df["upvotes"] = stats_df.apply(lambda row : util.format_big_num(row["upvotes"]), axis=1)
        stats_df["comments"] = stats_df.apply(lambda row : util.format_big_num(row["comments"]), axis=1)

    
        stats_df.to_csv(f'analysis/{platform}/keyword_comparision.csv', index=False)

def gather_instagram_data():
    def convert_date_to_years(date):
        if not isinstance(date, str):
            return 'N/A'

        return 2022 - int(date[:4])

    def format_df(file):
        df = pd.read_csv(file)
        df['page'] = file.split("/")[2]
        df['keyword'] = file.split("/")[3]
        return df
    
    platform = 'instagram'
    pages = ['explore', 'search', "tags"]
    keywords = ['fitness', 'nutrition']
    
    stats_df = format_df('output/instagram/explore/explore.csv')
    stats_df = stats_df.append(format_df('output/instagram/explore/fitness-2.csv'))
    stats_df = stats_df.append(format_df('output/instagram/search/personal%20training.csv'))
    
    for keyword in keywords:
        for page in pages:
            current_file = f'output/{platform}/{page}/{keyword}.csv'
            stats_df = stats_df.append(format_df(current_file))
    
    stats_df["years_ago"] = stats_df.apply(lambda row: convert_date_to_years(row["date_posted"]), axis=1)
    
    stats_df.to_csv(f'analysis/{platform}/keyword_comparision.csv', index=False)

def gather_tiktok_data():
    def format_df(file):
        df = pd.read_csv(file)
        df['keyword'] = file.split("/")[2]
        return df
    
    platform = 'tiktok'
    keywords = ['fitness', 'nutrition', 'fitness+certification', 'nutrition+certification', 'personal+training']
    
    stats_df = format_df(f'output/tiktok/{keywords[0]}.csv')
    
    for i in range(1, len(keywords)):
        current_file = f'output/{platform}/{keywords[i]}.csv'
        stats_df = stats_df.append(format_df(current_file))
        
    stats_df.to_csv(f'analysis/{platform}/keyword_comparision.csv', index=False)

def gather_all_data():
    df = {
        'years_ago': [],
        'interactions': [],
        'measure': [],
        'platform': [],
        'keyword': []
    }

    # youtube

    youtube_df = pd.read_csv('analysis/youtube/keyword_comparision.csv')
    df ['years_ago'] += youtube_df['years_ago'].tolist()
    df ['interactions'] += youtube_df['views'].tolist()
    df ['measure'] += ['views'] * len(youtube_df)
    df ['platform'] += ['youtube'] * len(youtube_df)
    df ['keyword'] += youtube_df['keyword'].tolist()

    # instagram
    instagram_df = pd.read_csv('analysis/instagram/keyword_comparision.csv')
    instagram_df = instagram_df[instagram_df['page'] == 'search']
    likes_df = instagram_df[instagram_df['is_video'] == False]
    df ['years_ago'] += likes_df['years_ago'].tolist()
    df ['interactions'] += likes_df['num_of_interactions'].tolist()
    df ['measure'] += ['likes'] * len(likes_df)
    df ['platform'] += ['instagram'] * len(likes_df)
    df ['keyword'] += likes_df['keyword'].tolist()

    videos_df = instagram_df[instagram_df['is_video'] == True]
    df ['years_ago'] += videos_df['years_ago'].tolist()
    df ['interactions'] += videos_df['num_of_interactions'].tolist()
    df ['measure'] += ['views'] * len(videos_df)
    df ['platform'] += ['instagram'] * len(videos_df)
    df ['keyword'] += videos_df['keyword'].tolist()

    # reddit
    reddit_df = pd.read_csv('analysis/reddit/keyword_comparision.csv')
    reddit_df = reddit_df[reddit_df['promotion'] == False]    
    reddit_df = reddit_df[reddit_df['page'] == 'search_page']
    reddit_df = reddit_df[reddit_df['sort'] == 'top']
    
    df ['years_ago'] += reddit_df['years_ago'].tolist()
    df ['interactions'] += reddit_df['upvotes'].tolist()
    df ['measure'] += ['upvotes'] * len(reddit_df)
    df ['platform'] += ['reddit'] * len(reddit_df)
    df ['keyword'] += reddit_df['keyword'].tolist()

    df ['years_ago'] += reddit_df['years_ago'].tolist()
    df ['interactions'] += reddit_df['comments'].tolist()
    df ['measure'] += ['comments'] * len(reddit_df)
    df ['platform'] += ['reddit'] * len(reddit_df)
    df ['keyword'] += reddit_df['keyword'].tolist()

    # tiktok
    tiktok_df = pd.read_csv('analysis/tiktok/keyword_comparision.csv')
    df ['years_ago'] += tiktok_df['date'].tolist()
    df ['interactions'] += tiktok_df['num_of_likes'].tolist()
    df ['measure'] += ['likes'] * len(tiktok_df)
    df ['platform'] += ['tiktok'] * len(tiktok_df)
    df ['keyword'] += tiktok_df['keyword'].tolist()

    df ['years_ago'] += tiktok_df['date'].tolist()
    df ['interactions'] += tiktok_df['num_of_comments'].tolist()
    df ['measure'] += ['comments'] * len(tiktok_df)
    df ['platform'] += ['tiktok'] * len(tiktok_df)
    df ['keyword'] += tiktok_df['keyword'].tolist()

    pd.DataFrame(df).to_csv('analysis/keyword_comparision.csv', index=False)

if __name__ == '__main__':
    
    gather_youtube_data()
    gather_reddit_data()
    gather_instagram_data()
    gather_tiktok_data()
    gather_all_data()
