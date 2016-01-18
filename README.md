# cragh

I have no idea what the name means.


# Usage

Get your Twitch password in oauth form [here](twitchapps.com/tmi)

First export these env vars:

```bash
export CRAGH_HOST="irc.twitch.tv"
export CRAGH_PORT=6667
export CRAGH_NICK="your_twitch_nick"
export CRAGH_PASS="oauth:your_password"
export CRAGH_CHAN="#your_twitch_nick"
```

```bash
python run.py
```


# Acknowledgements
[@affajapoz](https://github.com/affajapoz) - helped me with the initial tutorial
