# @Author: archer
# @Date:   2020-01-21
# @Last modified by:   archer
# @Last modified time: 2020-01-21

# this is the most barebones csv cleaner ever, you may want to drastically add
# to this file to suit your needs

import pandas as pd


def cleanHeader(df):
    # make column headers to lowercase
    df.columns = map(str.lower, df.columns)
    # stripping whitespace at front and end of the column headers list
    df.columns = df.columns.str.strip()
    # replacing spaces with underscores of column headers list
    df.columns = df.columns.str.replace(" ", "_")
    df.columns = df.columns.str.replace("-", "_")
    # additional change just to make data look nicer in my horrible case
    df.columns = df.columns.str.replace("___", "_")
    return df


def cleanContents(df):
    # this is the name of my date and time colummn in my case change to yours
    # so that this can properly convert to a datetime field
    df["date_&_time"] = pd.to_datetime(df["date_&_time"],
                                       infer_datetime_format=True)
    # note no normalisation happens here for me but it may be appropriate for
    # you to add some in your case here
    return df


def main(**kwargs):
    print(kwargs)
    args = kwargs["args"]
    # this gives us our process number which we can use to get our files etc
    process = args["process"]
    # this gets out data files list which we then pick which one we need
    # there can be multiple here but we get it using our process number
    print(args["data"][process])
    # this opens our csv file and removes any potential turds that come from
    # certain datasets
    with open(args["data"][process],
              mode='r', encoding='utf-8', errors='ignore') as f:
        # change this to be appropriate for your data such as where to skip to
        df = pd.read_csv(f, header=0,
                         skiprows=list(range(0, 5)),
                         na_values=["--"])

    df = cleanHeader(df)
    df = cleanContents(df)
    # while we are writing this file we may want a file output to preview
    # df.to_csv("./data/weather_data_clean.csv")
    print(df.head())
    for row in df.to_dict("records"):
        yield row


# testing the file standalone
if __name__ == "__main__":
    for _ in main():
        pass
