import os, requests, statistics

def tg_send_msg(content):
    import sys
    from telethon import TelegramClient
    from telethon.tl.types import InputChannel
    client = TelegramClient('cv_stats_session', content['api_id'], content['api_hash'])
    client.start()
    output_channel_entity = None
    for d in client.iter_dialogs():
        if d.name == content["output"]:
            try:
                output_channel_entity = InputChannel(d.entity.id, d.entity.access_hash)
            except:
                output_channel_entity = content['output']
    if output_channel_entity is None:
        print("Sending message to %s on telegram is failure." % content['output'])
        sys.exit(1)

    async def send_msg():
        await client.send_message(output_channel_entity, content['content'])

    with client:
        client.loop.run_until_complete(send_msg())

    return 0

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

    content = '# For the locale %s in Common Voice\n' % locale
    content += '## Statistics dated on %s\n' % stats_date
    content += 'Total %s users = %s\n' % (locale, speakers)
    content += 'Validated & Recorded Voices = %s / %s hours\n' % (round(stats_valid_hour/60/60,1), round(stats_record_hour/60/60,1))
    content += 'Validated & Recorded Voices = %s / %s seconds\n' % (stats_valid_hour, stats_record_hour)
    content += '## Today Statistics\n'
    content += 'Today Recorded Clip Count = %s\n' % stats_daily_count
    content += 'Today Validated Clip Count = %s\n' % stats_votes_count
    content += 'Online users in last 10 hours:\n%s\n(Avg: %s, Max: %s, Min: %s)' % \
          (online_hours, round(statistics.mean(online_hours),1), max(online_hours), min(online_hours))
    return content


def __main__():
    locale = os.environ.get('CV_LOCALE')
    tg_config = {}
    tg_config["api_id"] = os.environ.get('TG_API_ID')
    tg_config["api_hash"] = os.environ.get('TG_API_HASH')
    tg_config["output"] = os.environ.get('TG_OUTPUT')
    if not locale:
        content = get_cv_stats()
    else:
        content = get_cv_stats(locale)
    if not tg_config["api_id"]:
        print(content)
    else:
        tg_config["api_id"] = int(tg_config["api_id"])
        tg_config["content"] = content
        tg_send_msg(tg_config)
    return 0


__main__()