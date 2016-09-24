#! /usr/bin/env python3
"""Train tickets query via command-line.

Usage:
    tickets [-gdtkz] <from> <to> <date>

Options:
    -h,--help   caidan
    -g          gaotie
    -d          dongche
    -t          tekuai
    -k          kuaisu
    -z          zhida

Example:
    tickets beijing shanghai 2016-08-25
"""
from docopt import docopt
from stations import stations
import requests
from prettytable import PrettyTable

class TrainCollection(object):

    # ???????/???? ??/????????????????????????
    header = 'train station time duration first second softsleep hardsleep hardsit'.split()

    def __init__(self, rows):
        self.rows = rows

    def _get_duration(self, row):
        """
        ????????
        """
        duration = row.get('lishi').replace(':', 'h') + 'm'
        if duration.startswith('00'):
            return duration[4:]
        if duration.startswith('0'):
            return duration[1:]
        return duration

    @property
    def trains(self):
        for row in self.rows:
            train = [
                # ??
                row['station_train_code'],
                '\n'.join([colored('green', row['from_station_name']),
                           colored('red', row['to_station_name'])]),
                '\n'.join([colored('green', row['start_time']),
                           colored('red', row['arrive_time'])]),
                # ??
                self._get_duration(row),
                # ???
                row['zy_num'],
                # ???
                row['ze_num'],
                # ??
                row['rw_num'],
                # ??
                row['yw_num'],
                # ??
                row['yz_num']
            ]
            yield train

    def pretty_print(self):
        """
        ??????????????????????????????
        `prettytable`??????????MySQL?????????????
        """
        pt = PrettyTable()
        # ????????
        pt._set_field_names(self.header)
        for train in self.trains:
            pt.add_row(train)
        print(pt)
def colored(color, text):
    table = {
        'red': '\033[91m',
        'green': '\033[92m',
        # no color
        'nc': '\033[0m'
    }
    cv = table.get(color)
    nc = table.get('nc')
    return ''.join([cv, text, nc])

def cli():
    """command-line interface"""
    arguments = docopt(__doc__)
    from_station = stations.get(arguments['<from>'])
    to_station = stations.get(arguments['<to>'])
    date = arguments['<date>']
    # ??URL
    url = 'https://kyfw.12306.cn/otn/lcxxcx/query?purpose_codes=ADULT&queryDate={}&from_station={}&to_station={}'.format(
        date, from_station, to_station
    )
    # ??verify=False???????
    r = requests.get(url, verify=False)
    rows = r.json()['data']['datas']
    trains = TrainCollection(rows)
    trains.pretty_print()

if __name__ == '__main__':
    cli()

