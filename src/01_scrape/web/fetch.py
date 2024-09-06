import time
import requests

def fetch(url: str, pause_seconds=3.0):
    '''
    https://www.sports-reference.com/bot-traffic.html
    
    Update: May 29, 2024
    
    Sports Reference is primarily dependent on ad revenue, so we must ensure 
    that actual people using web browsers have the best possible experience when
    using this site. Unfortunately, non-human traffic, ie bots, crawlers, scrapers, 
    can overwhelm our servers with the number of requests they send us in a short 
    amount of time. Therefore we are implementing rate limiting on the site. 
    We will attempt to keep this page up to date with our current settings.

    Currently we will block users sending requests to:

    - FBref and Stathead sites more often than ten requests in a minute. * pause_seconds = 6.0 *
    - our other sites more often than twenty requests in a minute.  * pause_seconds = 3.0 *
    - This is regardless of bot type and construction and pages accessed.
    - If you violate this rule your session will be in jail for up to a day.
    
    Why Not Provide an API?

    Most of our data comes from third parties who sell the data to us. As part of 
    our agreements with them we can not provide the data available as a download on 
    our site. We are aware that an API would mitigate some issues, but it's not 
    our business model. If you want to get data for a low price, we suggest 
    NatStat.com.
    '''
    
    time.sleep(pause_seconds)
    response = requests.get(url)
    response.raise_for_status()
    return response.text

