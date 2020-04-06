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
@click.option('-o', '--output_file')
@click.option('-c', '--coords',
			nargs=2, type=float,
			help = 'Latitude of desired location. First number is longitude, second latitude.')
@click.option('-l', '--location',
	type=click.Choice(['MtBruce','MtMeharry','Mereenie','Arkaroola',
						'FowlersGap','Woomera','SidingSpring','Koonamoore',
						'Moorook','Adelaide']))
@click.option('--maps/--no-maps', default=False)

def main(path, output_folder, output_file, location, coords, maps):

	df = pd.DataFrame()
	files = glob.glob(path)

	if location == 'MtBruce':
		lat = -22.608
		lon = 118.144
	elif location == 'MtMeharry':
		lat = -22.980
		lon = 118.588
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
	else:
		#if len(location) > 0:
		#	raise Exception('This location is not pre-defined. Please specify the coordinates.')
		print(len(coords))
		if len(coords) != 2:
			raise Exception('Please specify a location or coordinates.')
		else:
			lon = coords[0]
			lat = coords[1]
			location = f'Lon{lon}_Lat{lat}'


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


		cmask_0 = bits_stripping(0, 1, mask1km[:,:,0]).flatten()
		cmask_1 = bits_stripping(1, 2, mask1km[:,:,0]).flatten()
		cmask_3 = bits_stripping(3, 1, mask1km[:,:,0]).flatten()
		cmask_4 = bits_stripping(4, 1, mask1km[:,:,0]).flatten()
		cmask_5 = bits_stripping(5, 1, mask1km[:,:,0]).flatten()
		cmask_6 = bits_stripping(6, 2, mask1km[:,:,0]).flatten()
		cmask_8 = bits_stripping(8, 1, mask1km[:,:,0]).flatten()
		cmask_14 = bits_stripping(14, 1, mask1km[:,:,0]).flatten()
		cmask_15 = bits_stripping(15, 1, mask1km[:,:,0]).flatten()
		cmask_17 = bits_stripping(17, 1, mask1km[:,:,0]).flatten()
		cmask_18 = bits_stripping(18, 1, mask1km[:,:,0]).flatten()
		cmask_19 = bits_stripping(19, 1, mask1km[:,:,0]).flatten()


		cheight = height1km.flatten()
		cfraction = fraction5km.flatten()

		dist1km = np.sqrt( (lon - lon1km) ** 2 + (lat - lat1km) ** 2 )
		dist5km = np.sqrt( (lon - lon5km) ** 2 + (lat - lat5km) ** 2 )

		if np.min(dist1km) < 0.005:
			idx1km = np.argmin(dist1km)
			idx5km = np.argmin(dist5km)

			df = df.append({
					'date': utc, 
					'filename': f,
					'cmask_0': cmask_0[idx1km],
					'cmask_1': cmask_1[idx1km],
					'cmask_3': cmask_3[idx1km],
					'cmask_4': cmask_4[idx1km],
					'cmask_5': cmask_5[idx1km],
					'cmask_6': cmask_6[idx1km],
					'cmask_8': cmask_8[idx1km],
					'cmask_14': cmask_14[idx1km],
					'cmask_15': cmask_15[idx1km],
					'cmask_17': cmask_17[idx1km],
					'cmask_18': cmask_18[idx1km],
					'cmask_19': cmask_19[idx1km],
					'cloudfraction': cfraction[idx5km],
					'height':cheight[idx1km],
					}, 
					ignore_index=True)

			if maps:

				size_map = 0.25
				idx_map = (lon1km > (lon - size_map)) & (lon1km < (lon + size_map))
				idx_map = idx_map & (lat1km > (lat - size_map)) & (lat1km < (lat + size_map))
				
				grid_x, grid_y = np.mgrid[np.min(lon1km[idx_map]):np.max(lon1km[idx_map]):100j, 
										  np.min(lat1km[idx_map]):np.max(lat1km[idx_map]):200j]
				intp_cmask = griddata((lon1km[idx_map],lat1km[idx_map]), cmask_1[idx_map], 
											(grid_x,grid_y), method='nearest')
				intp_cheight = griddata((lon1km[idx_map],lat1km[idx_map]), cheight[idx_map], 
											(grid_x,grid_y), method='nearest')
				
				np.save(f'{output_folder}{location}_cloudmask_{utc.date()}_{utc.time()}_{np.min(lon1km[idx_map])}_{np.max(lon1km[idx_map])}_{np.min(lat1km[idx_map])}_{np.max(lat1km[idx_map])}.npy', intp_cmask)
				np.save(f'{output_folder}{location}_cloudheight_{utc.date()}_{utc.time()}_{np.min(lon1km[idx_map])}_{np.max(lon1km[idx_map])}_{np.min(lat1km[idx_map])}_{np.max(lat1km[idx_map])}.npy', intp_cheight)
		
		else:
			print('Site not on map')

	
	df = df.sort_values(by='date', ascending=True) #reorders dataframe so histogram will be in correct order
	if output_file  == None:
		df.to_csv(f'{output_folder}{location}_{df.date.min()}_{df.date.max()}.csv', index=False)
	else:
		df.to_csv(output_folder+output_file, index=False)



def bits_stripping(bit_start,bit_count,value):
	bitmask = pow(2,bit_start+bit_count)-1
	return np.right_shift(np.bitwise_and(value,bitmask), bit_start)


if __name__ == '__main__':
	main()