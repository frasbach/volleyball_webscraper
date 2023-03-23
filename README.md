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
docker run -p 8080:8080 \
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

## Database
```bash
sudo apt-get install sqlite3
```

## Commands
```bash
ps -ef | grep python
```