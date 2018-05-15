#!/usr/bin/python
# -*- coding: utf-8 -*-
# pylint: disable=C0103
# pylint: disable=E1101
import sys
import os
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import json
import urllib2


def getImageUrlFromFlickr(API_KEY, query, N):

    NUM_OF_PHOTO = str(N) #取得する画像URLの数
    option = '&sort=relevance&privacy_filter=1&content_type=1&per_page='+ NUM_OF_PHOTO +'&format=json&nojsoncallback=1'
    url = 'https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key='+ API_KEY + option

    #JSON形式で結果を取得
    register_openers()
    datagen, headers = multipart_encode({'text': query})
    request = urllib2.Request(url, datagen, headers)
    response = urllib2.urlopen(request)
    res_dat = response.read()

    url_list = [] #URLリスト
    template_url = 'https://farm%s.staticflickr.com/%s/%s_%s.jpg' #URLのテンプレート
    for i in json.loads(res_dat)['photos']['photo']:
        img_url = template_url % (i['farm'], i['server'], i['id'], i['secret'])
        url_list.append(img_url) #リストに画像URLを追加

    return url_list


def getData(url):
    basename = os.path.basename(url)
    response = urllib2.urlopen(url)
    data = response.read()
    open(basename, "wt").write(data)


def wget_lists(url_List):
    for url in url_list:
        print url
        basename = os.path.basename(url)
        print basename
        if not os.path.isfile(basename):
#            cmd = "wget %s" % url
#            os.system(cmd)
            getData(url)
        else:
            print "already exists", basename


if __name__ == '__main__':

    API_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    from setting import API_KEY

    # 5f0c6cfcb646d668

    if len(sys.argv) != 3:
        print("""usage: %s query num
        """  % sys.argv[0])
        exit()

    query = sys.argv[1]
    num = int(sys.argv[2])

    #API KEY, クエリ, 取得したい画像の数を渡す
    url_list = getImageUrlFromFlickr(API_KEY, query, num)

    #取得した画像URLを表示
    for url in url_list:
        print url

    if 1:
        imgDir = "imgDir"
        if not os.path.isdir(imgDir):
            os.mkdir(imgDir)

        outDir = os.path.join(imgDir, query)
        if not os.path.isdir(outDir):
            os.makedirs(outDir)
        os.chdir(outDir)
        wget_lists(url_list)

