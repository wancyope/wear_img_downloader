#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import time
import os
import sys

from urllib import request
from bs4 import BeautifulSoup

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--target_dir","-dir",default="images")
    parser.add_argument("--gender","-gen",default="women")
    parser.add_argument("--tag_id","-id",default="1568")
    args = parser.parse_args()
    month=1
    if args.gender=="men":
        url = "http://wear.jp/men-coordinate/?tag_ids="+args.tag_id+"&from_month="+str(month)+"&to_month="+str(month)+"&type_id=2"
    elif args.gender=="women":
        url = "http://wear.jp/women-coordinate/?tag_ids="+args.tag_id+"&from_month="+str(month)+"&to_month="+str(month)+"&type_id=2"
    
    dirname = args.target_dir
    if not os.path.isdir(dirname):
        os.mkdir(dirname)
        
    images_sum = 0
    i = 0
    for j in range(1,13):
        while True:
            #Beautiful Soupで抽出
            start_time = time.time()
            headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0", }
            req = request.Request(url=url,headers=headers)
            response = request.urlopen(req)
            body = response.read()
            soup = BeautifulSoup(body)
            images_all = soup.find_all('img')
            for img in images_all:
                data = img.get("data-original")
                #"wimg.jp/coordinate"という文字列が含まれる画像URLから画像ダウンロード
                if "wimg.jp/coordinate" in str(data):
                    data=data.replace('_276','_500')
                    img = request.urlopen(data)
                    localfile = open(dirname + "/" + os.path.basename(data), 'wb')
                    localfile.write(img.read())
                    img.close()
                    localfile.close()
                    sys.stderr.write('{} \r'.format(images_sum))
                    sys.stderr.flush()
                    images_sum += 1
            #次のページが無かったらループ抜ける
            try:
                next_page = soup.find('link',rel="next").get("href")
            except Exception:
                break
            #待機時間を作っている
            end_time = time.time()
            sleep_time = 1 - (end_time - start_time)
            if sleep_time > 0:
                time.sleep(1)
                
            url = next_page
            i += 1
        if j == 12:
            break
        #次の月へ
        tmp = "from_month=" + str(month) + "&to_month=" + str(month) + "&"
        tmp2 = tmp.replace(str(month),str(month+1))
        url = url.replace(tmp,tmp2)
        month += 1
    print(images_sum)
