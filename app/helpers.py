from datetime import datetime


def format_dbdatetime(dbdatetime):
    return dbdatetime.strftime('%-I:%M%p on %b %d, %Y')
