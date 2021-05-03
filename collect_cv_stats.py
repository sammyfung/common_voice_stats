import os, requests, codecs, json, statistics


def get_cv_stats(locale='zh-HK'):
    cv_url_prefix = 'https://commonvoice.mozilla.org/api/v1/'
    clips_stats_url = cv_url_prefix + locale + '/clips/stats'
    clips_daily_count_url = cv_url_prefix + locale + '/clips/daily_count'
    clips_daily_votes_url = cv_url_prefix + locale + '/clips/votes/daily_count'
    clips_online_users_url = cv_url_prefix + locale + '/clips/voices'
    language_stats_url = cv_url_prefix + 'language_stats'

    wp = requests.get(language_stats_url, stream=True)
    language_stats = wp.json()
    speakers = 0
    for i in language_stats['launched']:
        if i['locale'] == locale:
            speakers = i['speakers']

    wp = requests.get(clips_daily_count_url, stream=True)
    stats_daily_count = wp.text

    wp = requests.get(clips_daily_votes_url, stream=True)
    stats_votes_count = wp.text

    wp = requests.get(clips_stats_url, stream=True)
    data_stats = wp.json()
    #data_stats = json.load(codecs.iterdecode(result_stats.iter_lines(), 'utf-8'))
    stats_date = ''
    stats_record_hour = 0
    stats_valid_hour = 0
    for i in data_stats:
        stats_date = i['date']
        stats_record_hour = i['total']
        stats_valid_hour = i['valid']

    wp = requests.get(clips_online_users_url, stream=True)
    data_stats = wp.json()
    online_hours = []
    for i in data_stats:
        online_hours += [i['value']]

    print('For the locale %s in Common Voice dated %s' % (locale, stats_date))
    print('--')
    print('Validated & Recorded Voices = %s / %s hours' % (round(stats_valid_hour/60/60,1), round(stats_record_hour/60/60,1)))
    print('Validated & Recorded Voices = %s / %s seconds' % (stats_valid_hour, stats_record_hour))
    print('Daily Recorded Clip Count = %s' % stats_daily_count)
    print('Daily Validated Clip Count = %s' % stats_votes_count)
    print('Total %s users = %s' % (locale, speakers))
    print('Online users in last 10 hours: %s (Avg: %s, Max: %s, Min: %s)' % \
          (online_hours, round(statistics.mean(online_hours),1), max(online_hours), min(online_hours)))


def __main__():
    locale = os.environ.get('CV_LOCALE')
    if not locale:
        get_cv_stats()
    else:
        get_cv_stats(locale)
    return 0


__main__()