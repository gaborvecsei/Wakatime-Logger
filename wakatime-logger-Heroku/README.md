# Wakatime logger with Heroku

Use Heroku and Slack, so you won't have to run it manually

With this method the code will run in a Heroku container so you won't have to run it every time manually.
It won't forget to run itself. :heart_eyes:

After the script is executed, you will receive an automatic message from a Slack bot with the `.csv` file which
contains the durations for the projects.

## Setup

1. clone the repo:
	- `git clone https://github.com/gaborvecsei/WakaTime-Logger.git`
	- `cd WakaTime-Logger` -> go inside `WakaTime-Logger` folder
	- `cd wakatime-logger-Heroku` -> go inside `wakatime-logger-Heroku` folder
2. Update the `config.ini` with:
    1. [Wakatime api key](https://wakatime.com/developers)
    2. Start date
    3. [Slack token](https://api.slack.com/custom-integrations/legacy-tokens)
    4. Slack channel name --> Be sure that you have a Slack channel with the exact name
3. Download the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
4. Deploy it to Heroku:

```shell
git init

heroku login
heroku apps:create <YOUR_APP_NAME>
heroku buildpacks:set heroku/python --app <YOUR_APP_NAME>

git add --all
git commit -m "init"
git push heroku master

heroku ps:scale app=1
```

After that it will run on every Sunday at 11 PM (you can edit this time in the code) and it will send you a Slack message to your Slack channel
with your prepared `.csv` file.