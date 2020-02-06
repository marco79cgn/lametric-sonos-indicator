import soco

import json
import requests
import time

import settings

class LaSo:
    def __init__(self, lametric_ip, lametric_user, lametric_key, sonos):
        self.lametric_ip = lametric_ip
        self.lametric_user = lametric_user
        self.lametric_key = lametric_key
        self.sonos = sonos

    def get_track(self):
        track = self.sonos.get_current_track_info()
        status = self.sonos.get_current_transport_info()
        return track, status

    def send_notification(self):
        track, status = self.get_track()

        if status['current_transport_state'] == 'PLAYING':

            artist = track['artist']
            title = track['title']

            api_url = "http://%s:8080/api/v2/device/notifications" % (self.lametric_ip)
            headers = {'Content-Type': 'application/json; charset=utf-8'}
            basicAuthCredentials = (self.lametric_user, self.lametric_key)
            data = '{"model":{"frames":[{"icon":"19113","text":"%s - %s"}]}}' % (artist, title)
            response = requests.post(api_url,
                                     headers=headers,
                                     auth=basicAuthCredentials,
                                     data=data.encode('utf-8'))

def main():
    # If you wish to show specific speaker song use its IP
    # sonos = soco.SoCo('192.168.1.86')
    sonos = soco.discovery.any_soco()
    laso = LaSo(settings.lametric_ip,
                "dev",
                settings.lametric_api_key,
                sonos)
    while True:
        laso.get_track()
        laso.send_notification()
        time.sleep(60)

if __name__ == "__main__":
    main()