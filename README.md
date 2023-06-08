# WebScrapVolleyball

## Setup Signal Cli Rest API

https://github.com/bbernhard/signal-cli-rest-api
https://github.com/filipre/signalbot-example 

1. 
```bash
docker run -p 8080:8080 \
    -v $(PWD)/signal-cli-config:/home/.local/share/signal-cli \
    -e 'MODE=normal' bbernhard/signal-cli-rest-api:0.64
```
2. open http://192.168.178.35:8080/v1/qrcodelink?device_name=RaspberryPi in browser and link device

3. 
```bash
docker run -d -p 8080:8080 --restart unless-stoppe \
    -v $(PWD)/signal-cli-config:/home/.local/share/signal-cli \
    -e 'MODE=json-rpc' bbernhard/signal-cli-rest-api:0.64
```

## Pip

```bash
pip freeze > requirements.txt
```

## Signal-Bot

Get Groups:
```bash
curl -X GET 'http://127.0.0.1:8080/v1/groups/+491794298507' | python -m json.tool > my-groups.json 
```

## Selenium

Download fitting chromedriver executable!


## Create Service
1. 
```bash
sudo vim /lib/systemd/system/<service-name>.service
[Unit]
Description=WebScraper for tournements on beachvolleyball.nrw
After=multi-user.target
StartLimitIntervalSec=120

[Service]
StartLimitBurst=20
Type=simple
User=pi
WorkingDirectory=/home/pi/dev/volleyball-webscraper
ExecStart=/home/pi/dev/volleyball-webscraper/venv/bin/python3.11  /home/pi/dev/volleyball-webscraper/src/app.py
Restart=allways

[Install]
WantedBy=multi-user.target
```

## Commands

```bash
ps -ef | grep python                                # Show python instances
systemctl list-units                                # Show all system services
sudo systemctl status volleyball-tracker.service    # For Service Status
sudo systemctl restart volleyball-tracker.service   # Restart service
```