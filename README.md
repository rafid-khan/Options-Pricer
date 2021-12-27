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

![Screen Shot 2021-12-26 at 9 40 33 PM](https://user-images.githubusercontent.com/93891008/147428918-06f437bf-8725-43e3-94a2-c7300fecee0c.png)

Since this is the theoretical price according to the Black-Scholes model, that accounts for a constant implied volatility it is
not likely that the resulting outputs will reflect the true price of the options. 

