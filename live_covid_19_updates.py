import requests
import time
import datetime

from bs4 import BeautifulSoup
from plyer import notification


class LiveCoronaVirusUpdate:
    """ Gives live corona virus updates in a day for India """

    @staticmethod
    def get_latest_count_of_active_cases() -> str:
        """ Get the latest count of active corona positive cases in a day """
        url = LiveCoronaVirusUpdate.get_url()
        html_structure = LiveCoronaVirusUpdate.get_html(url)

        total_cases_india = html_structure.find('div', attrs={'class': 'maincounter-number'})
        total_cases_india = total_cases_india.find('span')
        total_cases_india = total_cases_india.string

        news_update = html_structure.find('div', attrs={'id': 'news_block'})

        date = datetime.datetime.now().strftime("%Y-%m-%d")
        news_date = 'newsdate' + date

        news_today = news_update.find('div', attrs={'id': news_date})
        new_cases_india = news_today.find('strong')
        new_cases_india = new_cases_india.string.split(' ')[0]

        return total_cases_india, new_cases_india

    @staticmethod
    def get_url() -> str:
        """ Get data from the Ministry of Health and Wellness of India """
        url = "https://www.worldometers.info/coronavirus/country/india/"
        return url

    @staticmethod
    def get_html(url: str) -> object:
        """ Downloads the homepage structure """

        # Attaching headers for the browser compatibility
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
        }

        html = requests.get(url, headers=headers)
        soup = BeautifulSoup(html.content, "html.parser")
        return soup

    @staticmethod
    def get_status():
        """ Updates the status active corona positive in a day detected in India """
        total_cases, latest_active_cases = LiveCoronaVirusUpdate.get_latest_count_of_active_cases()
        return total_cases, latest_active_cases

    @staticmethod
    def get_message(total: str, active_cases: str) -> str:
        """ Message toast in system notification """
        return f'Total Cases in India: {total}\n' \
               f'New Active Cases in India: {active_cases}'

    @staticmethod
    def get_datetime():
        """ Gets current date, month, year """
        current = datetime.datetime.now()
        current_month = current.strftime("%b")
        current_date = current.day
        current_year = current.year
        return current_date, current_month, current_year

    @staticmethod
    def print_status():
        """ Prints status of the script in the terminal """
        date, month, year = LiveCoronaVirusUpdate.get_datetime()
        timestamp = datetime.datetime.now()
        print(f'[Last Update]: {date} {month} {year}: {timestamp.hour}:{timestamp.minute}')
        print(f'Updating.....')

    @staticmethod
    def system_notification(title: str) -> object:
        """
        To display notification in the system

        :param title: title of system notification
        """
        while True:
            total, active_cases = LiveCoronaVirusUpdate.get_status()

            message = LiveCoronaVirusUpdate.get_message(total=total, active_cases=active_cases)
            notification.notify(title=title, message=message, timeout=40)

            LiveCoronaVirusUpdate.print_status()
            # Active cases updates in 30 minutes
            time.sleep(1800)


current_date, current_month, current_year = LiveCoronaVirusUpdate.get_datetime()

title = "LIVE: COVID-19 India Outbreak - {} {} {}".format(current_date, current_month, current_year)

# Start giving updates
notifications = LiveCoronaVirusUpdate.system_notification(title=title)
