import requests
import time
import datetime

from bs4 import BeautifulSoup
from plyer import notification


class LiveCoronaVirusUpdate:
    """ Gives live corona virus updates in a day for India """
    def __init__(self):
        self.__url = "https://www.mohfw.gov.in/"
        self.__current_coronavirus_positive_count = 0
        self.__updated_count = 0

        print("---------------------------------------------------")
        print("COVID-19 India Update from {}".format(self.__url))
        print("---------------------------------------------------")

    def set_current_coronavirus_positive_count(self, current_coronavirus_positive_count: int) -> int:
        """
        Setter for the current coronaviurs positive count.

        :param current_coronavirus_positive_count: current active cases of coronavirus
        :return: current active cases of coronavirus
        """
        self.__current_coronavirus_positive_count = current_coronavirus_positive_count
        return self.__current_coronavirus_positive_count

    def update_coronavirus_positive_count(self, new_total_active_cases):
        """
        Updates coronavirus positive count.

        New total active cases will be always greater than current coronavirus positive count (fixed)

        :param new_total_active_cases: active cases in a day + total active cases = new_total_active_cases
        :return: rise in coronavirus positives count
        """

        self.__updated_count += (new_total_active_cases - self.__current_coronavirus_positive_count)
        self.__current_coronavirus_positive_count = new_total_active_cases
        return self.__updated_count

    def get_html(self):
        """ Downloads the homepage structure """

        # Attaching headers for the browser compatibility
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
        }

        html = requests.get(self.__url, headers=headers)
        soup = BeautifulSoup(html.content, "html.parser")
        return soup

    @staticmethod
    def system_notification(title: str, current_active_cases: int, extra_info: str) -> object:
        """
        To display notification in the system

        :param title: title of system notification
        :param current_active_cases: shows count of positive coronavirus patients in a day
        :param extra_info: extra message string
        """
        corona_positive_count = LiveCoronaVirusUpdate().set_current_coronavirus_positive_count(current_active_cases)
        enable_update = False

        while True:
            corona_positive_count = LiveCoronaVirusUpdate.update_coronavirus_positive_count()

            message = f'{extra_info}: {corona_positive_count}'
            notification.notify(title=title, message=message, timeout=10)

            # Active cases updates in 1 hour
            time.sleep(3600)


homepage_structure_html = LiveCoronaVirusUpdate().get_html()

site_stats_count = homepage_structure_html.find('div', attrs={'class': 'site-stats-count'})

active_cases = site_stats_count.find('li', attrs={'class': 'bg-blue'})
active_cases = active_cases.find('strong')

current = datetime.datetime.now()

current_month = current.strftime("%b")
current_date = current.day
current_year = current.year

title = "LIVE: COVID-19 India Outbreak - {} {} {}".format(current_date, current_month, current_year)

active_cases_count = active_cases.string
extra_info = "Active cases today in India"

notifications = LiveCoronaVirusUpdate.system_notification(
    title=title, current_active_cases=active_cases_count, extra_info=extra_info
)
