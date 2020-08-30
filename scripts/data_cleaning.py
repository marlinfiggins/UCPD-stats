import pandas as pd


def standardize_race(race):
    """
    Takes in "Race" entry and returns in standardized format.
    """
    race = str(race).upper()  # force upper case

    if "AMERICAN INDIAN" in race or "ALASKA" in race or "NATIVE AMERICAN" in race:
        return "NATIVE AMERICAN / ALASKAN NATIVE"

    if "AFRICAN" in race or "BLACK" in race:
        return "BLACK / AFRICAN AMERICAN"

    if "CAUCASIAN" in race or "WHITE" in race:
        return "WHITE AMERICAN / CAUCASIAN"

    if "HAWAIIAN" in race or "PACIFIC" in race:
        return "NATIVE HAWAIIAN / OTHER PACIFIC ISLANDER"

    if "HISPANIC" in race:
        return "HISPANIC"

    # If unclassified, return unchanged
    return race


def clean_UCPD_data(in_df):
    """
    This cleans the raw data returned from scrape_UCPD_data.
    Removes shifted rows, parses dates, and standardizes Gender and Race.
    """
    # We must drop rows containing "No [X] for [Y]"
    df = in_df[
        ~in_df["Date/Time"].str.contains("traffic stops|field interviews|no|No")
    ].reset_index(drop=True)

    # Standardizes gender capitalization
    df["Gender"] = df.Gender.str.upper()

    # Imposes 2000 census racial categoriees
    df["Race"] = df["Race"].apply(standardize_race)

    # REMOVE IF GENDER IN RACE COLUMN
    df[~df["Race"].isin(["MALE", "FEMALE"])]

    # Splits into Date, Time columns separately
    df["Date"] = df["Date/Time"].apply(lambda x: x.split(" ", 1)[0])
    df["Time"] = df["Date/Time"].apply(lambda x: x.split(" ", 1)[1])

    # Drop "Date/Time"
    df = df.drop(columns=["Date/Time"])
    return df


if __name__ == "__main__":

    # Cleaning Field Interview Data
    field_interview_df = pd.read_csv("../data/field_interview_df.csv")
    field_interview_df_cleaned = clean_UCPD_data(field_interview_df)
    field_interview_df_cleaned.to_csv(
        "../data/field_interview_df_cleaned.csv", index=False
    )

    # Cleaning Traffic Stop Data
    traffic_df = pd.read_csv("../data/traffic_df.csv")
    traffic_df_cleaned = clean_UCPD_data(traffic_df)
    traffic_df_cleaned.to_csv("../data/traffic_df_cleaned.csv", index=False)
