import json
import requests
import time
import os

class LaSo:
    def __init__(self, lametric_ip, lametric_user, lametric_api_key, node_sonos_http_api_ip):
        self.lametric_ip = lametric_ip
        self.lametric_user = lametric_user
        self.lametric_api_key = lametric_api_key
        self.node_sonos_http_api_ip = node_sonos_http_api_ip

    def get_track(self):
        node_sonos_http_api_url = "http://%s:5005/state" % (self.node_sonos_http_api_ip) 
        response = requests.get(node_sonos_http_api_url)
        if response.status_code == 200:
            json_response = response.json()
            track = {
                "title": json_response['currentTrack']['title'],
                "artist": json_response['currentTrack']['artist'],
            }
            status = json_response['playbackState']
        else:
            track = {
                "title": "",
                "artist": "",
            } 
            status = "STOPPED"
        return track, status

    def send_notification(self):
        track, status = self.get_track()

        if status == 'PLAYING':

            artist = track['artist']
            title = track['title']

            api_url = "http://%s:8080/api/v2/device/notifications" % (self.lametric_ip)
            headers = {'Content-Type': 'application/json; charset=utf-8'}
            basicAuthCredentials = (self.lametric_user, self.lametric_api_key)
            data = '{"priority":"warning","model":{"frames":[{"icon":"19113","text":"%s: %s"}],"cycles":3}}' % (artist, title)
            try:
                response = requests.post(api_url,
                                         headers=headers,
                                         auth=basicAuthCredentials,
                                         data=data.encode('utf-8'),
                                         timeout=3)
                # for debugging purpose
                print(f"{artist} - {title}")
            except requests.exceptions.RequestException as err:
                print ("OOps: Something Else", err)
            except requests.exceptions.HTTPError as errh:
                print ("Http Error:", errh)
            except requests.exceptions.ConnectionError as errc:
                print ("Error Connecting:", errc)
            except requests.exceptions.Timeout as errt:
                print ("Timeout Error:", errt)  

def main():
    laso = LaSo(os.environ["LAMETRIC_IP"],
                "dev",
                os.environ["LAMETRIC_API_KEY"],
                os.environ["NODE_SONOS_HTTP_API_IP"])
    # if envar DELAY isn't set than it equals 60
    delay = os.getenv('DELAY', 60)
    # print(delay)

    while True:
        laso.get_track()
        laso.send_notification()
        time.sleep(int(delay))

if __name__ == "__main__":
    main()
