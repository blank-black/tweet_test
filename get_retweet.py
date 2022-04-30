import requests
import random
import time
from configparser import ConfigParser

config = ConfigParser()
config.read('config.cfg')
config.sections()
bearer_token = config['config']['bearer_token']
tweet_status_id = config['config']['tweet_status_id']


def create_url(pagination):
    params = "user.fields=description,created_at"
    if pagination:
        params += "&pagination_token={}".format(pagination)
    url = "https://api.twitter.com/2/tweets/{}/retweeted_by".format(tweet_status_id)
    return url, params


def bearer_oauth(r):
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RetweetedByPython"
    return r


def connect_to_endpoint(url, params):
    response = requests.request("GET", url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def main():
    pagination = ''
    user_list = []
    while True:
        try:
            url, params = create_url(pagination)
            json_response = connect_to_endpoint(url, params)
            return_data = json_response
            user_list += return_data['data']
            if 'next_token' in return_data['meta']:
                pagination = return_data['meta']['next_token']
            if not pagination:
                break
        except Exception as e:
            break
    random.seed(time.time())

    print(len(user_list))
    index = random.randrange(len(user_list))
    print(user_list[index])


if __name__ == "__main__":
    main()