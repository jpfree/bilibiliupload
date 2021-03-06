# import json
# import re
import requests
from Engine.plugins import Download, BatchCheckBase
# from common import logger

headers = {
    'client-id': 'jzkbprff40iqj646a697cyrvl0zt2m6'
}
VALID_URL_BASE = r'(?:https?://)?(?:(?:www|go|m)\.)?twitch\.tv/(?P<id>[0-9_a-zA-Z]+)'
API_ROOMS = 'https://api.twitch.tv/helix/streams'
_API_USER = 'https://api.twitch.tv/helix/users'


class Twitch(Download):
    def __init__(self, fname, url, suffix='mp4'):
        Download.__init__(self, fname, url, suffix=suffix)

    # def check_stream(self):
    #
    #     check_url = re.sub(r'.*twitch.tv', 'https://api.twitch.tv/kraken/streams', self.url)
    #     try:
    #         res = requests.get(check_url, headers=headers)
    #         res.close()
    #     except requests.exceptions.SSLError:
    #         logger.error('获取流信息发生错误')
    #         logger.error(requests.exceptions.SSLError, exc_info=True)
    #         return None
    #     except requests.exceptions.ConnectionError:
    #         logger.exception('During handling of the above exception, another exception occurred:')
    #         return None
    #
    #     try:
    #         s = json.loads(res.text)
    #         # s = res.json()  https://api.twitch.tv/kraken/streams/
    #     except json.decoder.JSONDecodeError:
    #         logger.exception('Expecting value')
    #         return None
    #     print(self.fname)
    #     try:
    #         stream = s['stream']
    #     except KeyError:
    #         logger.error(KeyError, exc_info=True)
    #         return None
    #     return stream

    def download(self, ydl_opts, event):
        info_list = self.get_sinfo()

        if self.fname in ['星际2ByuN武圣人族天梯第一视角', '星际2INnoVation吕布卫星人族天梯第一视角', '星际2Maru人族天梯第一视角']:
            pass
        elif '720p' in info_list:
            ydl_opts['format'] = '720p'
        elif '720p60' in info_list:
            ydl_opts['format'] = '720p60'

        self.dl(ydl_opts)


class BatchCheck(BatchCheckBase):
    def __init__(self, urls):
        BatchCheckBase.__init__(self, pattern_id=VALID_URL_BASE, urls=urls)
        self.use_id = {}
        login = requests.get(_API_USER, headers=headers, params={'login': self.usr_list})
        try:
            for pair in login.json()['data']:
                self.use_id[pair['id']] = pair['login']
        except KeyError:
            print(login.json())
            return
        login.close()

    def check(self):

        live = []
        usr_list = self.usr_list
        if not usr_list:
            print('无用户列表')
            return
        # url = 'https://api.twitch.tv/kraken/streams/sc2_ragnarok'

        stream = requests.get(API_ROOMS, headers=headers, params={'user_login': usr_list})
        stream.close()

        data = stream.json()['data']
        if data:
            for i in data:
                live.append(self.use_id[i['user_id']])
        else:
            print('twitch无开播')

        return map(lambda x: self.usr_dict.get(x.lower()), live)


__plugin__ = Twitch
