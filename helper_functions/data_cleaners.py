import pandas as pd

def apply_cat_labels(x_Series):
    all_categories = ["Alcohol",
                        "Books",
                        "Career",
                        "Eating Out",
                        "Fun",
                        "Gas",
                        "Gift",
                        "Goods_Other",
                        "Grocery",
                        "Health",
                        "Health_Other",
                        "Home",
                        "Loans",
                        "Media",
                        "Media_Monthly",
                        "Other",
                        "Phone",
                        "Power",
                        "Rent",
                        "Savings",
                        "Snack",
                        "Style",
                        "Transportation",
                        "Travel",
                        "Utilities"]

    return pd.Categorical(x_Series, all_categories)