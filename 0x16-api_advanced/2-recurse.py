#!/usr/bin/python3
"""
Recursively for all hot articles of a given subreddit
"""
import sys
import requests

def recurse(subreddit, hot_list=[], after="tmp"):
    """
        Return all hot articles for a given subreddit
        or None if an invalid subreddit is given
    """
    headers = requests.utils.default_headers()
    headers.update({'User-Agent': 'My User Agent 1.0'})

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    if after != "tmp":
        url = url + "?after={}".format(after)
    r = requests.get(url, headers=headers, allow_redirects=False)

    results = r.json().get('data', {}).get('children', [])
    if not results:
        if after == "tmp":
            return None
        return hot_list
    for e in results:
        hot_list.append(e.get('data').get('title'))

    after = r.json().get('data').get('after')
    if not after:
        return hot_list
    return recurse(subreddit, hot_list, after)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please pass an argument for the subreddit to search.")
    else:
        result = recurse(sys.argv[1])
        if result is not None:
            print(len(result))
        else:
            print("None")
