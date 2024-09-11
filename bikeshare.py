import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def check_data_entry(prompt, valid_entries): 
    """
    Function that asks the user to input data and verifies if it's valid.
    This simplifies the get_filters() function, where we need to ask the user for three inputs.
    Args:
        (str) prompt - message to show to the user
        (list) valid_entries - list of accepted strings 
    Returns:
        (str) user_input - user's valid input
    """
    try:
        user_input = str(input(prompt)).lower()
        while user_input not in valid_entries : 
            print('It looks like your entry is incorrect.')
            print('Let\'s try again!')
            user_input = str(input(prompt)).lower()

        print('Great! You\'ve chosen: {}\n'.format(user_input))
        return user_input

    except:
        print('There seems to be an issue with your input.')

def get_filters(): 
    """
    Function to ask the user for a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    valid_cities = CITY_DATA.keys()
    prompt_cities = 'Choose one of the 3 cities (chicago, new york city, washington): '
    city = check_data_entry(prompt_cities, valid_cities)

    valid_months = ['all','january','february','march','april','may','june']
    prompt_month = 'Choose a month (all, january, february, ... , june): '
    month = check_data_entry(prompt_month, valid_months)

    valid_days = ['all','monday','tuesday','wednesday','thursday','friday','saturday', 'sunday']
    prompt_day = 'Choose a day (all, monday, tuesday, ... sunday): '
    day = check_data_entry(prompt_day, valid_days)

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def common_time(df, column):
    """Common for displays statistics on the most frequent times of travel."""
    common_data = df[column].value_counts()
    most_common_data = common_data.idxmax()
    print("The most common {}: {}".format(column.replace("_", " "), most_common_data))
    
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_time(df, 'month')
    # TO DO: display the most common day of week
    common_time(df, 'day_of_week')
    # TO DO: display the most common start hour
    common_time(df, 'hour')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print("The most commonly used start station: {}".format(df['Start Station'].value_counts().idxmax()))

    # TO DO: display most commonly used end station
    print("The most commonly used end station: {}".format(df['End Station'].value_counts().idxmax()))

    # TO DO: display most frequent combination of start station and end station trip
    # Group data by 2 columns Start Station and End Station
    combine_data = df.groupby(['Start Station', 'End Station'])
    # Count the number of occurrences of each group
    count_combine_data = combine_data.size()
    # Print most frequent combination of start and end station
    print("The most frequent combination of start station and end station trip: {}".format(count_combine_data.idxmax()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    # Trip duration is stored as second, so convert to hour
    print("Total travel time is: {} hours".format(df['Trip Duration'].sum() / 3600))

    # TO DO: display mean travel time
    print("The mean travel time is: {} hours".format(df['Trip Duration'].mean() / 3600))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Value count of each user type:\n', user_types)

    # Check 2 columns 'Gender' and 'Birth Year' exist in DataFrame or not
    gender_column = 'Gender'
    birth_year_column = 'Birth Year'
    if gender_column not in df.columns and birth_year_column not in df.columns:
        # If not exist, create 2 columns and setting default value for it
        df[gender_column] = 'Unknown'
        df[birth_year_column] = 0
    
    # TO DO: Display counts of gender
    # Create a copy of 'Gender' column
    gender_copy = df[gender_column].copy()
    # Change the NaN value in the copy without effecting to original DataFrame
    gender_copy.fillna('Unknown', inplace=True)

    gender_count = gender_copy.value_counts()
    print('Value counts of gender:\n', gender_count)

    # TO DO: Display earliest, most recent, and most common year of birth
    # Create a copy of the 'Birth Year' column
    birth_year_copy = df[birth_year_column].copy()
    # Change the NaN value in the copy without effecting to original DataFrame
    birth_year_copy.fillna(0, inplace=True) 

    print('The earliest year of birth: ', int(birth_year_copy.min()))
    print('The most recent year of birth: ', int(birth_year_copy.max()))
    print('The most common year of birth: ', int(birth_year_copy.value_counts().idxmax()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def get_raw_data(df):
    """
    Asks user if they want to see 5 lines of raw data.
    Display that data if the answer is 'yes'
    Stop the program when the user says 'no' or there is no more raw data to display
    """
	# Avoid the columns collapse and only a few are display when show raw data 
	pd.set_option('display.max_columns', 200)

    x = 0
    while(input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n').lower() != 'no'):
        x = x + 5
        if x > len(df):
            print("There is no more raw data to display")
            break
        print(df.head(x))

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        get_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
