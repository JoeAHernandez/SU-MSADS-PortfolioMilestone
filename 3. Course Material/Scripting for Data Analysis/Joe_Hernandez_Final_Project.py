#Load pandas, numpy, and statistics libraries
import pandas as pd
import numpy as np
import statistics
import plotly
import datetime
import time
import matplotlib
import plotly.io
plotly.tools.set_credentials_file(username='jahern01', api_key='SfQQtQr3iTfxVWEc1CC5')
#Read data from file
poop = pd.read_csv("C:\\Users\\l2pdwjah\\Desktop\\Professional Development\\Syracuse University\\IST652\\311_Cases.csv")
#Index Row Id
poop.set_index('CaseID', inplace = True)

#Build subset dataframe
hmnwst_df = poop[['Opened', 'Closed', 'Updated', 'Status Notes', 'Request Details','Street', 'Neighborhood',  'Latitude',  'Longitude', 'Source', 'Media URL']]
hmnwst_df.columns = hmnwst_df.columns.str.replace(' ', '_')
print(len(hmnwst_df))

#Slim down to only comepleted Human Waste reports and removal of duplicates
is_hw = hmnwst_df['Request_Details'] == 'Human Waste'
hmnwst = hmnwst_df[is_hw]
print(len(hmnwst))
hmnwst = hmnwst.dropna(subset=['Closed'])
print(len(hmnwst))

#Size of Human Waste only report (Remove comment markings to execute)
writer = pd.ExcelWriter('Human_Waste_Rpt.xlsx')
hmnwst.to_excel(writer, 'Sheet1')
writer.save()


#Prepare visual of human waste plot (All of San Francisco)
import plotly.plotly as py
from plotly.offline import plot
import plotly.graph_objs as go

mapbox_access_token = 'pk.eyJ1IjoiamFoZXJuMDEiLCJhIjoiY2p3Z2hrd3J1MW5lZzQ5bnUydHc0N2xmOSJ9.llgUrbXd8sLHdzE9bzIpug'

data = [
    go.Scattermapbox(
        lat=hmnwst.Latitude,
        lon=hmnwst.Longitude,
        mode='markers',
        marker=go.scattermapbox.Marker(size=5, color='rgb(122, 89, 1)', opacity=0.7),
        text = hmnwst.Media_URL,
    )
]

layout = go.Layout(
    autosize=True,
    hovermode='closest',
    mapbox=go.layout.Mapbox(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=go.layout.mapbox.Center(
            lat=round(statistics.median(hmnwst['Latitude'].unique()), 2),
            lon=round(statistics.median(hmnwst['Longitude'].unique()), 2)
        ),
        pitch=0,
        zoom=10
    ),
)

fig = go.Figure(data=data, layout=layout)
fig['layout']['title'] = "Human Waste Report 2008 - 2019"
#File uploaded to personal plotly account https://plot.ly/~jahern01
SFmapplot_url = plot(fig, filename='San Francisco Poop')
SFmapplot_url 





#Question 1: What times of the day have the highest frequency of reporting, least frequency?
#Convert Opened, Closed, and Updated Columns to datetime format
hmnwst1 = hmnwst
hmnwst1['Opened'] = pd.to_datetime(hmnwst1['Opened'])
hmnwst1['Closed'] = pd.to_datetime(hmnwst1['Closed'])

#Display map based on time of day
#Range for time of day will be hours
#Add column for time of day ranging (Morning: 0500 - 1159, Afternoon: 1200 - 1659, Evening: 1700 - 2359, Night: 2300 - 0459)
#Consider binning or subsetting by time of day
ToD = hmnwst1
ToD['Updated'] = ToD['Opened'].dt.hour

ToDMrn = ToD.loc[(ToD['Updated'] >= 5) & (ToD['Updated'] < 12)]
ToDAfr = ToD.loc[(ToD['Updated'] >= 12) & (ToD['Updated'] < 17)]
ToDEvn = ToD.loc[(ToD['Updated'] >= 17) & (ToD['Updated'] < 24)]
ToDNgt = ToD.loc[ToD['Updated'] < 5]
print(len(ToDMrn), 'Total Morning Reports:', round(len(ToDMrn)/len(ToD)*100, 2), '%')
print(len(ToDAfr), 'Total Afternoon Reports:', round(len(ToDAfr)/len(ToD)*100, 2), '%')
print(len(ToDEvn), 'Total Evening Reports:', round(len(ToDEvn)/len(ToD)*100, 2), '%')
print(len(ToDNgt), 'Total Night Reports:', round(len(ToDNgt)/len(ToD)*100, 2), '%')

#Prepare visual of human waste plot (All of San Francisco Morning)
data = [
    go.Scattermapbox(
        lat=ToDMrn.Latitude,
        lon=ToDMrn.Longitude,
        mode='markers',
        marker=go.scattermapbox.Marker(size=5, color='rgb(252, 209, 77)', opacity=0.7),
        text = ToDMrn.Media_URL,
    )
]

layout = go.Layout(
    autosize=True,
    hovermode='closest',
    mapbox=go.layout.Mapbox(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=go.layout.mapbox.Center(
            lat=round(statistics.median(ToDMrn['Latitude'].unique()), 2),
            lon=round(statistics.median(ToDMrn['Longitude'].unique()), 2)
        ),
        pitch=0,
        zoom=10
    ),
)

fig = go.Figure(data=data, layout=layout)
fig['layout']['title'] = "Morning Human Waste Report 2008 - 2019"
#File uploaded to personal plotly account https://plot.ly/~jahern01
SFMrnmapplot_url = plot(fig, filename='San Francisco Morning Poop')
SFMrnmapplot_url


#Prepare visual of human waste plot (All of San Francisco Afternoon)
data = [
    go.Scattermapbox(
        lat=ToDAfr.Latitude,
        lon=ToDAfr.Longitude,
        mode='markers',
        marker=go.scattermapbox.Marker(size=5, color='rgb(78, 172, 217)', opacity=0.7),
        text = ToDAfr.Media_URL,
    )
]

layout = go.Layout(
    autosize=True,
    hovermode='closest',
    mapbox=go.layout.Mapbox(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=go.layout.mapbox.Center(
            lat=round(statistics.median(ToDAfr['Latitude'].unique()), 2),
            lon=round(statistics.median(ToDAfr['Longitude'].unique()), 2)
        ),
        pitch=0,
        zoom=10
    ),
)

fig = go.Figure(data=data, layout=layout)
fig['layout']['title'] = "Afternoon Human Waste Report 2008 - 2019"
#File uploaded to personal plotly account https://plot.ly/~jahern01
SFAfrmapplot_url = plot(fig, filename='San Francisco Afternoon Poop')
SFAfrmapplot_url

#Prepare visual of human waste plot (All of San Francisco Evening)
data = [
    go.Scattermapbox(
        lat=ToDEvn.Latitude,
        lon=ToDEvn.Longitude,
        mode='markers',
        marker=go.scattermapbox.Marker(size=5, color='rgb(220, 109, 32)', opacity=0.7),
        text = ToDEvn.Media_URL,
    )
]

layout = go.Layout(
    autosize=True,
    hovermode='closest',
    mapbox=go.layout.Mapbox(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=go.layout.mapbox.Center(
            lat=round(statistics.median(ToDEvn['Latitude'].unique()), 2),
            lon=round(statistics.median(ToDEvn['Longitude'].unique()), 2)
        ),
        pitch=0,
        zoom=10
    ),
)

fig = go.Figure(data=data, layout=layout)
fig['layout']['title'] = "Evening Human Waste Report 2008 - 2019"
#File uploaded to personal plotly account https://plot.ly/~jahern01
SFEvnmapplot_url = plot(fig, filename='San Francisco Evening Poop')
SFEvnmapplot_url


#Prepare visual of human waste plot (All of San Francisco Night)
data = [
    go.Scattermapbox(
        lat=ToDNgt.Latitude,
        lon=ToDNgt.Longitude,
        mode='markers',
        marker=go.scattermapbox.Marker(size=5, color='rgb(19, 24, 98)', opacity=0.7),
        text = ToDNgt.Media_URL,
    )
]

layout = go.Layout(
    autosize=True,
    hovermode='closest',
    mapbox=go.layout.Mapbox(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=go.layout.mapbox.Center(
            lat=round(statistics.median(ToDNgt['Latitude'].unique()), 2),
            lon=round(statistics.median(ToDNgt['Longitude'].unique()), 2)
        ),
        pitch=0,
        zoom=10
    ),
)

fig = go.Figure(data=data, layout=layout)
fig['layout']['title'] = "Night Human Waste Report 2008 - 2019"
#File uploaded to personal plotly account https://plot.ly/~jahern01
SFNgtmapplot_url = plot(fig, filename='San Francisco Night Poop')
SFNgtmapplot_url




#Question 2: How much waste is in each neighborhood and street location?
#Neighborhood
Nbr_tb = pd.pivot_table(hmnwst, index=["Neighborhood"], values=["Updated"], aggfunc=len, fill_value=0)
result1 = Nbr_tb.sort_values(('Updated'), ascending=False)
#Build bar plot x as neighborhoods and y as frequency
#Build dataframe in long format of top 5 neighborhoods
import matplotlib.pyplot as plt
Nbr_tp5 = pd.DataFrame(result1.head(5))

#Bar chart Grouped
#From pivot table subset by Neighborhood for x Streets and y will be Updated
trace0 = go.Bar(
  x=['Tenderloin'],
  y=[Nbr_tp5.ix['Tenderloin'].Updated],
  name='Tenderloin'
)

trace1 = go.Bar(
  x=['Mission'],
  y=[Nbr_tp5.ix['Mission'].Updated],
  name='Mission'
)

trace2 = go.Bar(
  x=['South of Market'],
  y=[Nbr_tp5.ix['South of Market'].Updated],
  name='South of Market'
)

trace3 = go.Bar(
  x=['Civic Center'],
  y=[Nbr_tp5.ix['Civic Center'].Updated],
  name='Civic Center'
)

trace4 = go.Bar(
  x=['Mission Dolores'],
  y=[Nbr_tp5.ix['Mission Dolores'].Updated],
  name='Mission Dolores'
)

data = [trace0, trace1, trace2, trace3, trace4]

layout = {
  'xaxis': {'title': 'Neighborhood'},
  'yaxis': {'title': '# of Reports'},
  'title': 'Top 5 Neighborhoods: Human Waste Reports'
}

fig = go.Figure(data = data, layout = layout)

plot(fig, filename='San Francisco Neighborhood Poop')


#Save to excel sheet for complete list
writer = pd.ExcelWriter('Neighbor.xlsx')
Nbr_tp5.to_excel(writer, 'Sheet1')
writer.save()

#Street within neighborhood
NbrSt_tb = pd.pivot_table(hmnwst, index=["Neighborhood","Street"], values=["Updated"], aggfunc=len, fill_value=0)
result2 = NbrSt_tb.sort_values(('Updated'), ascending=False)
#Build bar plot x as neighborhoods and y as frequency
#Build dataframe in long format of top 5 neighborhoods
import matplotlib.pyplot as plt
NbrSt_tp25 = pd.DataFrame(result2.head(25))

#Bar chart Grouped
#From pivot table subset by Neighborhood for x Streets and y will be Updated
trace0 = go.Bar(
  x=NbrSt_tp25.ix['Tenderloin'].index,
  y=NbrSt_tp25.ix['Tenderloin'].Updated,
  name='Tenderloin'
)

trace1 = go.Bar(
  x=NbrSt_tp25.ix['Mission'].index,
  y=NbrSt_tp25.ix['Mission'].Updated,
  name='Mission'
)

trace2 = go.Bar(
  x=NbrSt_tp25.ix['South of Market'].index,
  y=NbrSt_tp25.ix['South of Market'].Updated,
  name='South of Market'
)

trace3 = go.Bar(
  x=NbrSt_tp25.ix['Civic Center'].index,
  y=NbrSt_tp25.ix['Civic Center'].Updated,
  name='Civic Center'
)

data = [trace0, trace1, trace2, trace3]

layout = layout = {
  'xaxis': {'title': 'Street'},
  'yaxis': {'title': '# of Reports'},
  'title': 'Top 25 Streets: Human Waste Reports'
}

fig = go.Figure(data = data, layout = layout)

plot(fig, filename='San Francisco Street Poop')


#Save to excel sheet for complete list
writer = pd.ExcelWriter('Neighbor_Street.xlsx')
NbrSt_tp25.to_excel(writer, 'Sheet2')
writer.save()





#Question 3: What is the duration of the resolution to these reports? Is resolution declining?
#Subset the data by binning in Month/Year format
#Build a box and whisker plot to show duration of cases per month for each year
#Create new dataframe to measure time delta
hmnwst2 = hmnwst
hmnwst2['Opened'] = pd.to_datetime(hmnwst2['Opened'])
hmnwst2['Closed'] = pd.to_datetime(hmnwst2['Closed'])
hmnwst2['Updated'] = hmnwst2.Closed - hmnwst2.Opened
hmnwst2['Updated'] = hmnwst2['Updated'] / np.timedelta64(1, 'm')
hmnwst2 = pd.DataFrame(hmnwst2)

#Subset dataframe by complete year (2009 - 2018)
hmnwst2009 = hmnwst2.loc[hmnwst2['Opened'].dt.year == 2009]
hmnwst2010 = hmnwst2.loc[hmnwst2['Opened'].dt.year == 2010]
hmnwst2011 = hmnwst2.loc[hmnwst2['Opened'].dt.year == 2011]
hmnwst2012 = hmnwst2.loc[hmnwst2['Opened'].dt.year == 2012]
hmnwst2013 = hmnwst2.loc[hmnwst2['Opened'].dt.year == 2013]
hmnwst2014 = hmnwst2.loc[hmnwst2['Opened'].dt.year == 2014]
hmnwst2015 = hmnwst2.loc[hmnwst2['Opened'].dt.year == 2015]
hmnwst2016 = hmnwst2.loc[hmnwst2['Opened'].dt.year == 2016]
hmnwst2017 = hmnwst2.loc[hmnwst2['Opened'].dt.year == 2017]
hmnwst2018 = hmnwst2.loc[hmnwst2['Opened'].dt.year == 2018]

#Get descriptive statistics for each year
#Remove Scientific Notation in results
pd.set_option('display.float_format', lambda x: '%.3f' % x)
#Create dataframe of each descriptive statistic result
hmnwst2.Updated.describe()
hmnwstdf2009 = pd.DataFrame(hmnwst2009.Updated.describe())
hmnwstdf2010 = pd.DataFrame(hmnwst2010.Updated.describe())
hmnwstdf2011 = pd.DataFrame(hmnwst2011.Updated.describe())
hmnwstdf2012 = pd.DataFrame(hmnwst2012.Updated.describe())
hmnwstdf2013 = pd.DataFrame(hmnwst2013.Updated.describe())
hmnwstdf2014 = pd.DataFrame(hmnwst2014.Updated.describe())
hmnwstdf2015 = pd.DataFrame(hmnwst2015.Updated.describe())
hmnwstdf2016 = pd.DataFrame(hmnwst2016.Updated.describe())
hmnwstdf2017 = pd.DataFrame(hmnwst2017.Updated.describe())
hmnwstdf2018 = pd.DataFrame(hmnwst2018.Updated.describe())
#Merge dataframes to one
hmnwstdfyrs = pd.DataFrame(hmnwstdf2009.merge(hmnwstdf2010, left_index=True, right_index=True).merge(hmnwstdf2011, left_index=True, right_index=True).merge(hmnwstdf2012, left_index=True, right_index=True).merge(hmnwstdf2013, left_index=True, right_index=True).merge(hmnwstdf2014, left_index=True, right_index=True).merge(hmnwstdf2015, left_index=True, right_index=True).merge(hmnwstdf2016, left_index=True, right_index=True).merge(hmnwstdf2017, left_index=True, right_index=True).merge(hmnwstdf2018, left_index=True, right_index=True))
hmnwstdfyrs.columns = ['2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018']
print(hmnwstdfyrs)

#Save to excel sheet for complete list
writer = pd.ExcelWriter('Des_Stat_Years.xlsx')
hmnwstdfyrs.to_excel(writer, 'Sheet1')
writer.save()

#Create a boxplot for each year by every month measuring the duration
#Human waste for 2009
#Get duration for each month
Jan = hmnwst2009['Updated'].loc[hmnwst2009['Opened'].dt.month == 1]
Feb = hmnwst2009['Updated'].loc[hmnwst2009['Opened'].dt.month == 2]
Mar = hmnwst2009['Updated'].loc[hmnwst2009['Opened'].dt.month == 3]
Apr = hmnwst2009['Updated'].loc[hmnwst2009['Opened'].dt.month == 4]
May = hmnwst2009['Updated'].loc[hmnwst2009['Opened'].dt.month == 5]
Jun = hmnwst2009['Updated'].loc[hmnwst2009['Opened'].dt.month == 6]
Jul = hmnwst2009['Updated'].loc[hmnwst2009['Opened'].dt.month == 7]
Aug = hmnwst2009['Updated'].loc[hmnwst2009['Opened'].dt.month == 8]
Sep = hmnwst2009['Updated'].loc[hmnwst2009['Opened'].dt.month == 9]
Oct = hmnwst2009['Updated'].loc[hmnwst2009['Opened'].dt.month == 10]
Nov = hmnwst2009['Updated'].loc[hmnwst2009['Opened'].dt.month == 11]
Dec = hmnwst2009['Updated'].loc[hmnwst2009['Opened'].dt.month == 12]

#Create boxplot by month
January = go.Box(
    y=Jan,
    name = 'January',
    boxpoints = False,
    marker = dict(
        color = 'rgb(132, 165, 184)',
    )
)
February = go.Box(
    y=Feb,
    name = 'February',
    boxpoints = False,
    marker = dict(
        color = 'rgb(66, 104, 124)',
    )
)
March = go.Box(
    y=Mar,
    name = 'March',
    boxpoints = False,
    marker = dict(
        color = 'rgb(180, 249, 165)',
    )
)
April = go.Box(
    y=Apr,
    name = 'April',
    boxpoints = False,
    marker = dict(
        color = 'rgb(158, 231, 245)',
    )
)
May = go.Box(
    y=May,
    name = 'May',
    boxpoints = False,
    marker = dict(
        color = 'rgb(243, 168, 188)',
    )
)
June = go.Box(
    y=Jun,
    name = 'June',
    boxpoints = False,
    marker = dict(
        color = 'rgb(21, 178, 211)',
    )
)
July = go.Box(
    y=Jul,
    name = 'July',
    boxpoints = False,
    marker = dict(
        color = 'rgb(255, 215, 0)',
    )
)
August = go.Box(
    y=Aug,
    name = 'August',
    boxpoints = False,
    marker = dict(
        color = 'rgb(243, 135, 47)',
    )
)
September = go.Box(
    y=Sep,
    name = 'September',
    boxpoints = False,
    marker = dict(
        color = 'rgb(156, 39, 6)',
    )
)
October = go.Box(
    y=Oct,
    name = 'October',
    boxpoints = False,
    marker = dict(
        color = 'rgb(212, 91, 18)',
    )
)
November = go.Box(
    y=Nov,
    name = 'November',
    boxpoints = False,
    marker = dict(
        color = 'rgb(95, 84, 38)',
    )
)
December = go.Box(
    y=Dec,
    name = 'December',
    boxpoints = False,
    marker = dict(
        color = 'rgb(179, 218, 241)',
    )
)
data = [January, February, March, April, May, June, July, August, September, October, November, December]
layout = go.Layout(
  title = "2009 Box Plot Response Duration",
  xaxis=dict(
    title='Months',
    zeroline=False
  ),
  yaxis=dict(
    title='Duration (in minutes)',
    zeroline=False
  )
)

fig = go.Figure(data = data, layout = layout)

plot(fig, filename='San Francisco Human Waste Response Duration 2009')

#Human waste for 2013
#Get duration for each month
Jan = hmnwst2013['Updated'].loc[hmnwst2013['Opened'].dt.month == 1]
Feb = hmnwst2013['Updated'].loc[hmnwst2013['Opened'].dt.month == 2]
Mar = hmnwst2013['Updated'].loc[hmnwst2013['Opened'].dt.month == 3]
Apr = hmnwst2013['Updated'].loc[hmnwst2013['Opened'].dt.month == 4]
May = hmnwst2013['Updated'].loc[hmnwst2013['Opened'].dt.month == 5]
Jun = hmnwst2013['Updated'].loc[hmnwst2013['Opened'].dt.month == 6]
Jul = hmnwst2013['Updated'].loc[hmnwst2013['Opened'].dt.month == 7]
Aug = hmnwst2013['Updated'].loc[hmnwst2013['Opened'].dt.month == 8]
Sep = hmnwst2013['Updated'].loc[hmnwst2013['Opened'].dt.month == 9]
Oct = hmnwst2013['Updated'].loc[hmnwst2013['Opened'].dt.month == 10]
Nov = hmnwst2013['Updated'].loc[hmnwst2013['Opened'].dt.month == 11]
Dec = hmnwst2013['Updated'].loc[hmnwst2013['Opened'].dt.month == 12]

#Create boxplot by month
January = go.Box(
    y=Jan,
    name = 'January',
    boxpoints = False,
    marker = dict(
        color = 'rgb(132, 165, 184)',
    )
)
February = go.Box(
    y=Feb,
    name = 'February',
    boxpoints = False,
    marker = dict(
        color = 'rgb(66, 104, 124)',
    )
)
March = go.Box(
    y=Mar,
    name = 'March',
    boxpoints = False,
    marker = dict(
        color = 'rgb(180, 249, 165)',
    )
)
April = go.Box(
    y=Apr,
    name = 'April',
    boxpoints = False,
    marker = dict(
        color = 'rgb(158, 231, 245)',
    )
)
May = go.Box(
    y=May,
    name = 'May',
    boxpoints = False,
    marker = dict(
        color = 'rgb(243, 168, 188)',
    )
)
June = go.Box(
    y=Jun,
    name = 'June',
    boxpoints = False,
    marker = dict(
        color = 'rgb(21, 178, 211)',
    )
)
July = go.Box(
    y=Jul,
    name = 'July',
    boxpoints = False,
    marker = dict(
        color = 'rgb(255, 215, 0)',
    )
)
August = go.Box(
    y=Aug,
    name = 'August',
    boxpoints = False,
    marker = dict(
        color = 'rgb(243, 135, 47)',
    )
)
September = go.Box(
    y=Sep,
    name = 'September',
    boxpoints = False,
    marker = dict(
        color = 'rgb(156, 39, 6)',
    )
)
October = go.Box(
    y=Oct,
    name = 'October',
    boxpoints = False,
    marker = dict(
        color = 'rgb(212, 91, 18)',
    )
)
November = go.Box(
    y=Nov,
    name = 'November',
    boxpoints = False,
    marker = dict(
        color = 'rgb(95, 84, 38)',
    )
)
December = go.Box(
    y=Dec,
    name = 'December',
    boxpoints = False,
    marker = dict(
        color = 'rgb(179, 218, 241)',
    )
)
data = [January, February, March, April, May, June, July, August, September, October, November, December]
layout = go.Layout(
  title = "2013 Box Plot Response Duration",
  xaxis=dict(
    title='Months',
    zeroline=False
  ),
  yaxis=dict(
    title='Duration (in minutes)',
    zeroline=False
  )
)

fig = go.Figure(data = data, layout = layout)

plot(fig, filename='San Francisco Human Waste Response Duration 2013')

#Human waste for 2018
#Get duration for each month
Jan = hmnwst2018['Updated'].loc[hmnwst2018['Opened'].dt.month == 1]
Feb = hmnwst2018['Updated'].loc[hmnwst2018['Opened'].dt.month == 2]
Mar = hmnwst2018['Updated'].loc[hmnwst2018['Opened'].dt.month == 3]
Apr = hmnwst2018['Updated'].loc[hmnwst2018['Opened'].dt.month == 4]
May = hmnwst2018['Updated'].loc[hmnwst2018['Opened'].dt.month == 5]
Jun = hmnwst2018['Updated'].loc[hmnwst2018['Opened'].dt.month == 6]
Jul = hmnwst2018['Updated'].loc[hmnwst2018['Opened'].dt.month == 7]
Aug = hmnwst2018['Updated'].loc[hmnwst2018['Opened'].dt.month == 8]
Sep = hmnwst2018['Updated'].loc[hmnwst2018['Opened'].dt.month == 9]
Oct = hmnwst2018['Updated'].loc[hmnwst2018['Opened'].dt.month == 10]
Nov = hmnwst2018['Updated'].loc[hmnwst2018['Opened'].dt.month == 11]
Dec = hmnwst2018['Updated'].loc[hmnwst2018['Opened'].dt.month == 12]

#Create boxplot by month
January = go.Box(
    y=Jan,
    name = 'January',
    boxpoints = False,
    marker = dict(
        color = 'rgb(132, 165, 184)',
    )
)
February = go.Box(
    y=Feb,
    name = 'February',
    boxpoints = False,
    marker = dict(
        color = 'rgb(66, 104, 124)',
    )
)
March = go.Box(
    y=Mar,
    name = 'March',
    boxpoints = False,
    marker = dict(
        color = 'rgb(180, 249, 165)',
    )
)
April = go.Box(
    y=Apr,
    name = 'April',
    boxpoints = False,
    marker = dict(
        color = 'rgb(158, 231, 245)',
    )
)
May = go.Box(
    y=May,
    name = 'May',
    boxpoints = False,
    marker = dict(
        color = 'rgb(243, 168, 188)',
    )
)
June = go.Box(
    y=Jun,
    name = 'June',
    boxpoints = False,
    marker = dict(
        color = 'rgb(21, 178, 211)',
    )
)
July = go.Box(
    y=Jul,
    name = 'July',
    boxpoints = False,
    marker = dict(
        color = 'rgb(255, 215, 0)',
    )
)
August = go.Box(
    y=Aug,
    name = 'August',
    boxpoints = False,
    marker = dict(
        color = 'rgb(243, 135, 47)',
    )
)
September = go.Box(
    y=Sep,
    name = 'September',
    boxpoints = False,
    marker = dict(
        color = 'rgb(156, 39, 6)',
    )
)
October = go.Box(
    y=Oct,
    name = 'October',
    boxpoints = False,
    marker = dict(
        color = 'rgb(212, 91, 18)',
    )
)
November = go.Box(
    y=Nov,
    name = 'November',
    boxpoints = False,
    marker = dict(
        color = 'rgb(95, 84, 38)',
    )
)
December = go.Box(
    y=Dec,
    name = 'December',
    boxpoints = False,
    marker = dict(
        color = 'rgb(179, 218, 241)',
    )
)
data = [January, February, March, April, May, June, July, August, September, October, November, December]
layout = go.Layout(
  title = "2018 Box Plot Response Duration",
  xaxis=dict(
    title='Months',
    zeroline=False
  ),
  yaxis=dict(
    title='Duration (in minutes)',
    zeroline=False
  )
)

fig = go.Figure(data = data, layout = layout)

plot(fig, filename='San Francisco Human Waste Response Duration 2018')




#Question 4: Has there been a transition in the source of reporting human waste covered by the data?
#Create a time series line graph over time to show different mediums of reporting
#Subset by Source and collect by daily reports

#Source and Date(Opened) Pivot Table
from datetime import datetime
hmnwst3 = hmnwst
hmnwst3['Opened'] = hmnwst3['Opened'].dt.date
SrcDt_tb = pd.pivot_table(hmnwst3, index=["Source","Opened"], values=["Updated"], aggfunc=len, fill_value=0)

#Save to excel sheet for complete list
writer = pd.ExcelWriter('Source_Rpt.xlsx')
SrcDt_tb.to_excel(writer, 'Sheet1')
writer.save()

#Grouped Time Series graph
trace0 = go.Scatter(
  x=SrcDt_tb.ix['Twitter'].index,
  y=SrcDt_tb.ix['Twitter'].Updated,
  name = "Twitter",
  line = dict(color = '#1DA1F2'),
  opacity = 0.8)

trace1 = go.Scatter(
  x=SrcDt_tb.ix['Phone'].index,
  y=SrcDt_tb.ix['Phone'].Updated,
  name = "Phone",
  line = dict(color = '#000000'),
  opacity = 0.8)
  
trace2 = go.Scatter(
  x=SrcDt_tb.ix['Mobile/Open311'].index,
  y=SrcDt_tb.ix['Mobile/Open311'].Updated,
  name = "Mobile/Open311",
  line = dict(color = '#808080'),
  opacity = 0.8)

trace3 = go.Scatter(
  x=SrcDt_tb.ix['Web'].index,
  y=SrcDt_tb.ix['Web'].Updated,
  name = "Web",
  line = dict(color = '#FF8C00'),
  opacity = 0.8)

trace4 = go.Scatter(
  x=SrcDt_tb.ix['Other Department'].index,
  y=SrcDt_tb.ix['Other Department'].Updated,
  name = "Other Department",
  line = dict(color = '#228B22'),
  opacity = 0.8)

trace5 = go.Scatter(
  x=SrcDt_tb.ix['Integrated Agency'].index,
  y=SrcDt_tb.ix['Integrated Agency'].Updated,
  name = "Integrated Agency",
  line = dict(color = '#FFD700'),
  opacity = 0.8)

data = [trace0, trace1, trace2, trace3, trace4, trace5]

layout = dict(
    title = "Reporting Trend By Source",
)

fig = dict(data=data, layout=layout)
SrcTS_url = plot(fig, filename = "Reporting Trend By Source")
SrcTS_url


#Get Cumulative reports
SrcDt_tb1 = SrcDt_tb
SrcDt_tb1['Updated'] = SrcDt_tb1.groupby(level=0, as_index=False).cumsum()

#Save to excel sheet for complete list
writer = pd.ExcelWriter('Cum_Source_Rpt.xlsx')
SrcDt_tb1.to_excel(writer, 'Sheet1')
writer.save()

#Grouped Time Series graph
trace0 = go.Scatter(
  x=SrcDt_tb1.ix['Twitter'].index,
  y=SrcDt_tb1.ix['Twitter'].Updated,
  name = "Twitter",
  # fill='tozeroy',
  # fillcolor = '#1DA1F2',
  line = dict(color = '#1DA1F2'),
  opacity = 0.8)

trace1 = go.Scatter(
  x=SrcDt_tb1.ix['Phone'].index,
  y=SrcDt_tb1.ix['Phone'].Updated,
  name = "Phone",
  # fill='tozeroy',
  # fillcolor = '#000000',
  line = dict(color = '#000000'),
  opacity = 0.8)
  
trace2 = go.Scatter(
  x=SrcDt_tb1.ix['Mobile/Open311'].index,
  y=SrcDt_tb1.ix['Mobile/Open311'].Updated,
  name = "Mobile/Open311",
  # fill='tozeroy',
  # fillcolor = '#808080',
  line = dict(color = '#808080'),
  opacity = 0.8)

trace3 = go.Scatter(
  x=SrcDt_tb1.ix['Web'].index,
  y=SrcDt_tb1.ix['Web'].Updated,
  name = "Web",
  # fill='tozeroy',
  # fillcolor = '#FF8C00',
  line = dict(color = '#FF8C00'),
  opacity = 0.8)

trace4 = go.Scatter(
  x=SrcDt_tb1.ix['Other Department'].index,
  y=SrcDt_tb1.ix['Other Department'].Updated,
  name = "Other Department",
  # fill='tozeroy',
  # fillcolor = '#228B22',
  line = dict(color = '#228B22'),
  opacity = 0.8)

trace5 = go.Scatter(
  x=SrcDt_tb1.ix['Integrated Agency'].index,
  y=SrcDt_tb1.ix['Integrated Agency'].Updated,
  name = "Integrated Agency",
  # fill='tozeroy',
  # fillcolor = '#FFD700',
  line = dict(color = '#FFD700'),
  opacity = 0.8)

data = [trace0, trace1, trace2, trace3, trace4, trace5]

layout = dict(
    title = "Cumulative Reporting Trend By Source",
)

fig = dict(data=data, layout=layout)
SrcTScm_url = plot(fig, filename = "Cumulative Reporting Trend By Source")
SrcTScm_url
