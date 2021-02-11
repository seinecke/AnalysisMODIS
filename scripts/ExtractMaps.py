from pyhdf.SD import SD, SDC
from scipy.interpolate import griddata
import numpy as np
import pandas as pd
import os
import glob
from geotiepoints.geointerpolator import GeoInterpolator
import matplotlib.pyplot as plt
import re
from datetime import datetime, timedelta
import calendar
import click
import matplotlib.patches as patches

@click.command()
@click.argument('path')
@click.option('-f', '--output_folder', 
			default='./')


def main(path, output_folder):

	df = pd.DataFrame()
	files = glob.glob(path)


	for f in files:
		print(f'Processing file {f}')

		file = SD(f, SDC.READ)

		# Seconds since 1993-01-01 at 0:00:00.0 (TAI)
		sec93 = file.select('Scan_Start_Time').get()[0,0]
		utc = datetime(1993,1,1,0,0) + timedelta(seconds=sec93)
		print(f'Acquisition date: {utc.strftime("%Y-%m-%d %H:%M")}')

		lat5km = file.select('Latitude').get()
		lon5km = file.select('Longitude').get()
		mask1km = file.select('Cloud_Mask_1km').get()
		height1km = file.select('cloud_top_height_1km').get()
		fraction5km = file.select('Cloud_Fraction_Night').get()

		tie_rows = np.arange(2,3000,5)[:np.shape(lat5km)[0]]
		tie_cols = np.arange(2,1500,5)[:np.shape(lat5km)[1]]
		fine_rows = np.arange(0,3000,1)[:np.shape(mask1km)[0]]
		fine_cols = np.arange(0,1500,1)[:np.shape(mask1km)[1]]

		interpolator = GeoInterpolator(
				(lon5km, lat5km), 
				(tie_rows, tie_cols), 
				(fine_rows, fine_cols), 2, 2)
		lon1km, lat1km = interpolator.interpolate()

		lon1km = lon1km.flatten()
		lat1km = lat1km.flatten()

		lon5km = lon5km.flatten()
		lat5km = lat5km.flatten()


		cmask_1 = bits_stripping(1, 2, mask1km[:,:,0]).flatten()
		cheight = height1km.flatten()
		cfraction = fraction5km.flatten()


		for location in ['Arkaroola', 'WesternAustralia', 'Mereenie', 'Arkaroola', 'FowlersGap', 'Woomera', 'SidingSpring', 'Koonamoore', 'Moorook']:

			if location == 'MtBruce':
				lat = -22.608
				lon = 118.144
			elif location == 'MtMeharry':
				lat = -22.980
				lon = 118.588
			elif location == 'WesternAustralia':
				lat = -22.72372
				lon = 118.39802
			elif location == 'Mereenie':
				lat = -23.886
				lon = 132.20
			elif location == 'Arkaroola':
				lat = -30.308
				lon = 139.338
			elif location == 'FowlersGap':
				lat = -31.087
				lon = 141.705
			elif location == 'Woomera':
				lat = -31.099
				lon = 136.786
			elif location == 'SidingSpring':
				lat = -31.2755
				lon = 149.067
			elif location == 'Koonamoore':
				lat = -32.064
				lon = 139.383
			elif location == 'Moorook':
				lat = -34.267
				lon = 140.334
			elif location == 'Adelaide':
				lat = -34.928889
				lon = 138.601111

			dlat = 1
			dlon = 1

			dist1km = np.sqrt( (lon - lon1km) ** 2 + (lat - lat1km) ** 2 )

			if np.min(dist1km) < 0.005:

				print(f'{location} on map')

				grid_x1km, grid_y1km = np.mgrid[lon-dlon:lon+dlon:200j, lat-dlat:lat+dlat:200j]
				grid_x5km, grid_y5km = np.mgrid[lon-dlon:lon+dlon:40j, lat-dlat:lat+dlat:40j]
	        
				intp_cmask = griddata((lon1km,lat1km), 
	                               cmask_1, 
	                               (grid_x1km,grid_y1km), 
	                               method='nearest')
				np.save(f'{output_folder}{location}_cloudmask_{utc.date()}_{utc.time()}_{lon-dlon}_{lon-dlat}_{lat-dlat}_{lat+dlat}.npy', intp_cmask)
	        
				intp_cheight = griddata((lon1km,lat1km), 
	                               cheight, 
	                               (grid_x1km,grid_y1km), 
	                               method='nearest')
				np.save(f'{output_folder}{location}_cloudheight_{utc.date()}_{utc.time()}_{lon-dlon}_{lon-dlat}_{lat-dlat}_{lat+dlat}.npy', intp_cheight)
	        

				intp_cfraction = griddata((lon5km,lat5km), 
	                               cfraction, 
	                               (grid_x5km,grid_y5km), 
	                               method='nearest')
				np.save(f'{output_folder}{location}_cloudfraction_{utc.date()}_{utc.time()}_{lon-dlon}_{lon-dlat}_{lat-dlat}_{lat+dlat}.npy', intp_cfraction)


			else:
				print(f'{location} not on map')



def bits_stripping(bit_start,bit_count,value):
	bitmask = pow(2,bit_start+bit_count)-1
	return np.right_shift(np.bitwise_and(value,bitmask), bit_start)


if __name__ == '__main__':
	main()

