#!/usr/bin/env python3
import re


def filter_datum(fields, redaction, message, separator):
    """ called filter_datum that returns the log message obfuscated: """
    pattern = "|".join(map(re.escape, fields))
    # print(f"Pattern : {pattern}")
    regex = re.compile(rf'(?:^|{re.escape(separator)})(?:{pattern})=[^;]*')

    return regex.sub(f'{redaction}', message)


if __name__ == "__main__":
    fields = ["password", "date_of_birth"]
    messages = [
        "name=egg;email=eggmin@eggsample.com;password=eggcellent;date_of_birth=12/12/1986;",
        "name=bob;email=bob@dylan.com;password=bobbycool;date_of_birth=03/04/1993;"]

    for message in messages:
        print(filter_datum(fields, 'xxx', message, ';'))
