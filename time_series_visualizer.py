import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates = ["date"], index_col=0)
month_dict = {'Jan':1,'Feb':2,'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}
month_dict_full_month = {'January':1,'February':2,'March':3, 'April':4, 'May':5, 'June':6, 'July':7, 'August':8, 'September':9, 'October':10, 'November':11, 'December':12}

# Clean data
df = df.loc[~((df.value <= df.value.quantile(q = 0.025)) | (df.value >= df.value.quantile(q = 0.975)))]


def draw_line_plot():
    # Draw line plot
  fig, ax = plt.subplots(figsize=(15,8))
  sns.lineplot(x=df.index ,y = df.value)
  ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
  ax.set_xlabel('Date')
  ax.set_ylabel('Page Views')
  # Save image and return fig (don't change this part)
  fig.savefig('line_plot.png')
  return fig

def draw_bar_plot():
  # Copy and modify data for monthly bar plot
  df_bar = df
  df_bar['year'] = df_bar.index.strftime('%Y')
  df_bar['month'] = df_bar.index.strftime('%B')
  df_bar = df_bar.groupby(['year','month']).mean()
  df_bar.reset_index(inplace=True)

  # Draw bar plot
  fig,ax = plt.subplots(figsize = (15,8))
  sns.barplot(data = df_bar, x= 'year', y = 'value', hue=df_bar.month , hue_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])
  ax.set_ylabel("Average Page Views")
  ax.set_xlabel('Years')
  ax.tick_params(axis='x', rotation=90)

  # Save image and return fig (don't change this part)
  fig.savefig('bar_plot.png')
  return fig

def draw_box_plot():
  # Prepare data for box plots (this part is done!)
  df_box = df.copy()
  df_box.reset_index(inplace=True)
  df_box['year'] = [d.year for d in df_box.date]
  df_box['month'] = [d.strftime('%b') for d in df_box.date]

  # Draw box plots (using Seaborn)
  fig, ax = plt.subplots(1,2,figsize = (15,7))
  sns.boxplot(data = df_box, x = 'year' , y='value', ax=ax[0])
  sns.boxplot(data = df_box.sort_values('month', key = lambda x : x.apply (lambda x : month_dict[x])), x = 'month' , y='value',ax=ax[1])
  for axe in ax:
      axe.set_ylabel('Page Views')
  ax[0].set_title('Year-wise Box Plot (Trend)')
  ax[0].set_xlabel('Year')
  ax[1].set_title('Month-wise Box Plot (Seasonality)')
  ax[1].set_xlabel('Month')
  # Save image and return fig (don't change this part)
  fig.savefig('box_plot.png')
  return fig
