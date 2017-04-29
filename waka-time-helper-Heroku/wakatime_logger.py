import base64
import configparser
import os
from datetime import timedelta, date, datetime

import pandas as pd
import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from slackclient import SlackClient


class SlackNotifier:
    def __init__(self, slack_token, channel_name, bot_name="Notifier Bot"):
        super().__init__()
        self.bot_name = bot_name
        self.channel_name = channel_name
        self.slack_token = slack_token
        self.slack_client = SlackClient(self.slack_token)

    def upload_file(self, filename):
        self.slack_client.api_call("files.upload", filename=filename, channels=self.channel_name,
                                   file=open(filename, 'rb'))

    def send_message(self, message):
        self.slack_client.api_call('chat.postMessage', text=message, channel=self.channel_name, username=self.bot_name,
                                   icon_emoji=":robot_face:")


config = configparser.ConfigParser()
config.read('config.ini')

FILE_NAME = config.get("Waka", "fileName")
API_KEY = config.get("Waka", "apiKey")
BASE_URL = config.get("Waka", "baseUrl")
START_DATE = datetime.strptime(config.get("Waka", "startDate"), "%Y-%m-%d").date()
SLACK_TOKEN = config.get("Slack", "token")
SLACK_CHANNEL_NAME = config.get("Slack", "channelName")

scheduler = BlockingScheduler()
slack = SlackNotifier(SLACK_TOKEN, SLACK_CHANNEL_NAME)


def prepare_request_header(api_key_in_bytes):
    b64_api_key = base64.b64encode(api_key_in_bytes).decode("utf-8")
    headers = {'content-type': 'application/json', 'Authorization': 'Basic ' + b64_api_key}
    return headers


def get_durations_from_waka(date, header):
    req_url = BASE_URL + date.strftime("%Y-%m-%d")
    response = requests.get(req_url, headers=header)
    return response.json()


def date_range(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def write_data_to_dataframe(df, start_date, end_date):
    last_df_index = len(df)
    if last_df_index > 0:
        start_date_str = df["date"].values[last_df_index - 1]
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        start_date = start_date + timedelta(days=1)
    for d in date_range(start_date, end_date):
        response_json = get_durations_from_waka(d, prepare_request_header(str.encode(API_KEY)))
        try:
            data = response_json["data"]
            data_dict = {}
            for duration_data in data:
                project_name = duration_data["project"]
                duration = duration_data["duration"]
                try:
                    data_dict[project_name] += duration
                except KeyError:
                    data_dict[project_name] = duration
            for k, v in data_dict.items():
                new_row = [d.strftime("%Y-%m-%d"), k, v]
                df.loc[last_df_index] = new_row
                last_df_index += 1
        except KeyError as keyError:
            print("[*] ERROR: for {0}, key error: {1}".format(d.strftime("%Y-%m-%d"), keyError))
            print("This means that you can't see this day's records because you've exceeded the free Waka limit")
            print("Run this script at least once in a week to get all the records!")

        print("Durations saved for: {0}".format(d.strftime("%Y-%m-%d")))


@scheduler.scheduled_job('cron', day_of_week='sun', hour=23)
def run_the_program():
    if not os.path.exists(FILE_NAME):
        print("It looks like this is the first time you run this script!")
        print("This is the start date: {0}".format(START_DATE))
        df = pd.DataFrame(columns=["date", "project", "duration"])
        write_data_to_dataframe(df, START_DATE, date.today())
        df.to_csv(FILE_NAME)
    else:
        df = pd.DataFrame.from_csv(FILE_NAME, header=0)
        # Here we don't need start_date because it is calculated from previous entries
        write_data_to_dataframe(df, START_DATE, date.today())
        df.to_csv(FILE_NAME)

    slack.upload_file(FILE_NAME)
    print("Data collection stopped and sent to Slack!")


scheduler.start()
