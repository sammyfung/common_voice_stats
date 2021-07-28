[![CI](https://github.com/sammyfung/common_voice_stats/actions/workflows/main.yml/badge.svg)](https://github.com/sammyfung/common_voice_stats/actions/workflows/main.yml)

Common Voice Statistics
-----------------------

This is a script to collect common voice statistics from the website. Default locale is zh-HK aka Chinese (Hong Kong).

You can set a enviornment variable CV_LOCALE to check the statistics of other locales in Common Voice project.

If you would like to send the stats data to telegram, you can create your API ID and HASH on me.telegram.org and then set the following enviornment variables: TG_API_ID, TG_API_HASH, TG_OUPUT (The name of output group/channel).

## Run

```
python collect_cv_stats.py
```
