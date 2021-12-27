"""
This program uses the Black-Scholes formula to estimate
returns of an option at a range of dates and potential underlying prices.
The estimations are based on constant implied volatility.

@author: Rafid Khan
"""

import numpy as np
from scipy.stats import norm
from yahoo_fin.stock_info import *
from datetime import date, timedelta


def getDTE(expiry):
    """
    this method calculates the remaining days given an expiration date
    :param expiry: expiration date
    :return: (int) number of days between today and expiration date
    """
    today = date.today()
    dte = expiry - today
    return dte.days


def pricer(underlying, strike, dte, strategy=""):
    """
    this method uses the Black-Scholes method to derive the theoretical
    price of an option assuming constant volatility, and interest rates
    :param underlying: the current price of the underlying security
    :param strike: the strike price of the contract
    :param dte: no. of days remaining until expiration
    :param strategy: which direction the strategy is going long "C" for long call,
    "P" for long put
    :return: (float) price of the option
    """
    d1 = (np.log(underlying / strike) + (0.01 + 0.30 ** 2 / 2) * dte) \
         / (0.30 * np.sqrt(dte))

    d2 = d1 - 0.30 * np.sqrt(dte)

    if strategy == "C":
        price = underlying * norm.cdf(d1, 0, 1) - strike * \
                np.exp(-0.01 * dte) * norm.cdf(d2, 0, 1)
    elif strategy == "P":
        price = strike * np.exp(-0.01 * dte) * \
                norm.cdf(-d2, 0, 1) - underlying * norm.cdf(-d1, 0, 1)
    else:
        print("Please confirm all option parameters above")

    return price


def get_underlying():
    """
    uses the yahoo finance module to derive the price of a stock / etf
    (data is delayed by 15 minutes)
    :return: (float) price of the stock or etf
    """
    while True:
        try:
            temp = input("Enter the ticker symbol of the underlying stock or ETF: ")
            underlying = (round(get_live_price(temp), 2))
            break
        except AssertionError:
            print("Symbol not found ")

    return underlying


def get_strike():
    """
    prompts the user to enter the strike price of their contract
    :return: (float) strike price
    """
    while True:
        try:
            strike = float(input("Enter the strike price of the option: "))
            break
        except ValueError:
            print("Please enter a number: ")

    return strike


def get_expiry():
    """
    prompts the user to enter the expiration date of their contract
    :return: (date) date of expiry formatted according to datetime (yyyy-mm-dd)
    """
    while True:
        try:
            temp = input("Enter the date of expiry: (e.g. YYYY/MM/DD) ")
            split = temp.split("/")
            split = list(map(int, split))
            expiry = (date(split[0], split[1], split[2]))
            today = date.today()
            if expiry < today:
                raise Exception
            break
        except:
            print("Enter a valid date! ")

    return expiry


def get_strategy():
    """
    prompts the user to indicate if their contract is a long call or long put
    :return: (char) 'C' if call or 'P' if put
    """
    while True:
        try:
            strategy = input("Enter which strategy you are going long ( (C)all or (P)ut ?) ")
            if len(strategy) != 1:
                raise Exception
            elif strategy == "C":
                break
            elif strategy == "P":
                break
            else:
                raise Exception
        except Exception:
            print("Enter a valid strategy 'C' if call 'P' if put")

    return strategy


def get_range():
    """
    prompts the user for the price range of the underlying they'd like to see
    in order to derive the theoretical option price for each price in that range
    :return: (array) (size: 2)  [lowest_price , highest_price]
    """
    while True:
        try:
            temp = input("Enter the range of potential underlying prices: (e.g 100-200) ")
            split = temp.split("-")
            split = list(map(int, split))
            if split[1] < split[0]:
                raise Exception
            elif split[0] < 0:
                raise Exception
            break
        except Exception:
            print("Invalid range! ")
    return split


def create_underlying_ranges(underlying_range):
    """
    given an array of two prices which is assumed to be the range, it will
    calculate an appropriate increment between the two prices to display
    to the user.

    For instance, a price range of 100 will have an increment of 5.
    (e.g underlying_range = [100,200]:
        ranges = [100, 105, 110, 115, 120, 125, 130,
                135, 140, 145, ... , 200]

    It will then create a new array with the price range + prices in
    between according to the calculated increment value.
    :param underlying_range: range of underlying prices obtained from user
    :return: array containing the complete range of prices
    """
    ranges = []
    difference = underlying_range[1] - underlying_range[0]

    if 0 < difference <= 10:
        increment = 1
    elif 10 < difference <= 100:
        increment = 5
    elif 100 < difference <= 1000:
        increment = 10
    elif 1000 < difference:
        increment = 100
    else:
        increment = 100

    for i in range(underlying_range[0], underlying_range[1], increment):
        ranges.append(i)

    ranges.append(underlying_range[1])
    return ranges


def create_days_range(expiration):
    """
    given the number of days until expiration, this function will
    create an array of all the days to represent the range of dates
    :param expiration: number of days until expiration
    :return: days_range: array containing dates from today, until expiration
            (e.g today = 2021/12/01, expiration = 3:
                days_range = [2021/12/01, 2021/12/02, 2021/12/03])
    """
    days_range = []
    today = date.today()
    for i in range(expiration + 1):
        temp = today + timedelta(days=i)
        var = date.strftime(temp, "%Y/%m/%d")
        days_range.append(var)

    return days_range


def calculate_dte(days_range):
    """
    given a range of dates, this function will create an array containing
    their dte values, which is required for the Black-Scholes formula. Since
    you must enter the value of time in the equation as (# of days remaining) / 365
    :param days_range: array containing dates from today, until expiration
    :return: dte: array containing the dte value for each date in date range
    """
    length = len(days_range)
    dte = []
    temp = []

    for i in range(0, length):
        temp.append(i)

    temp.reverse()

    for j in range(0, length):
        dte.append(temp[j] / 365)

    dte[len(dte) - 1] = 0.00000001

    return dte


def create_matrix(price_ranges, days_ranges, strike, calculated_dte, strategy):
    """
    given the necessary information, this function will create a 2D array, which
    contains price of an option according to its date found in the range of dates,
    and a hypothetical price found in the price range.
    :param price_ranges: array containing range of hypothetical prices
    :param days_ranges: array containing range of dates until expiration
    :param strike: strike price
    :param calculated_dte: array containing time values for each date in days_range
    :param strategy: strategy of the contract
    :return: matrix: 2D array containing the solution
    """
    rows = len(price_ranges)
    col = len(days_ranges)
    matrix = []
    for i in range(0, rows):
        row = []
        for j in range(0, col):
            row.append(round(pricer(price_ranges[i], strike, calculated_dte[j], strategy), 2))
        matrix.append(row)
    return matrix


def matrix_to_string(matrix, price_ranges, date_ranges, strike, underlying, strategy, expiry, dte):
    """
    string representation of the 2D array from create_matrix(...)
    :param matrix: 2D array containing the solution
    :param price_ranges: range of prices
    :param date_ranges: range of dates
    :param strike: strike price
    :param underlying: underlying stock / etf
    :param strategy: strategy of the contract
    :param expiry: expiration date
    :param dte: days until expiration
    :return:
    """
    result = ""
    rows = len(price_ranges)
    col = len(date_ranges)

    result += "Underlying current price:  " + str(underlying) + "     "
    result += "Contract: " + str(expiry) + str(strike) + strategy
    result += "Current value: " + str(pricer(underlying, strike, dte, strategy))
    result += "\n"

    for i in range(0, col):
        result += "       "
        result += date_ranges[i]

    for i in range(0, rows):
        result += "\n"
        result += "$" + str(price_ranges[i]) + "       "
        for j in range(0, col):
            if len(str(matrix[i][j])) == 5:
                result += str(matrix[i][j]) + "            "
            elif len(str(matrix[i][j])) == 6:
                result += str(matrix[i][j]) + "           "
            elif len(str(matrix[i][j])) == 3:
                result += str(matrix[i][j]) + "              "
            else:
                result += str(matrix[i][j]) + "             "

    return result


def main():
    underlying = get_underlying()
    strike = get_strike()
    expiry = get_expiry()
    ranges = get_range()
    strategy = get_strategy()

    days = getDTE(expiry)

    underlying_ranges = create_underlying_ranges(ranges)
    date_ranges = create_days_range(days)

    calculated_dte = calculate_dte(date_ranges)

    matrix = create_matrix(underlying_ranges, date_ranges, strike, calculated_dte, strategy)
    print(matrix_to_string(matrix, underlying_ranges, date_ranges, strike, underlying, strategy, expiry, days / 365))


main()
