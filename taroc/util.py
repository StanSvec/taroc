import os
import secrets
from datetime import datetime, timezone
from typing import Dict, Optional

import itertools
import yaml

from taroc import utilns
from taroc.utilns import NestedNamespace


def expand_user(file):
    if not isinstance(file, str) or not file.startswith('~'):
        return file

    return os.path.expanduser(file)


def read_yaml(stream) -> NestedNamespace:
    return utilns.wrap_namespace(yaml.safe_load(stream))


def read_yaml_file(file_path) -> NestedNamespace:
    with open(file_path, 'r') as file:
        return utilns.wrap_namespace(yaml.safe_load(file))


def split_params(params, kv_sep="=") -> Dict[str, str]:
    f"""
    Converts sequence of values in format "key{kv_sep}value" to dict[key, value]
    """

    def split(s):
        if len(s) < 3 or kv_sep not in s[1:-1]:
            raise ValueError(f"Parameter must be in format: param{kv_sep}value")
        return s.split(kv_sep)

    return {k: v for k, v in (split(set_opt) for set_opt in params)}


# TODO check whether the functions below are needed

def unique_timestamp_hex(random_suffix_length=4):
    return secrets.token_hex(random_suffix_length) + format(int(datetime.utcnow().timestamp() * 1000000), 'x')[::-1]


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def dt_from_utc_str(str_ts, is_iso=True) -> Optional[datetime]:
    if not str_ts:
        return None
    sep = "T" if is_iso else " "

    # Workaround: https://stackoverflow.com/questions/30999230/how-to-parse-timezone-with-colon to support Python <3.7
    if ":" == str_ts[-3:-2]:
        str_ts = str_ts[:-3] + str_ts[-2:]

    return datetime.strptime(str_ts, "%Y-%m-%d" + sep + "%H:%M:%S.%f%z")


def dt_to_iso_str(dt, default_val="N/A"):
    if not dt:
        return default_val

    return dt.astimezone().replace(tzinfo=None).isoformat(sep=' ', timespec='milliseconds')


def format_timedelta(td):
    mm, ss = divmod(td.seconds, 60)
    hh, mm = divmod(mm, 60)
    s = "%02d:%02d:%02d" % (hh, mm, ss)
    if td.days:
        def plural(n):
            return n, abs(n) != 1 and "s" or ""

        s = ("%d day%s, " % plural(td.days)) + s
    if td.microseconds:
        s = s + ".%06d" % td.microseconds
        # s = s + ("%f" % (td.microseconds / 1000000))[1:-3]
    return s


def sequence_view(seq, *, sort_key, asc, limit):
    sorted_seq = sorted(seq, key=sort_key, reverse=not asc)
    return itertools.islice(sorted_seq, 0, limit if limit > 0 else None)
