
# cids.txtとcnames.txtからyoutuberの交友関係を表すyoutuber.txtを作る

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

    # channelIdの動画の中で検索語qと関連性がある動画を上位2件取ってくる
    search_response = youtube.search().list(
        q=options.q,
        channelId=options.channelId,
        part='id,snippet',
        maxResults=options.max_results,
        type='video'
    ).execute()

    flag = 0

    # 取ってきた動画が本当にコラボ動画かどうか調べる,コラボ動画だったらyoutuber.txtに書き込む
    for search_result in search_response.get('items', []):
        # 1:タイトル内にchannel名が含まれているか
        index1 = search_result['snippet']['title'].find(options.q)
        # 2:概要欄にchannel名が含まれているか
        index2 = search_result['snippet']['description'].find(options.q)
        # 3:概要欄にchannelIDが含まれているか
        index3 = search_result['snippet']['description'].find(options.qId)
        if ((index1 != -1  or index2 != -1 or index3 != -1) 
            and flag == 0 and search_result['snippet']['channelTitle'] != options.q):
            flag = 1
            # txtファイル用にchannel名に含まれる空白を削除
            text = (options.q).replace(" ", "") + ' ' + (search_result["snippet"]["channelTitle"]).replace(" ", "")
            # 'a'は上書きでなく追記
            f = open('youtuber.txt','a')
            f.write(text)
            f.write('\n')
            f.close()
            return 1
    return 0

if __name__ == '__main__':
    # youtuber.txtファイルに上書き
    f = open('youtuber.txt','w')
    f.close()

    # cids.txtから読み込む
    f1 = open('cids.txt','r')
    cids = []
    for x in f1:
        cids.append(x.rstrip('\n'))
    f1.close()

    # cnames.txtから読み込む
    f2 = open('cnames.txt', 'r')
    cnames = []
    for y in f2:
        cnames.append(y.rstrip('\n'))
    f2.close

    # すでに交友関係が示されたペアについては再検索を行わないようにする(計算を減らすため)
    # 二次元配列で交友関係がすでにあるか,ないか,を管理する
    search_list = [[0 for i in range(len(cids))] for j in range(len(cnames))]
    for k in range(len(cids)):
        search_list[k][k] = 1
    
    for i, cname in enumerate(cnames):
        for j, cid in enumerate(cids):
            if search_list[i][j] != 1:
                parser = argparse.ArgumentParser()
                parser.add_argument('--q', help='Search term', default=cname)
                # 検索語qのidも渡して概要欄にqのidが含まれるかの判定に使う
                parser.add_argument('--qId', help='Search terms ID', default=cids[i])
                parser.add_argument('--channelId', help='SearchFromId', default=cid)
                parser.add_argument('--max-results', help='Max results', default=2)
                args = parser.parse_args()
                try:
                    result = youtube_search(args)
                    # i,jのペアで交友関係があった場合には
                    # listのi,j成分と、その対角成分も1(交友関係有)にする
                    if result:
                        search_list[i][j] = 1
                        search_list[j][i] = 1
                except HttpError as e:
                    print ('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))