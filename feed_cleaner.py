import requests
import time
import os
import sys
from datetime import datetime
from dateutil.relativedelta import relativedelta

FOLLOWING_ENDPOINT = r'https://api.twitter.com/1.1/friends/list.json'
DATE_FORMAT = '%a %b %d %H:%M:%S +0000 %Y'

def print_outdated_profiles(
    username: str,
    months_old: int = 1,
    iter_count: int = 200):
    
    params = { 'screen_name': username, 'count': iter_count, 'cursor': -1 }

    try:
        headers = { 'Authorization': f"Bearer {os.environ['TWITTER_AUTH_KEY']}" }
    except KeyError:
        print("ERROR: Could not find environment variable 'TWITTER_AUTH_KEY' containing a valid key for the Twitter API")
        sys.exit(1)

    outdated_profiles = []

    while params['cursor'] != 0:
        response = requests.get(
            FOLLOWING_ENDPOINT,
            params=params,
            headers=headers)

        parsed_response = response.json()

        if not response.ok:
            print(f'ERROR: unexpected error sending the request: {parsed_response}')
            sys.exit(1)

        users = parsed_response['users']

        print(f'Fetched {len(users)} profiles!')
        params['cursor'] = parsed_response['next_cursor']

        for user in users:
            status = user.get('status')
            created_at = status.get('created_at') if status else None
            if created_at is not None:
                parsed_time = datetime.strptime(created_at, DATE_FORMAT)
            
            if parsed_time < (datetime.now() - relativedelta(months=months_old)):
                screen_name = user.get('screen_name')
                outdated_profiles.append(f'https://twitter.com/{screen_name}/')

        time.sleep(1)

    print('Outdated profiles:')
    for profile_link in outdated_profiles:
        print(profile_link)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    
    parser.add_argument(
        dest='username',
        help='the username to retrieve the info from')

    parser.add_argument(
        '-c', '--count',
        dest='count', type=int,
        required=False, default=200,
        help='the profile count to retrieve at once. Maximum and default: 200')

    parser.add_argument(
        '-m', '--months',
        dest='months_old', type=int,
        required=False, default=1,
        help="how many months to consider a profile 'old'. Default: 1")

    args = parser.parse_args()
    print_outdated_profiles(args.username, args.months_old, args.count)
    input('Press any key to exit...')