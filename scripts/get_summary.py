import numpy as np
import pandas as pd
from itertools import product
from datetime import datetime

import matplotlib.pyplot as plt

import click
import glob

@click.command()
@click.argument('site')

def main(site):

	### Prepare DataFrame for store summary statistics

	columns = ['site']

	months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun',
	          'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

	seasons = ['winter', 'spring', 'summer', 'autumn']

	measures = ['clouddays', 'cloudfraction', 'cloudheight']
	columns = np.append(columns, measures)

	for measure, month in product(measures, months):
	    columns = np.append(columns, measure + '_' + month)
	    
	for measure, season in product(measures, seasons):
	    columns = np.append(columns, measure + '_' + season)

	df = pd.DataFrame(columns=columns)

	df['site'] = [site]


	### Read files
	files = glob.glob(site+'/*.csv')
	res = pd.DataFrame()

	for f in files:
	    res = res.append(pd.read_csv(f))
	    
	#res.index = np.arange(len(res))
	res = res.reset_index()

	res['year'] = [datetime.fromisoformat(res.date.values[i]).year for i in res.index]
	res['month'] = [datetime.fromisoformat(res.date.values[i]).month for i in res.index]

	years = list(set(res['year']))

	### Calculate summary statistics
	clouddays = []
	cloudfraction = []
	cloudheight = []

	for y in years:
	    days = len(res[(res.cmask_1 < 1.5) & (res.year == y) & (res.cmask_0 == 1)])
	    total = len(res[(res.year == y) & (res.cmask_0 == 1)])
	    clouddays += [days / total * 365]
	    
	    cloudfraction += [np.mean(res.cloudfraction[(res.year == y) & (res.cmask_0 == 1)])]

	    cloudheight += [np.mean(res.height[(res.year == y) & (res.cmask_1 < 1.5) & (res.cmask_0 == 1)])]

	df['clouddays'][df.site == site] = np.mean(clouddays)
	df['cloudfraction'][df.site == site] = np.mean(cloudfraction)
	df['cloudheight'][df.site == site] = np.mean(cloudheight) / 1000


	for m in range(len(months)):
	    clouddays = []
	    cloudfraction = []
	    cloudheight = []
	    
	    for y in years:
	        days = len(res[(res.cmask_1 < 1.5) & (res.year == y) & (res.month == m+1) & (res.cmask_0 == 1)])
	        total = len(res[(res.year == y) & (res.month == m+1) & (res.cmask_0 == 1)])
	        clouddays += [days / total * 31]
	    
	    cloudfraction += [np.mean(res.cloudfraction[(res.year == y) & (res.month == m+1) & (res.cmask_0 == 1)])]

	    cloudheight += [np.mean(res.height[(res.year == y) & (res.month == m+1) & (res.cmask_1 < 1.5) & (res.cmask_0 == 1)])]

	    df['clouddays_'+months[m]][df.site == site] = np.mean(clouddays)
	    df['cloudfraction_'+months[m]][df.site == site] = np.mean(cloudfraction)
	    df['cloudheight_'+months[m]][df.site == site] = np.mean(cloudheight) / 1000

	
	for measure in measures:
	    df[measure+'_spring'] = df[measure+'_sep'] + df[measure+'_oct'] + df[measure+'_nov'] 
	    df[measure+'_summer'] = df[measure+'_dec'] + df[measure+'_jan'] + df[measure+'_feb']
	    df[measure+'_autumn'] = df[measure+'_mar'] + df[measure+'_apr'] + df[measure+'_may']
	    df[measure+'_winter'] = df[measure+'_jun'] + df[measure+'_jul'] + df[measure+'_aug']

	    if measure != 'clouddays':
	    	df[measure+'_spring'] = df[measure+'_spring'] / 3
	    	df[measure+'_summer'] = df[measure+'_summer'] / 3
	    	df[measure+'_autumn'] = df[measure+'_autumn'] / 3
	    	df[measure+'_winter'] = df[measure+'_winter'] / 3
	   

	### Store summary statistics
	df.to_csv(site+'/'+site+'_summary.csv', index=False)
	

if __name__ == '__main__':
	main()