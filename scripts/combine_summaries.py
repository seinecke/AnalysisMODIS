import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

import click
import glob

@click.command()
@click.argument('sites')

def main(sites):

	df = pd.DataFrame()

	for site in sites:
		df = df.append(pd.read_csv(site+'_summary.csv'))
	
	df = df.reset_index()
	
	df.to_csv('summary.csv', index=False)
	

if __name__ == '__main__':
	main()