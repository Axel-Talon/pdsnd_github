import pandas as pd
import datetime as dt


def load_data(city):
    """User inputs city they would like to create the DataFrame for and function output creates Dataframe"""
    city_csv = pd.read_csv(("{}.csv").format(city))
    df = pd.DataFrame(city_csv)
    return df

def raw_data_print(dataset,first_obs,last_obs):
    """Ask if would like to see raw data. Can only accept inputs of y or n"""
    while True:
        try:
            z = input('Would you like to view raw data? [y/n]: ')
            z_items = ['y','n']
            z_items.index(z)
            break
        except:
            print("Please input a 'y' or an 'n'")
    """Based on response to previous question initiate view of data. Loop round until person inputs no to below question"""
    while z == 'y':
        print(dataset[first_obs:last_obs])
        first_obs += 5
        last_obs += 5
        z = input('Would you like to see the next 5 rows of data? [y/n]: ')

def filters():
    """User inputs month they would like to filter on. Error message will occur if not valid response"""
    while True:
        try:
            month = input("This dataset includes data from January to June.\nPlease choose the month you would like to filter for.\nAlternatively, type 'none' if you do not want to apply a month filter: ")
            month_items = ["January","February","March","April","May","June","none"]
            month_items.index(month)
            break
        except:
            print("That is not a valid input.\nPlease input a month from January to June (Eg March) or put 'none'")

    print()
    """User inputs day they would like to filter on. Error message will occur if not valid response"""
    while True:
        try:
            day = input("Please choose the Day of the Week you would like to filter for.\nAlternatively, type 'none' if you do not want to apply a day filter: ")
            day_items = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday","none"]
            day_items.index(day)
            break
        except:
            print("That is not a valid input.\nPlease input a day (Eg Tuesday) or put 'none'")
            print()
    """User defined month and day specified as outputs"""
    return month, day


def filter_data(input_data,city,month,day):
    """Amends current fields and creates additional fields to aid in filtering"""
    input_data['Start Time'] = pd.to_datetime(input_data['Start Time'])
    input_data['End Time'] = pd.to_datetime(input_data['End Time'])
    input_data['Start Month'] = input_data['Start Time'].dt.month_name(locale = 'English')
    input_data['Start Day'] = input_data['Start Time'].dt.day_name(locale = 'English')
    input_data['Start Hour'] = input_data['Start Time'].dt.hour
    input_data['Trip'] = input_data['Start Station']+'_'+input_data['End Station']

    """Filter based on User specified month and day inputs"""
    if month == 'none' and day == 'none':
        city_filter = input_data.copy()
    elif month == 'none':
        city_filter = input_data[input_data['Start Day'] == day]
    elif day == 'none':
        city_filter = input_data[input_data['Start Month'] == month]
    else:
        city_filter = input_data.loc[(input_data['Start Month'] == month)&(input_data['Start Day'] == day)]

    """Print relevent information based on month and day filters"""
    if month == 'none' and day == 'none':
        print('The month in which most trips started was {}!'.format(city_filter['Start Month'].mode().iloc[0]))
        print('The day on which most trips started was {}!'.format(city_filter['Start Day'].mode().iloc[0]))
    elif month == 'none':
        print('The month on which most trips started was {}!'.format(city_filter['Start Month'].mode().iloc[0]))
    elif day == 'none':
        print('The day in which most trips started was {}!'.format(city_filter['Start Day'].mode().iloc[0]))

    """Print additional metrics"""
    print('The most common start hour was {}:00h'.format(city_filter['Start Hour'].mode().iloc[0]))
    print('The most common starting station was {}'.format(city_filter['Start Station'].mode().iloc[0]))
    print('The most common ending station was {}'.format(city_filter['End Station'].mode().iloc[0]))

    modal_trip = city_filter['Trip'].mode().iloc[0]
    sep_index = modal_trip.find('_')
    print()
    print('The most common trip is from {} Station to {} Station'.format(modal_trip[:sep_index],modal_trip[sep_index+1:]))

    trip_seconds = (city_filter['End Time']-city_filter['Start Time']).dt.total_seconds()
    trip_days = trip_seconds.sum()//86400
    trip_remainder_hours = (trip_seconds.sum()%86400)//3600
    trip_remainder_minutes = round((trip_seconds.sum()-((trip_days*86400)+(trip_remainder_hours*3600)))/60)
    print()
    print('Total time travelled amounts to {} days, {} hours, and {} minutes'.format(trip_days,trip_remainder_hours,trip_remainder_minutes))

    av_trip_minutes = round(trip_seconds.mean())//60
    av_trip_seconds = round(trip_seconds.mean())%60
    print()
    print('Average time travelled amounts to {} minutes and {} seconds'.format(av_trip_minutes,av_trip_seconds))
    print()
    print('User type count is:')
    print(city_filter['User Type'].value_counts())
    print()

    """Create city dependency for Gender/Birth Year info as Washington Dataset does not include these fields"""
    if city == 'Chicago' or city == 'New_York_City':
        print('The Gender count is:')
        print(city_filter['Gender'].value_counts())
        print()
        print('The earliest Birth Year is: {}\nThe most recent Birth Year is: {}\nThe most common Birth Year is: {}'.format(int(city_filter['Birth Year'].min()),int(city_filter['Birth Year'].max()),int(city_filter['Birth Year'].mode().iloc[0])))
    else:
        print('Unfortunately Washington does not have any Gender or Birth Year information')


"""Ask for city input and runs defined functions in loop"""
restart = 'y'
while restart == 'y':
    while True:
        try:
            city = input("Please enter city for which you would like to explore data.\nNew York City, Chicago, or Washington: ")
            city_items = ["New York City","Washington","Chicago"]
            city_items.index(city)
            if city == "New York City":
                city = "New_York_City"
            break
        except:
            print("That is not a valid city. Please try again")
            print()

    print()
    df = load_data(city)
    raw_data_print(df,0,5)
    print()
    month, day = filters()
    print()
    filter_data(df,city,month,day)

    print()

    restart = input("Would you like to explore again?\nPress 'y' for Yes or any other key for No: ")
