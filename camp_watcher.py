import requests
from bs4 import BeautifulSoup
import copy
import datetime
import logging
from collections import defaultdict
import urllib
import IPython

BASE_URL = "https://www.recreation.gov/campsiteCalendar.do"
BASE_PARAMS = {
    "page": "matrix",
    "contractCode": "NRSO",
}

#"calarvdate=08/17/2018&&parkId=70757"

PARK_DATE_FORMAT = "%m/%d/%Y"

FORMAT = '%(asctime)-15s: %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger("watcher")


def camp_watcher(park_id, dates):
    dates.sort()
    cur_date = dates[0]
    max_date = dates[-1]
    dates_available = defaultdict(list)
    while cur_date <= max_date:
        assert isinstance(cur_date, datetime.date)
        cur_params = copy.deepcopy(BASE_PARAMS)
        cur_params["parkId"] = park_id
        cur_params["calarvdate"] = cur_date.strftime(PARK_DATE_FORMAT)
        result = requests.get(BASE_URL, params=cur_params)
        if result.status_code != 200:
            logger.error("invalid result for: %s --> %s" % (cur_params, (result.status_code, result.text)))
            raise Exception("unexpected error")
        soup = BeautifulSoup(result.text, 'html.parser')
        calendar = soup.find(id="calendar")
        avail = calendar.select('a[class="avail"]')
        for result in avail:
            href = result.attrs["href"]
            parsed_url = urllib.parse.urlparse(href)
            query_parsed = urllib.parse.parse_qs(parsed_url.query)
            arvdate = query_parsed["arvdate"][0]
            free_date = datetime.datetime.strptime(arvdate, PARK_DATE_FORMAT).date()
            site_id = query_parsed["siteId"][0]
            if free_date in dates:
                dates_available[free_date].append(site_id)
        cur_date = cur_date + datetime.timedelta(days=14)


    print(dates_available)
