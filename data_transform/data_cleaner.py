import pandas as pd


if __name__ == '__main__':

    filename = "analysis/Youtube/Fitness-Data.csv"

    df = pd.read_csv('data.csv')
    df = df.drop_duplicates(subset=['title', 'channel_name', 'date_posted', 'views'])
    df.to_csv('data.csv', index=False)