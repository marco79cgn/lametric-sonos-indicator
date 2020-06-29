# Lametric Sonos Indicator

<p align="center">
  <img width="550" src="image.gif" />
</p>

This indicator displays the current song of your Sonos system on your Lametric Clock. The script should be running on a system like the [Raspberry Pi](https://www.raspberrypi.org/)) in your local network. This fork relies on the [node-sonos-http-api](https://github.com/jishi/node-sonos-http-api) and assumes you have it running as well. Unfortunately [official Lametric application](https://apps.lametric.com/apps/display_for_sonos/4961) is buggy and doesn't work correct at least for me. The [SoCo](https://github.com/SoCo/SoCo) python library has problems with the metadata of some of my favorite TuneIn radio stations (like 'Radioeins vom rbb'). Therefore I made this fork, removed the SoCo dependency and queried the metadata from Node Sonos HTTP api instead.

## Requirements

* [node-sonos-http-api](https://github.com/jishi/node-sonos-http-api) has to be running
* Requests

## Traditional Installation

Clone repository:
```
$ git clone git@github.com:marco79cgn/lametric-sonos-indicator.git
```
Create virtual env:
```
$ cd lametric-sonos-indicator
$ python3 -m venv venv
```
Activate virtual env:
```
$ source venv/bin/activate
```
That's almost it. Use `requirments.txt` to setup all python dependencies:
```
$ pip install -r requirements.txt
```
Get and create env variables [LAMETRIC_IP and LAMETRIC_API_KEY](https://lametric-documentation.readthedocs.io/en/latest/guides/first-steps/first-local-notification.html#find-api-key):
```
$ export LAMETRIC_API_KEY="e56b92_lametric_long_api_string_c2a0c4"
$ export LAMETRIC_IP="192.168.1.25"
$ export DELAY=30
$ export NODE_SONOS_HTTP_API_IP="192.168.1.10"
```
`DELAY` is a time in seconds how often the notifications are sent to your Lametric Time.
`NODE_SONOS_HTTP_API_IP` is the ip address of the host where your node sonos http api is running.

Launch it:
```
$ python3 main.py
```

## Docker

It's also possible to launch this indicator with Docker. Apply the following steps to build and run it:
```
cd lametric-sonos-indicator # -> this cloned repository

docker build -t lametric-sonos .

docker run \
  -d \
  --name lametric-sonos \
  --net host \
  --env LAMETRIC_IP="192.168.1.25" \
  --env LAMETRIC_API_KEY="e56b92_lametric_long_api_string_c2a0c4" \
  --env NODE_SONOS_HTTP_API_IP="192.168.1.10" \
  --env DELAY=60 \
  --restart unless-stopped \
  lametric-sonos
```

That's it. I hope this is useful for you.

**Links**: \
https://lametric-documentation.readthedocs.io/en/latest/index.html \
https://blog.aruehe.io/tag/lametric/ \
https://github.com/jishi/node-sonos-http-api/blob/master/README.md
