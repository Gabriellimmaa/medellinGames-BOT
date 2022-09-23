# 🤖 medellinGames BOT

---


## ⚙️ Description

This project was developed for a discord server whose name is MedellinGames (@medellingames), the bot has a system to verify tweets to receive benefits from the bot, draws a 4x4 team of members on call, has the possibility to create fans to win benefits .

## 🎮 Commands

The chatbot contains the following commands:

- **!join:** Starts a tournament;
- **!vip:** Get your daily vip by tweet;
- **!torcida:** Consult a player's crowd or create a new one;
- **!torcidas:** Displays the list with all the twists;
- **!aprovar:** Approve a crowd;

---

## 🛠️ Developed with

For the development of this chatbot I used the following technologies:

- python 3.9.10;
- pymongo==3.12.3
- motor==2.5.1
- tweetpy==4.10.0
- git+https://github.com/Rapptz/discord.py

All library versions are in requirements.txt

---
## 🔧 Getting started

This project requires python 3.9.10;

1. Clone the repository
```bash
git clone https://github.com/Gabriellimmaa/medellinGames-BOT.git
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Edit the config.ini

```bash
[twitter]
api_key = YOUR_API_KEY
api_key_secret = YOUR_API_KEY
access_token = YOUR_API_TOKEN
access_token_secret = YOUR_API_TOKEN
client_id = YOUR_CLIENT_ID
client_secret = YOUR_CLIENT_SECRET
bearer_token = YOUR_BEARER_TOKEN

[discord]
discord_token = YOUR_DISCORD_TOKEN
```

4 Run the project
```bash
python main.py
```

---

## ✒️ Author

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/Gabriellimmaa">
        <img src="https://avatars3.githubusercontent.com/u/42157830" width="100px;" alt="Photo by Gabriel Lima on GitHub"/><br>
        <sub>
          <b>Gabriel Lima</b>
        </sub>
      </a>
    </td>
  </tr>
</table>

---

Thank you for taking the time to read about my work.

Any questions, criticisms or suggestions, please contact us, <a href="mailto:gabriellimamoraes@gmail.com/">contact</a> by my email
