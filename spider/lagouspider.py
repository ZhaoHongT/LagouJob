#!/usr/bin/env python
# coding: utf-8

import os
import time

import requests

import sys
sys.path.append('./')

from util import toolkit
from util import excelhelper


def scrapy(jobname, cookie):
    req_url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'
    headers = {
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept-Encoding': 'gzip, deflate',
        'Host': 'www.lagou.com',
        'Origin': 'https://www.lagou.com',
        'Content-Type': 'Content-Type:application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://www.lagou.com/zhaopin/chanpinjingli1/2/?filterOption=2',
        'Cookie': cookie,
        'Proxy-Connection': 'keep-alive',
        'X-Anit-Forge-Code': '0',
        'X-Anit-Forge-Token': None
    }
    maxpagenum = \
        int(int(requests.post(req_url, params={'first': 'true', 'pn': 1, 'kd': jobname}, headers=headers).json()[
                    'content']['positionResult']['totalCount']) / 15)

    flag = True
    num = 1

    maxpagenum = 10

    filedir = '/Users/iceke/PycharmProjects/LagouJob/data/' + jobname

    if os.path.exists(filedir) is not True or os.path.isdir(filedir) is not True:
        os.mkdir(filedir)

    while flag:
        payload = {'first': 'true', 'pn': str(num), 'kd': jobname}

        response = requests.post(req_url, params=payload, headers=headers)
        if num > maxpagenum:
            flag = False

        if response.status_code == 200:
            job_json = response.json()['content']['positionResult']['result']
            print('正在爬取第 ' + str(num) + ' 页的数据...')
            print(job_json)
            f = open(filedir + '/' + jobname + '_' + str(num) + '.json', 'wt',
                     encoding='utf-8')
            f.write(str(job_json))
            f.flush()
            f.close()
        else:
            print('connect error! url = ' + req_url)

        num += 1
        time.sleep(2)


if __name__ == '__main__':
    configmap = toolkit.readconfig('/Users/iceke/PycharmProjects/LagouJob/job.xml')
    cookie = toolkit.readCookie('/Users/iceke/PycharmProjects/LagouJob/cookie.xml')

    for item, value in configmap.items():
        for job in value:
            print('start crawl ' + str(job.parameter) + ' ...')
            scrapy(job.parameter, cookie)

    excelhelper.process_json('/Users/iceke/PycharmProjects/LagouJob/data/',
                             '/Users/iceke/PycharmProjects/LagouJob/data/')
