from datetime import datetime, timedelta, UTC





def parse_datetime_to_unix(timestamp: datetime, days: int | None = None) -> dict: 
    
    parsed_dates = {
        "timestamp_str": timestamp.strftime("%Y%m%d_%H%M"), 
        "timestamp_unix": int(timestamp.timestamp())
        }

    if days is not None: 
        previous_date = timestamp-timedelta(days=days)
        # Rest x days from timestamp and convert to string
        parsed_dates["previous_str"] = previous_date.strftime("%Y%m%d_%H%M")
        # Convert x previous days date to unix
        parsed_dates["previous_unix"] = int(previous_date.timestamp())

    return parsed_dates