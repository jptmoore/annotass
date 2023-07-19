import dateutil.parser
from datetime import datetime


class Date:
    def __init__(self, ctx: object) -> None:
        pass

    def __process_date(self, date_string: str) -> datetime | None:
        try:
            valid_datetime = dateutil.parser.parse(date_string)
            if valid_datetime.tzname() == "UTC":
                return valid_datetime
            else:
                return None
        except ValueError:
            return None

    def __in_range_helper(self, check: str, range: str) -> bool:
        match range.split("/"):
            case [d1, d2]:
                start = self.__process_date(d1)
                end = self.__process_date(d2)
                x = self.__process_date(check)
                if x and start and end != None:
                    return start <= x <= end
                else:
                    return False
            case _:
                return False

    def in_range(self, check: str, ranges: str) -> bool:
        if ranges == None:
            return True
        else:
            return any(
                self.__in_range_helper(check=check, range=r) for r in ranges.split(" ")
            )
