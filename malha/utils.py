# -*- coding: utf-8 -*-
from datetime import datetime


def parse_timestamp(ts_string):
    return datetime.utcfromtimestamp(
        float(ts_string.split('-')[0].replace('/Date(', '')) / 1000.0)
