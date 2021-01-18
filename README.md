# Smythsaco
Request - Hybrid Auto checkout bot for https://www.smythstoys.com/uk/en-gb/

This bot is only intended to be used in UK region and GBP currency. This bot will auto cart and submit details until it gets to posting CC info, there you a browser will open and you can manual checkout. I made this due to restock of console's and hope this can help you secure an console. 

Required Modules
- requests
- re 
- time
- datetime
- selenium

Install modules in CMD shell using pip, run commands 'pip install <module_name>' (Remove <> and ''). If 'no module named <module_name>' error happens just skip.

Download chromedriver here https://chromedriver.storage.googleapis.com/index.html?path=87.0.4280.88/. Extract it and take the .exe out the folder and copy the path to the variable inside the .py.

Edit the .py file lines 16 to 25, these are the data needed to ATC, do not include any spaces in the post code, make sure the email is a new email that hasn't been used on smyths before. Chrome driver path use two \\ instead of a singular \.

How to get sku of item:
https://www.smythstoys.com/uk/en-gb/video-games-and-tablets/playstation-5/playstation-5-consoles/playstation-5-console/p/191259
The end of the URL '191259' is the sku.

Simply run the .py enter the product URL and then the SKU and you should be good to go. Monitor delays are at 7 seconds, you can reduce or up this I have been running this all day without and rate limits so experiment. To change change the number on line 96 and 99.

This was only intented to help you guys get at least one console.Those who want to develop the scripts look into selenium module to add lines of code to auto fill the last stages of checkout. Thos who want multiples just duplicated the script and run different information, or you can look into threading or multiprocessing to develop it.

This is my first Github post so bear with me if it's bad. Good luck on the Console restock.

Follow my twitter - https://twitter.com/damon3312 (;
