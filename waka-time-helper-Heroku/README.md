# Wakatime logger with Heroku

Use Heroku and Slack, so you won't have to run it manually

## Setup

1. Update the `config.ini` with:
    1. Wakatime api key
    2. Start date
    3. Slack token
    4. Slack channel name --> Be sure that you have a Slack channel with the exact name
2. Download the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
3. Deploy it to Heroku:

```sh
git init

heroku login
heroku apps:create <your-app-name>
heroku buildpacks:set heroku/python --app <your-app-name>

git add --all
git commit -m "init"
git push heroku master

heroku ps:scale app=1
```

After that it will run on every Sunday at 11 PM and it will send you a Slack message to your Slack channel
with your prepared `.csv` file.