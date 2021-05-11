import time
from pandas import read_csv, to_datetime
from numpy import array, where

# available cities and corresponding files' paths
CITY_DATA = {'chicago': 'chicago.csv', 'new york city': 'new_york_city.csv', 'washington': 'washington.csv'}
# list available techniques
available_techs = array(['month', 'day', 'both', 'none'])
# list available months
available_months = array(['january', 'february', 'march', 'april', 'may', 'june'])
# list available days
available_days = array(['saturday', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday'])


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    # set default month and day to all
    month = "all"
    day = "all"

    # get the city from user
    print('Hello! Let\'s explore some US bike share data!')
    while True:
        city = input('Which city you want to explore bike share data for ? Chicago, New York, or Washington ?\n')
        city = city.lower()
        if city not in CITY_DATA.keys():
            print("Oops, that's not a valid input, Please watch out for typos!")
        else:
            break

    # offer techniques for filtering
    filter_tech = input('Would you like to filter the data by month, day, both or not at all ? Type "none" for '
                        'no time filter\n')

    while True:
        if filter_tech not in available_techs:
            filter_tech = input("Invalid input! Please enter :\n'month' to filter by month\n'day' to filter by day\n'both'"
                                " to filter by both month and day\n'none' if you don't need any filter\n")
        else:
            break

    # get user input for month (january, february, ... , june)
    if filter_tech == 'month' or filter_tech == 'both':
        month = input("Which month? January, February, March, April, May, or June ?\n").lower()
        while True:
            if month not in available_months:
                month = input("Pleas type the month full name between January and June and watch out for typos!\n")
            else:
                break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    if filter_tech == 'day' or filter_tech == 'both':
        day = input("Which day? Saturday, Sunday, Monday, Tuesday, Wednesday, Thursday, or Friday ?\n").lower()
        while True:
            if day not in available_days:
                day = input("Pleas type the day full name between Saturday and Friday and watch out for typos!\n")
            else:
                break

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month, day, both or none specified by filter_tech.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = to_datetime(df['Start Time'])

    # extract month, day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month_int = where(available_months == month)[0][0] + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month_int]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    frequent_month = df['month'].mode()[0]
    print("The most frequent month is : {}".format(frequent_month))

    # display the most common day of week
    frequent_day = df['day_of_week'].mode()[0]
    print("The most frequent day is : {}".format(frequent_day))

    # display the most common start hour
    frequent_hour = df['hour'].mode()[0]
    print("The most frequent hour is : {}".format(frequent_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    frequent_start_stat = df['Start Station'].mode()[0]
    print("The most commonly used start station is : {}".format(frequent_start_stat))

    # display most commonly used end station
    frequent_end_station = df['End Station'].mode()[0]
    print("The most commonly used end station is : {}".format(frequent_end_station))

    # display most frequent combination of start station and end station trip
    combined_stations = df['Start Station'].str.strip() + "!" + df['End Station'].str.strip()
    print("\nThe most frequent combination of start station and end station trip is :\nStart Station : {}\nEnd "
          "Station : {} ".format(combined_stations.mode()[0].split("!")[0], combined_stations.mode()[0].split("!")[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    print("The total travel time is : {}".format(total_time))

    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    print("The mean travel time is : {}".format(mean_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bike share users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_count = df['User Type'].value_counts()
    print("The user type and the corresponding count is : \n{}".format(user_type_count))

    # gender and birth year statistics with an exception for Washington
    try:
        # Display counts of gender
        gender_count = df['Gender'].value_counts()
        print("The gender and the corresponding count is : \n{}".format(gender_count))

        # Display earliest, most recent, and most common year of birth
        earliest_date = df['Birth Year'].min()
        recent_date = df['Birth Year'].max()
        frequent_date = df['Birth Year'].mode()[0]
        print("The earliest year of birth is : {}".format(earliest_date))
        print("The most recent year of birth is : {}".format(recent_date))
        print("The most common year of birth is : {}".format(frequent_date))

    except KeyError:
        print("Gender and birth year are not available for Washington")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def raw_data(city):
    df = read_csv(CITY_DATA[city])
    start = 0
    end = 5
    while True:
        view_data = input("Would you like to view raw data ? Type 'yes' or 'no'\n").lower()
        if view_data == 'yes':
            print(df[start:end])
            start = end
            end += 5
        elif view_data == 'no':
            break
        else:
            print("Oops ! Invalid Input watch out for typos!")


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(city)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() == 'no':
            break


if __name__ == "__main__":
    main()
