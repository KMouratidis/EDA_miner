import re
import numpy as np
import pandas as pd
from fuzzywuzzy import fuzz


def can_into_date(col):
    """
    # Can handle with various separators \
    # e.g.: "-" or "/" or " " \
    # (time MUST be separated with ":")
        YYYY
        YYYY-MM
        MM-YYYY
        YYYY-MM-DD
        MM-DD-YYYY
        DD-MM-YYYY
        DD-MM-YYYY-HRS:MIN
        June 1995
        03 June 1995
        03 Jun 1995
        03 June 1995 15:32
        15:32 16 Jun 2015
        15:32 16th Jun 2015
        15:32 Jun 16th 2015

    # Partially handles
        15:32  # assumed: Today

    # Cannot handle
        YYYY-DD-MM

    # Incorrectly handles
        int
        float
    """

    try:
        pd.to_datetime(col)
        return True
    except ValueError:
        return False


def can_into_categorical(col, threshold=None):
    """
    Convert to categorical IF the unique values are fewer than some threshold.
    """

    n_rows = col.shape[0]
    n_unique = col.nunique()

    if isinstance(threshold, float):
        return (n_unique < threshold * n_rows)

    elif isinstance(threshold, int):
        return (n_unique < threshold)

    elif threshold == "sqrt":
        return (n_unique < np.sqrt(n_rows))

    elif threshold == "log":
        return (n_unique < np.log(n_rows))

    else:
        # We choose a max of 100 since larger values cannot be visualized very well
        return (n_unique < max(min(np.log(n_rows), np.sqrt(n_rows), n_unique), 100))


def can_into_int(col):
    """
    Attempt to convert to int.
    """

    try:
        col.astype(np.int32)
        return True
    except ValueError:
        return False


def column_name_match(col_name, list_of_words, match_threshold=55):
    """
    Helper for matching column names to a list of words.
    """

    return any((fuzz.QRatio(word, col_name) > match_threshold)
               for word in list_of_words)


def infer_types(df, is_sample=False):
    """
    Guess data types.
    float > int > datetime > categorical > string

    1. "Unsafe" assumption. Try to infer datatypes by using directly \
       "tests" / "transformations".
    2. "Lenient" assumption. Pass once over column headers and try to \
       guess the column. Apply the "test" / "transformation" to see if \
       it works. Overwrite if necessary.
    3. Try to guess subtypes.
    4. Anything the user explicitly corrects.

    Args:
        df (`pd.DataFrame`): Dataframe on which to run data type inference.
        is_sample (`bool`): If True then df will be treated as being a sample.

    Returns:
        list(dict): Types and subtypes.

    Todo:
        When saving these make sure that the 1st and 2nd are marked as \
        inferred while the 3rd is marked as "ground truth".
    """

    # Don't include "month", "day" etc because they cannot be parsed as time on their own
    time_words = ["year", "time", "date", "datetime", "date time", "date_time"]
    int_words = ["code", "age"]
    float_words = ["weight", "lat", "latitude", "lon", "long", "longitute", "distance",
                   "length", "width"]  # LGTM[useless-code]
    categorical_words = ["sex", "gender", "state", "country"]

    # Define some patters for regex matching for subtypes
    mails = re.compile(".*@.*\..*")
    ipv4 = re.compile("(\d{1,3}\.){3}\d{1,3}")
    ipv6 = re.compile("([0-9a-f]{4}:){7}[0-9a-f]{4}")
    mac_address = re.compile("([0-9a-f]{2}:){5}[0-9a-f]{2}")

    # 0. Attempt to fillna()
    df = df.fillna(np.nan)
    # Get a sample (or copy if it already is a sample)
    if is_sample:
        sample = df.copy()
    else:
        sample = df.sample(n=50, replace=True).dropna()

    # 1. Attempt to infer based on datatype.
    unsafe = {}
    for col_name in df.columns:

        # https://stackoverflow.com/a/37727662/6655150
        if np.issubdtype(sample[col_name], np.floating):
            unsafe[col_name] = "float"

        elif np.issubdtype(sample[col_name], np.integer):
            unsafe[col_name] = "integer"

        elif can_into_date(sample[col_name]):
            unsafe[col_name] = "date"

        # Not on sample, because we use calculate statistics
        elif can_into_categorical(df[col_name]):
            unsafe[col_name] = "categorical"

        else:
            unsafe[col_name] = "string"

    # 2. Try to determine datatype with column headers
    lenient = {}
    for col_name in df.columns:

        # Float columns can be anything, so ignore for now

        # Int
        if column_name_match(col_name, int_words) and (
                (np.issubdtype(sample[col_name], np.number) or
                 can_into_int(sample[col_name]))):

            lenient[col_name] = "integer"

        # Date
        elif (column_name_match(col_name, time_words) and
                can_into_date(df[col_name])):

            lenient[col_name] = "date"

        # Category
        elif (column_name_match(col_name, categorical_words) and
                can_into_categorical(df[col_name])):

            lenient[col_name] = "categorical"

    # Update the unsafe assumption with the lenient one to form the
    # base / high-level types
    high_level_types = unsafe.copy()
    high_level_types.update(lenient)

    # 3. Try to guess sub-types.
    sub_categories = {}
    for col_name in df.columns:
        dtype = high_level_types[col_name]

        # Initialize subtype to high-level type
        sub_categories[col_name] = dtype

        # Try to update to more specific

        if dtype == "categorical" and df[col_name].nunique() == 2:
            sub_categories[col_name] = "binary"

        elif dtype == "float":
            if col_name in ["lat", "latitude"]:
                sub_categories[col_name] = "latitude"

            elif col_name in ["lon", "long", "longitute"]:
                sub_categories[col_name] = "longitude"

        elif dtype == "string":
            # Check every pattern
            for pattern, subtype in zip([mails, ipv4, ipv6, mac_addr],
                                        ["email", "ipv4", "ipv6", "mac_addr"]):
            
                # If all the rows in the sample match, assume the subtype
                if all(pattern.match(x) for x in sample[col_name]):
                    sub_categories[col_name] = subtype

    return [high_level_types, sub_categories]
