# Options-Pricer
A stock / ETF options pricer and returns calculator  

This program uses the Black-Scholes formula to estimate
returns of an option at a range of dates and potential underlying prices.
The estimations are based on constant implied volatility.

The program prompts the user for:
- an underlying stock / ETF 
- a strike price 
- an expiration date 
- whether they are longing a call or a put 
- a range of potential prices of the underlying stock / ETF  

The program then creates a 2D array that displays what the option price would be
within certain increments of the inputted price range, and on each date before expiration. 

An example of the output would look like:
- Enter the ticker symbol of the underlying stock or ETF: FB
- Enter the strike price of the option: 350
- Enter the date of expiry: (e.g. YYYY/MM/DD) 2021/12/31
- Enter the range of potential underlying prices (e.g 100-200): 330-360
- Enter which strategy you are going long ((C)all or (P)ut ?): C

- Underlying current price:  335.24     Contract: 2021-12-31 350.0C       Current value: 0.64

![Matrix of outputs](https://imgur.com/BqvlDHJ)

Since this is the theoretical price according to the Black-Scholes model, that accounts for a constant implied volatility it is
not likely that the resulting outputs will reflect the true price of the options. 
