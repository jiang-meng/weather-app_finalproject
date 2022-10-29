import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

plt.style.use('seaborn')

st.title('Overview of precipitation in Australia and its influencing factors')

primaryColor='#F63366'
backgroundColor='#FFFFFF'
secondaryBackgroundColor='#F0F2F6'
textColor='#262730'
font='sans serif'

df = pd.read_csv('weatherAUS_1.csv')
# see if there are null data
df.isnull().sum()
#delete null infomation
df.dropna(inplace=True)

def delete_outlier(dfs, i):
    zscore = i + '_z'
    dfs.zscore = (dfs[i] - dfs[i].mean())/dfs[i].std() 
    dfs = dfs[(dfs.zscore > -1.5) & (dfs.zscore < 1.5)]
    return(dfs)

delete_outlier(df, 'Rainfall')
delete_outlier(df, 'MinTemp')
delete_outlier(df, 'MaxTemp')
delete_outlier(df, 'Evaporation')
delete_outlier(df, 'Sunshine')
delete_outlier(df, 'WindGustSpeed')
delete_outlier(df, 'WindSpeed9am')
delete_outlier(df, 'WindSpeed3pm')
delete_outlier(df, 'Humidity9am')
delete_outlier(df, 'Humidity3pm')
delete_outlier(df, 'Pressure9am')
delete_outlier(df, 'Pressure3pm')
delete_outlier(df, 'Cloud9am')
delete_outlier(df, 'Cloud3pm')
delete_outlier(df, 'Temp9am')
delete_outlier(df, 'Temp3pm')

df = df.sample(50000, ignore_index=True)  # random sample 5000 rows

st.map(df)

# add two column to datetime format
#df = pd.read_csv('weather_5000.csv')
df['Date'] = pd.to_datetime(df['Date'])
df['year'] = df['Date'].dt.year
df['month'] = df['Date'].dt.month
df['day'] = df['Date'].dt.day

# Overview of Precipitation in Australia
st.markdown('## *Overview of Precipitation in Australia')

# rainfall in each year, month, day
df_year = df[['year', 'Rainfall','RainToday']].sort_values(by='year',ignore_index=True)
df_month = df[['month', 'Rainfall','RainToday']].sort_values(by='month',ignore_index=True)
df_day = df[['day', 'Rainfall','RainToday']].sort_values(by='day',ignore_index=True)

fig, ax = plt.subplots(1,2,figsize = (10,5))
df_year.groupby('year').mean()['Rainfall'].plot(ax=ax[0])
df_month.groupby('month').mean()['Rainfall'].plot.bar(ax=ax[1])
ax[0].set_xlabel('rainfall for different years')
ax[1].set_xlabel('rainfall for different months')
st.pyplot(fig)


affect = st.sidebar.radio(
    'Select an option to see how this factor relates to whether rain will fall tomorrow',
    ('min and max Temp', 'Rainfall', 'Evaporation', 'Sunshine','WindSpeed','Pressure','Cloud', 'Humidity','Winddirection'))

if affect == 'min and max Temp':
    fig, ax = plt.subplots(1, 2, figsize=(15,5))
    df[df.RainTomorrow=='Yes'].WindSpeed3pm.plot.box(ax=ax[0])
    ax[0].set_xlabel('Rain Tomorrow')
    ax[0].set_ylabel('Temperature') 
    df[df.RainTomorrow=='Yes'].MinTemp.plot.box(ax=ax[1])
    ax[1].set_xlabel('Rain Tomorrow')
    st.pyplot(fig)
    fig1, ax = plt.subplots()
    ax.scatter(df[df.RainTomorrow=='Yes']['MinTemp'],df[df.RainTomorrow=='Yes']['MaxTemp'],c='plum',alpha=0.3,label='Tomorrow Rain = Yes') 
    ax.scatter(df[df.RainTomorrow=='No']['MinTemp'],df[df.RainTomorrow=='No']['MaxTemp'],c='slategrey',alpha=0.3,label='Tomorrow Rain = No') 
    fig1.set_figheight(6)
    fig1.set_figwidth(10)
    plt.legend()
    st.pyplot(fig1)
elif affect == 'Rainfall':
    fig, ax = plt.subplots()
    df[df.RainTomorrow=='Yes'].Rainfall.plot.box(ax=ax)
    ax.set_xlabel('Rain Tomorrow')
    ax.set_ylabel('Rainfall Today')
    st.pyplot(fig) 
elif affect == 'Evaporation':
    fig, ax = plt.subplots()
    df[df.RainTomorrow=='Yes'].Evaporation.plot.box(ax=ax)
    ax.set_xlabel('Rain Tomorrow')
    ax.set_ylabel('Today\'s Evaporation')
    st.pyplot(fig)
elif affect == 'Sunshine':
    fig, ax = plt.subplots()
    df[df.RainTomorrow=='Yes'].Sunshine.plot.box(ax=ax)
    ax.set_xlabel('Rain Tomorrow')
    ax.set_ylabel('Today\'s Sunshine') 
    st.pyplot(fig)
elif affect == 'WindSpeed':
    fig, ax = plt.subplots()
    df[df.RainTomorrow=='Yes'].WindGustSpeed.plot.box(ax=ax)
    ax.set_xlabel('Rain Tomorrow')
    ax.set_ylabel('Today\'s WindGustSpeed')  
    st.pyplot(fig)
elif affect == 'Pressure':
    fig, ax = plt.subplots(1, 2, figsize=(15,5))
    df[df.RainTomorrow=='Yes'].Pressure9am.plot.box(ax=ax[0])
    ax[0].set_xlabel('Rain Tomorrow')
    ax[0].set_ylabel('Pressure9am') 
    df[df.RainTomorrow=='Yes'].Pressure3pm.plot.box(ax=ax[1])
    ax[1].set_xlabel('Pressure3pm')
    st.pyplot(fig)
    fig1, ax = plt.subplots()
    ax.scatter(df[df.RainTomorrow=='Yes']['Pressure9am'],df[df.RainTomorrow=='Yes']['Pressure3pm'],c='plum',alpha=1,label='Tomorrow Rain = Yes') 
    ax.scatter(df[df.RainTomorrow=='No']['Pressure9am'],df[df.RainTomorrow=='No']['Pressure3pm'],c='slategrey',alpha=1,label='Tomorrow Rain = No') 
    fig1.set_figheight(6)
    fig1.set_figwidth(10)
    plt.legend()
    st.pyplot(fig1)
elif affect == 'Cloud':
    fig, ax = plt.subplots(1, 2, figsize=(15,5))
    df[df.RainTomorrow=='Yes'].Cloud9am.plot.box(ax=ax[0])
    ax[0].set_xlabel('Rain Tomorrow')
    ax[0].set_ylabel('Cloud9am') 
    df[df.RainTomorrow=='Yes'].Cloud3pm.plot.box(ax=ax[1])
    ax[1].set_xlabel('Cloud3pm')
    st.pyplot(fig)
elif affect == 'Humidity':
    fig, ax = plt.subplots(1, 2, figsize=(15,5))
    df[df.RainTomorrow=='Yes'].Humidity9am.plot.box(ax=ax[0])
    ax[0].set_xlabel('Rain Tomorrow')
    ax[0].set_ylabel('Humidity9am') 
    df[df.RainTomorrow=='Yes'].Humidity3pm.plot.box(ax=ax[1])
    ax[1].set_xlabel('Humidity3pm')
    st.pyplot(fig)
    fig1, ax = plt.subplots()
    ax.scatter(df[df.RainTomorrow=='Yes']['Humidity9am'],df[df.RainTomorrow=='Yes']['Humidity3pm'],c='plum',alpha=1,label='Tomorrow Rain = Yes') 
    ax.scatter(df[df.RainTomorrow=='No']['Humidity9am'],df[df.RainTomorrow=='No']['Humidity3pm'],c='slategrey',alpha=1,label='Tomorrow Rain = No') 
    fig1.set_figheight(6)
    fig1.set_figwidth(10)
    plt.legend()
    st.pyplot(fig1)
elif affect == 'Winddirection':
    winddirect = df[(df.RainTomorrow=='Yes')&(df.WindGustDir)].groupby('WindGustDir')['RainTomorrow'].count()/len(df[df.RainTomorrow=='Yes'])
    windgustspeed = pd.DataFrame(winddirect)
    wind_direct_9am = (df[(df.RainTomorrow=='Yes')&(df.WindDir9am)].groupby('WindDir9am')['RainTomorrow'].count())/len(df[df.RainTomorrow=='Yes'])*100
    winddir9am = pd.DataFrame(wind_direct_9am)
    wind_direct_3pm = df[(df.RainTomorrow=='Yes')&(df.WindDir3pm)].groupby('WindDir3pm')['RainTomorrow'].count()
    winddir3pm = pd.DataFrame(wind_direct_3pm)
    options = st.multiselect(
        'Select the data you want to watch about wind direction and tomorrow\'s rain',
        ['windgustspeed', 'winddir9am', 'winddir3pm'],
        ['windgustspeed', 'winddir9am', 'winddir3pm'])
    if options == 'windgustspeed':
        st.write(windgustspeed)
    if options == 'winddir9am':
        st.write(winddir9am)
    if options == 'winddir3pm':
        st.write(winddir3pm)



# create a input form
form = st.sidebar.form('country_form')
country_filter = form.text_input('Enter the city where you want to search for precipitation information (enter ALL to reset)', 'ALL')
form.form_submit_button('Apply')
loca = df['Location']
df_info = df[['Location','Rainfall', 'RainToday','RainTomorrow']]
if country_filter!='ALL' :
    df_info = df_info[df_info.Location == country_filter]

st.sidebar.dataframe(df_info,500,200)
