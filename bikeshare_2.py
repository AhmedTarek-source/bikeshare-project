import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def check_input(input_str, input_type):
    """
    check the validity of user input.
    input_str: is the input of the user
    input_type: is the type of input: 1 = city, 2 = month, 3 = day
    """
    while True:
        input_read = input(input_str)
        try:
            if input_read in ['chicago', 'new york city', 'washington'] and input_type == 1:
                break
            elif input_read in ['january', 'february', 'march', 'april', 'may', 'june', 'all'] and input_type == 2:
                break
            elif input_read in ['sunday', 'monday', 'tuseday', 'wednesday', 'thursday', 'friday', 'saturday', 'all'] and input_type == 3:
                break
            else:
                if input_type == 1:
                    print('city not included, please choose from the cities provided')
                if input_type == 2:
                    print('month not included, please choose from months provided')
                if input_type == 3:
                    print('error please choose a day')
        except ValueError:
            print('Error, please enter a correct input' )
    return input_read

def get_filters():
    print('Hello! Let\'s explore some US bikeshare data!\n')
    city = check_input('Please choose which city you would like to get your information from (chicago, new york city, washington)\n',1)
    month = check_input('Please choose which month (january, february, march, april, may, june, all)\n',2)
    day = check_input('Please choose which day or all\n',3)
    print('='*100)
    return city, month, day

def load_data(city, month, day):
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1

        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df

def popular_time_of_travel(df):
    start_time = time.time()
    most_common_month = df['month'].mode()[0]
    print('Most common month =', most_common_month)
    most_common_day_of_week = df['day_of_week'].mode()[0]
    print('Most common day of week:', most_common_day_of_week)
    most_common_hour_of_day = df['hour'].mode()[0]
    print('Most common hour of day: {}:00'.format(most_common_hour_of_day))

    print('\nTime taken to get this information is {} seconds'.format(time.time() - start_time))
    print('='*100)

def popular_stations_and_trips(df):
    start_time = time.time()
    most_common_start_station = df['Start Station'].mode()[0]
    print('Most common start station is:', most_common_start_station)
    most_common_end_station = df['End Station'].mode()[0]
    print('Most common end station is:', most_common_end_station)
    start_end = df.groupby(['Start Station','End Station'])
    most_common_trip_from_start_to_end = start_end.size().sort_values(ascending = False).head(1)
    print('Most common trip from start to end is:\n from:                      to:                   times repeated:\n', most_common_trip_from_start_to_end)

    print('\nTime taken to get this information is {} seconds'.format(time.time() - start_time))
    print('='*100)

def trip_duration(df):
    start_time = time.time()
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time = {} seconds'.format(total_travel_time))
    average_travel_time = df['Trip Duration'].mean()
    print('Average travel time = {} seconds'.format(average_travel_time))

    print('\nTime taken to get this information is {} seconds'.format(time.time() - start_time))
    print('='*100)

def user_info(df, city):
    start_time = time.time()
    counts_of_each_user_type = df['User Type'].value_counts()
    print('Counts of each user type:\n ', counts_of_each_user_type)
    if city !='washington':
        counts_of_each_gender = df['Gender'].value_counts()
        print('Counts of each gender:\n', counts_of_each_gender)
        earliest_year_of_birth = df['Birth Year'].min()
        print('Earliest year of birth is:', earliest_year_of_birth)
        most_recent_year_of_birth = df['Birth Year'].max()
        print('Most recent year of birth is:', most_recent_year_of_birth)
        most_common_year_of_birth = df['Birth Year'].mode()[0]
        print('Most common year of birth is:', most_common_year_of_birth)

    print('\nTime taken to get this information is {} seconds'.format(time.time() - start_time))
    print('='*100)

def data(df):
    raw_data = 0
    while True:
        five_lines = input('Would you like to view raw data before showing your statistics (yes/no)?\n')
        if five_lines not in ['yes', 'no']:
            five_lines = input('Error, please enter a correct input')
        elif five_lines == 'yes':
            raw_data += 5
            print(df.iloc[raw_data : raw_data + 5])
        five_lines_continue = input('Would you like to view more (yes/no)?\n')
        if five_lines_continue == 'no':
            break
        elif five_lines == 'no':
            return
    print('='*100)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        data(df)
        popular_time_of_travel(df)
        popular_stations_and_trips(df)
        trip_duration(df)
        user_info(df, city)
        restart = input('\n\nwould you like to make another search (yes,no)?\n')
        if restart !='yes':
            break

if __name__=="__main__":
    main()
