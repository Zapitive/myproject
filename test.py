from condb import *
from elecdetails import *
from datetime import datetime, timedelta

def test_t():
    data = elecdetails(1)
    if data[0][4] >= datetime.now():
        return "election is not started"
    elif data[0][5] <= datetime.now():
        return "election has ended"
    else:
        return "election is ongoing"
