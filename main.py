import config
import rss
import gcalendar

token_name = config.token_name


def check_ya_neck():
    for i in range(0, 16):
        game = rss.check_for_game(config.feed_url, i)
        if game:
            name = game["name"]
            date = game["date"]
            print(gcalendar.iso_date(date))

game = rss.check_for_game(config.feed_url, 1)
gcalendar.make_event(game, config.calendar_id, config.token)

