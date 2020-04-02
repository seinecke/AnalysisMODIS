import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

import click


#@click.command()
#@click.argument('path')

def main():

	# df = pd.read_csv(path)

	# plt.plot(df.visibility, 'o', color='grey')
	# plt.xlabel('Time')
	# plt.ylabel('Mean Cloud Index')
	# plt.ylim([-0.1,3.1])
	# plt.show()

	# plt.hist(df.visibility, 
	# 	bins=10, range=(0,3), color='grey')
	# plt.xlabel('Mean Cloud Index')
	# plt.show()


	df1 = pd.read_csv('/Users/a1224137/CTR/MODIS/AnalysisMODIS/Arkaroola/2018.csv')
	df1 = df1.append(pd.read_csv('/Users/a1224137/CTR/MODIS/AnalysisMODIS/Arkaroola/2017.csv'))
	df1 = df1.append(pd.read_csv('/Users/a1224137/CTR/MODIS/AnalysisMODIS/Arkaroola/2016.csv'))
	#df1 = df1.append(pd.read_csv('/Users/a1224137/CTR/MODIS/AnalysisMODIS/Arkaroola/2015.csv'))

	df2 = pd.read_csv('/Users/a1224137/CTR/MODIS/AnalysisMODIS/Barmera/2018.csv')
	df2 = df2.append(pd.read_csv('/Users/a1224137/CTR/MODIS/AnalysisMODIS/Barmera/2017.csv'))
	df2 = df2.append(pd.read_csv('/Users/a1224137/CTR/MODIS/AnalysisMODIS/Barmera/2016.csv'))
	#df2 = df2.append(pd.read_csv('/Users/a1224137/CTR/MODIS/AnalysisMODIS/Barmera/2015.csv'))

	plt.hist(df1.visibility, label='Arkaroola',
		bins=6, range=(0,3), color='grey', alpha=0.3)
	plt.hist(df2.visibility, label='Barmera',
		bins=6, range=(0,3), color='darkblue', alpha=1, lw=2, histtype='step')
	plt.xlabel('Mean Cloud Index')
	plt.ylabel('Number of Days')
	plt.legend()
	plt.savefig('Hist2016-2018.svg')

	plt.show()


if __name__ == '__main__':
	main()