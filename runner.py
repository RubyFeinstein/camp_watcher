import click
import camp_watcher
import datetime


DATE_FORMAT = "%Y%m%d"


@click.command("watch")
@click.argument("park_id", type=int)
@click.option("--date", "-d", multiple=True, type=str)
def watch(park_id, date):
    if len(date) == 0:
        raise Exception("at least one date is required")
    dates = []
    for d in date:
        dates.append(datetime.datetime.strptime(d, DATE_FORMAT).date())

    camp_watcher.camp_watcher(park_id, dates)


if __name__ == "__main__":
    watch()
