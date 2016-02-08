#Criminal Incident Analysis
#Seattle and San FRancisco information are analyzed
####
#Load libraries
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as matdates
#Set visualization settings
pd.set_option('display.mpl_style', 'default')
pd.set_option('display.width', 4000)
pd.set_option('display.max_columns', 800)
#Load data from Seattle and San Francisco
src_data_df = pd.read_csv("seattle_incidents_summer_2014.csv", low_memory=False,  index_col=False)
src_data_sf_df = pd.read_csv("sanfrancisco_incidents_summer_2014.csv", low_memory=False,  index_col=False)
#Seattle incident time information requires to be classify 
def strip_and_classify_time(fulltms):
    """
    Extract time from the 'Occurred Date or Date Range Start' field and classify it 
    """
    rawtime = fulltms[11:]
    ht24 = 0
    if ("PM" in rawtime):
        ht24 = int(rawtime[0:2])
        ht24 += 12
        nwtm = str(ht24) + rawtime[2:]
        rawtime = nwtm
    htst = rawtime[0:2]
    ht24 = int(htst)
    if ht24 > 23 or ht24 == 0:
        return "Midnight"
    elif ht24 >=1 and ht24 <= 4:
        return "01:00 AM to 04:00 AM"    
    elif ht24 >=5 and ht24 <= 8:
        return "05:00 AM to 08:00 AM"
    elif ht24 >=9 and ht24 <= 12:
        return "09:00 AM to 12:00 PM"
    elif ht24 >=13 and ht24 <= 16:
        return "01:00 PM to 04:00 PM"
    elif ht24 >=17 and ht24 <= 20:
        return "05:00 PM to 08:00 PM"	
    elif ht24 >=21 and ht24 < 24:
        return "09:00 PM to 12:00 AM"
    else:
        return "time out of range"	  

#San Francisco incident information requires different processing in order to be classified
def strip_and_classify_timeSF(fulltms):
    """
    Extract time from the 'Time' field and classify it 
    """
    rawtime = fulltms
    ht24 = 0
    htst = rawtime[0:2]
    ht24 = int(htst)
    if ht24 > 23 or ht24 == 0:
        return "Midnight"
    elif ht24 >=1 and ht24 <= 4:
        return "01:00 AM to 04:00 AM"    
    elif ht24 >=5 and ht24 <= 8:
        return "05:00 AM to 08:00 AM"
    elif ht24 >=9 and ht24 <= 12:
        return "09:00 AM to 12:00 PM"
    elif ht24 >=13 and ht24 <= 16:
        return "01:00 PM to 04:00 PM"
    elif ht24 >=17 and ht24 <= 20:
        return "05:00 PM to 08:00 PM"	
    elif ht24 >=21 and ht24 < 24:
        return "09:00 PM to 12:00 AM"
    else:
        return "time out of range"	 

#Create new column classifying time of the day for Seattle and San Francisco
src_data_df['Period of Time'] = src_data_df['Occurred Date or Date Range Start'].apply(strip_and_classify_time)
src_data_sf_df['Period of Time'] = src_data_sf_df['Time'].apply(strip_and_classify_timeSF)

#Gets period of time in the day with more incidents for Seattle
crimeBytime = pd.DataFrame(src_data_df['Period of Time'].value_counts())
#Creates horizontal graphic
crimeBytime.plot(kind='barh')

#Gets period of time in the day with more incidents for San Francisco
crimeBytimeSF = pd.DataFrame(src_data_sf_df['Period of Time'].value_counts())
#Creates horizontal graphic
crimeBytimeSF.plot(kind='barh')

#Now get the top ten main incidents occured at the time where Seattle has more incidents
crimeTypeByTime = src_data_df.groupby(['Period of Time','Summarized Offense Description']).size()
crimeTypeByTimedf = crimeTypeByTime.to_frame()
cdf1= pd.DataFrame(crimeTypeByTimedf)
cdf1.reset_index(inplace=True)
#Rename column names
cdf1.columns = ['PeriodOfTime', 'OffenseDescription', 'Offenses']
cdf1.loc[cdf1['PeriodOfTime'].isin(['05:00 PM to 08:00 PM'])].sort(['Offenses'], ascending=False)[:10]
mostCommonEveningOffenses=cdf1.loc[cdf1['PeriodOfTime'].isin(['05:00 PM to 08:00 PM'])].sort(['Offenses'], ascending=False)[['OffenseDescription','Offenses']][:10]
mostCOmmonOffenses=mostCommonEveningOffenses.set_index('OffenseDescription')
mostCOmmonOffenses.plot(kind='barh')

#Now get the top ten main incidents occured at the time when San Francisco has more incidents
crimeTypeByTimeSF = src_data_sf_df.groupby(['Period of Time','Category']).size()
crimeTypeByTimeSFdf = crimeTypeByTimeSF.to_frame()
crimeSFdf1= pd.DataFrame(crimeTypeByTimeSFdf)
crimeSFdf1.reset_index(inplace=True)
#Rename column names
crimeSFdf1.columns = ['PeriodOfTime', 'OffenseDescription', 'Offenses']
crimeSFdf1.loc[crimeSFdf1['PeriodOfTime'].isin(['05:00 PM to 08:00 PM'])].sort_values(['Offenses'], ascending=False)[:10]
mostCommonEveningOffensesSF=crimeSFdf1.loc[crimeSFdf1['PeriodOfTime'].isin(['05:00 PM to 08:00 PM'])].sort_values(['Offenses'], ascending=False)[['OffenseDescription','Offenses']][:10]
mostCOmmonOffensesSF=mostCommonEveningOffensesSF.set_index('OffenseDescription')
mostCOmmonOffensesSF.plot(kind='barh')

#Incidents by Zone in Seattle
#theft incidents
crimeByNeighborhood = src_data_df.groupby(['Hundred Block Location','Zone/Beat','Offense Type','Summarized Offense Description']).size()
crimeByZonedf = crimeByNeighborhood.to_frame()
crimeByZonedf.reset_index(inplace=True)
crimeByZonedf.columns = ['Hundred Block Location', 'Zone/Beat','Offense Type', 'Summarized Offense Description', 'Incidens']
mainTheftZones =crimeByZonedf.loc[crimeByZonedf['Offense Type'].str.contains('THEFT')].sort(['Incidens'], ascending=False)[:10]
mainTheftZones[['Hundred Block Location','Summarized Offense Description','Incidens']]
mtz=mainTheftZones[['Hundred Block Location','Summarized Offense Description','Incidens']]
mainTheftZones=mtz.set_index('Hundred Block Location')
mainTheftZones.plot(kind='barh')

#Incidents by Zone in San Francisco
#theft incidents
crimeBypdDistrict = src_data_sf_df.groupby(['PdDistrict','Category']).size()
crimeBypdDistrict.columns=['PdDistrict', 'Category', 'Offenses']

crimePdDistrict= pd.DataFrame(crimeBypdDistrict)
crimePdDistrict.reset_index(inplace=True)
crimePdDistrict.columns = ['PdDistrict', 'OffenseDescription', 'Offenses']
top10crimePdDist=crimePdDistrict.sort_values(['Offenses'], ascending=False)[:10]
top10crimePdDist['PdDistrict'] = top10crimePdDist.PdDistrict.map(str) +" - " + top10crimePdDist.OffenseDescription
del top10crimePdDist['OffenseDescription']
top10crimePdDist.columns = ['PdDistrict - Offense Category', 'Offenses']
top10crimePdDist.set_index('PdDistrict - Offense Category')
top10crimePdDist.plot(kind='barh')

#summer Crime Incidents in Seattle 
summerCrimedf = src_data_df.loc[src_data_df['Month'].isin([6,7,8])]
summerCrime = summerCrimedf.groupby(['Month']).size()

def getthedate(fulldt):
     return fulldt[0:10]

#Create new column only date
src_data_df['crimedate'] = src_data_df['Occurred Date or Date Range Start'].apply(getthedate)
crimebyday = src_data_df.groupby(['crimedate']).size()
#In order to create a time graph we need format the dates
def getfmtdate(olddate):
    return matdates.datestr2num(olddate) 

	
crimebyday = crimebyday.to_frame()	
crimebyday.reset_index(inplace=True)
crimebyday['crimedate'] = crimebyday['crimedate'].apply(getfmtdate)
crimebyday.columns = ['crimedate', 'Incidents']
plt.style.use('ggplot')
plt.plot_date(x=crimebyday['crimedate'], y=crimebyday['Incidents'], fmt="b-")
plt.title("Crime Incidents Day by Day")
plt.ylabel("Incidents")
plt.grid(True)

#summer Crime Incidents in San Francisco
summerCrimedf = src_data_sf_df.loc[src_data_sf_df['Month'].isin([6,7,8])]
summerCrime = summerCrimedf.groupby(['Month']).size()
#Create new column only date
src_data_sf_df['crimedate'] = src_data_sf_df['Occurred Date or Date Range Start'].apply(getthedate)
crimebyday = src_data_sf_df.groupby(['crimedate']).size()
crimebyday = crimebyday.to_frame()	
crimebyday.reset_index(inplace=True)
crimebyday['crimedate'] = crimebyday['crimedate'].apply(getfmtdate)
crimebyday.columns = ['crimedate', 'Incidents']
plt.style.use('ggplot')
plt.plot_date(x=crimebyday['crimedate'], y=crimebyday['Incidents'], fmt="b-")
plt.title("Crime Incidents Day by Day")
plt.ylabel("Incidents")
plt.grid(True)

#how do incidents vary by time of day? Which incidents are most common in the evening? During what periods of the day are robberies most common?