
# cnames.txtからchans.txtを作る

import os
import argparse
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

DEVELOPER_KEY = os.environ['DEVELOPER_KEY']
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def youtube_search(options):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

    search_response = youtube.search().list(
        q=options.q,
        part='id,snippet',
        maxResults=options.max_results,
        type = 'channel',     
    ).execute()

    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#channel':
            f = open('cids.txt','a')
            f.write(search_result['id']['channelId'])
            f.write('\n')
            f.close()

if __name__ == '__main__':

    # cids.txtファイルに上書き
    f = open('cids.txt','w')
    f.close()

    # cnames.txtから読み込む
    f1 = open('cnames.txt', 'r')
    cnames = []
    for y in f1:
        cnames.append(y.rstrip('\n'))
    f1.close

    for cname in cnames:
        parser = argparse.ArgumentParser()
        parser.add_argument('--q', help='Search term', default=cname)
        parser.add_argument('--max-results', help='Max results', default=1)
        args = parser.parse_args()

        try:
            youtube_search(args)
        except HttpError as e:
            print ('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))