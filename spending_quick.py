# First swipe at categorical analysis for this september. I know I missed at least a few cash things but whachagonnado?

#%%
# To activate the virtual environment, Ctrl+Shft+P 'Python:Select Interpreter'
# A heros's job is to risk his life to turn lip serviece into reality
# remember where you came from
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
# module is a file containing Python definitions and statements.
# In this case, data_cleaners is the module
#%%
# Import local modules
from helper_functions.data_cleaners import apply_cat_labels
from os import *
print(getcwd())
# Important to recognize that this would also work
# from helper_functions import data_cleaners
# But if I did that, the functions from data_cleaners would not be loaded into
# the global environment, so I'd have to access them through data_cleaners.whatever()
# This occurs because data_cleaners is a module, when a module
# is loaded, you can access its elements using _module_name.element

#%%
# Read in Data
# I had to specify the encoding in response to an error regarding a diacritic mark
df = pd.read_csv('..\Data\Spending2017.csv', encoding  = "ISO-8859-1")

# Print the first 5 rows of the data set
print(df.head())

#%%
# Print the variable types
print("Before Transformation: \n", df.dtypes)

# Change the date variable to datetime for sorting and filtering and whatnot
df["Date"] = pd.to_datetime(df["Date"])

df["SpendCategory"] = apply_cat_labels(df["Category"])

print("After Transformation: \n", df.dtypes)

# I read in the Python for Data Science book today that for production code
# you should always use the .loc and iloc functions in production code. 
# Even though numpy type indexing may be easier for inspecting 
# things quickly.

#%%
# Remove months that aren't in current month

# This is extra stupid, but to get the floor with a datetime, you must convert 
# to a period
# first_of_month = pd.to_datetime('today').to_period('M').to_timestamp()
first_of_month = pd.to_datetime('today').to_period('M').to_timestamp()

# Remember loc is for booleans involving the columns of the
# data frame and iloc is for indeces
current_df = df.loc[df["Date"] >= first_of_month]

current_total = current_df["Cost"].sum()

print(f"You spent ${current_total:.2f} in the month of {first_of_month}")

#%%
# Bar chart of categories

# This grouped each row of the data frame then took the sum of the cost variable
cost_table = current_df.groupby(["Category"])["Cost"].sum()

fig, ax = plt.subplots(1,2)

# This is a built in plotting function for a bar chart. I didn't use the
cost_table.plot.barh(ax = ax[0])

# I used a module to get the function apply_cat_labels
# current_df["SpendCategory"] = apply_cat_labels(current_df.loc[:, "Category"])

cost_table = current_df.groupby(["SpendCategory"])["Cost"].sum()

# Remember, using matplotlibs subplots function, you indicate the overall figure
# and the grid of axes. 
cost_table.plot.barh(ax = ax[1])

# Okay, so clearly there are categories missing here, I will
# Write a separate function to fill them out

#%%
# Applying multiple aggregation functions can be done using .agg

cost_table = current_df.groupby(["SpendCategory"]).agg({'Cost': ['count', 'sum', 'mean', 'min', 'max']})

print("Cost Table:\n", cost_table)

#%%
# Okay, so now I am going to skim through the time series chapter to better
# understand what is going on on a monthly basis.

# Looks like this may be easy. the datetime type should have an associated
# bound function called .month()

print(current_df.columns)

df_timeseries = df.set_index(df["Date"].values)

df_ts_grouped = df_timeseries.groupby([pd.Grouper(freq='M'), "SpendCategory"])

df_ts_grouped.sum().head()

agg_costs = df_ts_grouped.sum()

print(agg_costs)
# agg_costs.loc(agg_costs["Date"] == 2022)
#%%
# Stacked Bar chart
# To get this to run in iPython vscode I had to install both plotly and nbformat from the ipython terminal

fig = px.bar(agg_costs.reset_index(), x = "level_0", y = "Cost", color = "SpendCategory")

fig.show()