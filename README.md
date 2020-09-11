# TwitterFeedCleaner
Python script that helps you discover the outdated accounts that you follow on Twitter.

## Usage:
First of all, add your Twitter Bearer Token in a environment variable called 'TWITTER_AUTH_KEY' then execute it through the command line as follows:
    
    usage: feed_cleaner.py [-h] [-c COUNT] [-m MONTHS_OLD] username
    positional arguments:
      username              the username to retrieve the info from

    optional arguments:
      -h, --help            show this help message and exit
      -c COUNT, --count COUNT
                            the profile count to retrieve at once. Maximum and default: 200
      -m MONTHS_OLD, --months MONTHS_OLD
                            how many months to consider a profile 'old'. Default: 1
