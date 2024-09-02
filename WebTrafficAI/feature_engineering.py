import pandas as pd

def feature_engineering(df):
    df['DayOfWeek'] = df['Date'].dt.dayofweek
    df['IsWeekend'] = df['DayOfWeek'].apply(lambda x: 1 if x >= 5 else 0)
    df['PageViews_per_Click'] = df['Page Views'] / df['Clicks']
    df['SessionDuration_per_PageView'] = df['Session Duration'] / df['Page Views']
    return df
