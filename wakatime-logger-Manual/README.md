# Wakatime logger Manual

## Setup

1. clone the repo:
	- `git clone https://github.com/gaborvecsei/WakaTime-Logger.git`
	- `cd WakaTime-Logger` -> go inside `WakaTime-Logger` folder
	- `cd wakatime-logger-Manual` -> go inside `wakatime-logger-Manual` folder
2. Update the `config.ini` with:
    1. [Wakatime api key](https://wakatime.com/developers)
    2. Start date

The start date is used for the first run.
Don't worry if you don't remember the first date for the logging,
it will recognize if a date is "valid", so it has time information stored.

## Usage

Just run it: `python wakatime_logger.py`

(Make sure that you run the script once per week, so it won't skip days because of your wakatime free plan)