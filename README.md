# GrafanaScreenshot

This is a tool that to help you capture screenshots of standard Grafana dashboards.


## Components

- `print_dashboard.py` - Uses Selenium to interact with the browser and save the screenshots to the script directory.
- `print_dash_bot.py` - Telegram bot that allows users to request screenshots of dashboards and receive the images directly in the chat.

## Install
    conda env create --name screencap --file=conda_env.yml
