# merge newly gathered data to main dataframe to be graphed
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re
import os
from datetime import date


def fix_initial_data(df):
    df = df.drop(columns=['Unnamed: 0'])
    df = df.replace(',', '', regex=True)
    df['Mileage: '] = pd.to_numeric(df['Mileage: '].str.split(" ", 1).str[0], downcast="signed")
    df["Price: "] = pd.to_numeric(df["Price: "], downcast="signed")
    df = df.drop_duplicates() # in case we grabbed same vehicle entry more than once
    return df


if __name__ == '__main__':
    date = str(date.today())

    # create backup of main w/ date
    df1 = pd.read_csv('main_df.csv')     # open old main_df
    backup_name = str(date) + ' main_df backup.csv'
    df1.to_csv(backup_name)    # save back up of old main_df as data+ main_df.csv

    # move backup to backup folder
    init_folder = "./" + backup_name
    dest_folder = "./main df backups/" + backup_name
    os.replace(init_folder, dest_folder)

    df3 = df1
    # Open NEW DF as df2
    for file in os.listdir():
        print(str(file))
        if file.endswith("carvana_data.csv"):
            df2 = pd.read_csv(file)
            # move file out of main folder and into the 'raw gathered data folder'
            os.replace("./" + str(file),
                       "./raw gathered data/" + str(file))
            df2 = fix_initial_data(df2)
            df3 = pd.concat([df3, df2])

    print(df1)
    print(df2)
    print(df3)

    # save df3 as main_df.csv
    df3.to_csv('mainy_df.csv')
