from matplotlib import pyplot as plt
from datetime import datetime as dt, date, timedelta
from matplotlib import dates
from matplotlib import style
from mpl_finance import candlestick_ohlc

def create_table(file_name):
    f = open(file_name, "r")
    main_lst = []
    company_lst = []
    f.readline()
    for line in f:
        row = line.strip().split(",")
        if len(company_lst) > 0 and row[6] != company_lst[0][3]:
            main_lst.append(company_lst)
            company_lst = []
        company_lst.append([dt.strptime(row[0],'%m/%d/%y'), float(row[4]), int(row[5]), row[6], float(row[1]), float(row[2]), float(row[3])])
    main_lst.append(company_lst)
    f.close()
    return main_lst

def date_lst(big_data):
    dates_lst = []
    for row in big_data[0]:
        dates_lst.append(row[0])
    return dates_lst

def features_lst(big_data,index):
    main_features = []
    for company in big_data:
        company_features = []
        for day in company:
            company_features.append(day[index])
        main_features.append(company_features)
    return main_features

def plot_comparative_graphs(dates, close):
    style.use("dark_background")
    ax1 = plt.subplot2grid((6, 1), (0, 0), rowspan=5, colspan=1)
    ax1.plot(dates, close[0], label="Amazon")
    ax1.plot(dates, close[1], label="Apple")
    ax1.plot(dates, close[2], label="Microsoft")
    ax1.plot(dates, close[3], label="Google")
    ax1.plot(dates, close[4], label="Facebook")
    ax1.legend()
    plt.xlabel("Date")
    plt.ylabel("Closing Price")
    plt.title("Closing Price Comparison in the Tech Industry")
    ax1.grid('True', alpha=0.2)
    plt.show()

def open_high_low_close(company_data):
    company_name = input("Please enter the name of the company: ")
    style.use('dark_background')
    dates_lst = company_data[0]
    open_price = company_data[1]
    high_price = company_data[2]
    low_price = company_data[3]
    close = company_data[4]
    volume = company_data[5]
    new_dates = []
    for date in dates_lst:
        num_date = dates.datestr2num(str(date))
        new_dates.append(num_date)
    ohlc_lst = []
    for i in range(len(new_dates)):
        data_points = new_dates[i], float(open_price[i]), float(high_price[i]), float(low_price[i]), float(close[i])
        ohlc_lst.append(data_points)
    ax1 = plt.subplot2grid((6, 1), (0, 0), rowspan=5, colspan=1)
    for date in ax1.xaxis.get_ticklabels():
        date.set_rotation(45)
    lowest_volume = 0
    ax1volume = ax1.twinx()
    ax1volume.fill_between(new_dates, lowest_volume, volume, facecolor='#1f77b4', alpha=0.4)
    candlestick_ohlc(ax1, ohlc_lst, width=2, colorup='g', colordown='r', alpha=0.8)
    dayFormatter = (dates.DateFormatter("%m/%d/%y"))
    ax1.xaxis.set_major_formatter(dayFormatter)
    ax1.grid('True', alpha=0.2)
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Price")
    ax1volume.get_yaxis().get_major_formatter().set_useOffset(False)
    ax1volume.set_ylabel("Volume(in Millions)")
    plt.title("Stock Prices and Trade Volume\nOver Time For " + company_name)
    plt.show()


def moving_avg(close_prices,window_size):
    avg_lst = [0] * window_size
    for i in range(window_size,len(close_prices)):
        total = close_prices[i - window_size:i]
        avg_lst.append(sum(total)/len(total))
    return avg_lst

def predictive_model(close_prices, window, predict_len):
    length = len(close_prices)
    prediction_range = close_prices[length - window:]
    prediction = sum(prediction_range)/window
    prediction_lst = [prediction] * predict_len
    return prediction_lst

def plot_predictive_model(company_data):
    added_dates_lst = []
    d = date(2018, 2, 8)
    d2 = date(2018, 5, 9)
    new_dates_lst = []
    added_days = d2 - d
    for i in range(int((added_days.days) + 1)):
        new_dates_lst.append(d + timedelta(i))
    added_dates_lst.extend(new_dates_lst)
    style.use("dark_background")
    company_name = input("Please enter the name of the company: ")
    close = company_data[4]
    dates_lst = company_data[0]
    dates_lst.extend(added_dates_lst)
    length = len(dates_lst)
    prediction_lst = predictive_model(close, 5, 90)
    ax1 = plt.subplot2grid((6, 1), (0, 0), rowspan=5, colspan=1)
    moving_avg_line1 = moving_avg(close, 50)
    ax1.plot(dates_lst[:len(close)], close, label="Daily Stock Prices", alpha=0.4)
    ax1.plot(dates_lst[50:len(close)], moving_avg_line1[50:len(close)+1], label="Moving Average Line", alpha=0.5, linestyle="dashed")
    ax1.plot(dates_lst[length-len(prediction_lst):], prediction_lst, label="Prediction for Next 3 Months", color="green", linewidth=3.0)
    ax1.legend()
    ax1.grid('True', alpha=0.2)
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.title("Price vs Time for " + company_name)
    plt.show()

def plot_moving_averages(company_data):
    company_name = input("Please enter the name of the company: ")
    style.use("dark_background")
    close = company_data[4]
    dates_lst = company_data[0]
    ax1 = plt.subplot2grid((6, 1), (0, 0), rowspan=5, colspan=1)
    moving_avg_line1 = moving_avg(close, 50)
    ax1.plot(dates_lst,close, label= "Daily Stock Prices", alpha=0.4)
    ax1.plot(dates_lst[50:],moving_avg_line1[50:], label="Moving Average Line", alpha=0.7)
    ax1.legend()
    ax1.grid('True', alpha=0.2)
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.title("Price vs Time for " + company_name)
    plt.show()

def find_error(close_price, moving_avg, window_size):
    error = 0
    for i in range(window_size, len(close_price)):
        error += ((close_price[i] - moving_avg[i]) ** 2)
    return error / (len(close_price) - window_size)

def find_weighted_avg(close_price, window_size):
    wa_lst = [0] * window_size
    for i in range(window_size, len(close_price)):
        wa = 0
        for j in range(i - window_size, i):
            if 0 < j < 20:
                wa += close_price[j] * 0.0075
            elif 20 <= j < 30:
                wa += close_price[j] * 0.02
            else:
                wa += close_price[j] * 0.0125
        wa_lst.append(wa)
    return wa_lst

def main():

    #data
    big_data = create_table("tech_stocks.csv")
    volume_lst = features_lst(big_data, 2)
    open_lst = features_lst(big_data, 4)
    high_lst = features_lst(big_data, 5)
    low_lst = features_lst(big_data, 6)
    close_lst = features_lst(big_data, 1)
    dates = date_lst(big_data)
    Amazon_data = [dates, open_lst[0], high_lst[0], low_lst[0], close_lst[0],volume_lst[0]]
    Apple_data = [dates, open_lst[1], high_lst[1], low_lst[1], close_lst[1], volume_lst[1]]
    Microsoft_data = [dates, open_lst[2], high_lst[2], low_lst[2], close_lst[2], volume_lst[2]]
    Google_data = [dates, open_lst[3], high_lst[3], low_lst[3], close_lst[3], volume_lst[3]]
    Facebook_data = [dates, open_lst[4], high_lst[4], low_lst[4], close_lst[4], volume_lst[4]]

    #1st graph #comparative graph
    print(plot_comparative_graphs(dates,close_lst))

    #2nd set of graphs #moving averages
    print(plot_moving_averages(Amazon_data))
    print(plot_moving_averages(Apple_data))
    print(plot_moving_averages(Microsoft_data))
    print(plot_moving_averages(Google_data))
    print(plot_moving_averages(Facebook_data))

    #moving average lists of each company
    Amazon50 = moving_avg(close_lst[0], 50)
    Apple50 = moving_avg(close_lst[1], 50)
    Microsoft50 = moving_avg(close_lst[2], 50)
    Google50 = moving_avg(close_lst[3], 50)
    Facebook50 = moving_avg(close_lst[4], 50)

    #degree of error squared for each company between the prices and moving averages
    Amazon_error = find_error(close_lst[0], Amazon50, 50)
    Apple_error = find_error(close_lst[1], Apple50, 50)
    Microsoft_error = find_error(close_lst[2], Microsoft50, 50)
    Google_error = find_error(close_lst[3], Google50, 50)
    Facebook_error = find_error(close_lst[4], Facebook50, 50)

    print(
        "The most accurate moving averages window between 50, 100, and 150 was 50. \nThe larger the window, the greater the error will be. However, too small of \na window will not be meaningful and will resemble the daily stock price too \nmuch to give us any reasonable predictions. The total squared error for Amazon was \n",
        Amazon_error, ".\nThe squared error for Apple was ", Apple_error, ".\nThe squared error for Microsoft was ",
        Microsoft_error, ".\nThe squared error for Google was ", Google_error, "\nThe squared error for Facebook was ",
        Facebook_error, ".", sep="")

    #3rd set of graphs #candlestick model
    print(open_high_low_close(Amazon_data))
    print(open_high_low_close(Apple_data))
    print(open_high_low_close(Microsoft_data))
    print(open_high_low_close(Google_data))
    print(open_high_low_close(Facebook_data))

    #4th set of graphs #prediction
    print(plot_predictive_model(Amazon_data))
    print(plot_predictive_model(Apple_data))
    print(plot_predictive_model(Microsoft_data))
    print(plot_predictive_model(Google_data))
    print(plot_predictive_model(Facebook_data))


main()


