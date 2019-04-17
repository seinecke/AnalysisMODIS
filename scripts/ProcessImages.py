from pyhdf.SD import SD, SDC
from scipy.interpolate import griddata
import numpy as np
import pandas as pd
import os
import glob
from geotiepoints.geointerpolator import GeoInterpolator
import matplotlib.pyplot as plt
import re
import datetime
import calendar
import click
import matplotlib.patches as patches

@click.command()
@click.argument('path')
@click.option('-f', '--output_folder', 
			default='./')
@click.option('-o', '--output_file')
@click.option('-s', '--size_map',
				default=0.25)
@click.option('--size_mean', 
			default=0.25)
@click.option('-c', '--coords',
			nargs=2, type=float,
			help = 'Latitude of desired location. First number is longitude, second latitude.')
@click.option('-l', '--location',
	type=click.Choice(['Adelaide', 'Arkaroola', 'Barmera']))

def main(path, output_folder, output_file, size_map, size_mean, location, coords):

	df = pd.DataFrame(columns=['date', 'visibility'])
	files = glob.glob(path)

	if location == 'Arkaroola':
		lat = -30.311667
		lon = 139.336111
	elif location == 'Adelaide':
		lat = -34.928889
		lon = 138.601111
	elif location == 'Barmera':
		lat = -34.25
		lon = 140.466667
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

		year = int(f[28:32])
		day = int(f[32:35])
		hour = int(f[36:38])
		minute = int(f[38:40])
		print(year, day, hour, minute)
		date_time = ( datetime.datetime(year, 1, 1, hour, minute) 
					+ datetime.timedelta(day - 1) )
		print(f'Acquisition date: {date_time.strftime("%Y-%m-%d %H:%M")}')

		file = SD(f, SDC.READ)
		datasets_dic = file.datasets()
		lat5km = file.select('Latitude').get()
		long5km = file.select('Longitude').get()
		mask1km = file.select('Cloud_Mask_1km').get()

		if np.shape(long5km)[0] == 406:

			tie_rows = np.arange(2,2030,5)
			tie_cols = np.arange(2,1350,5)
			fine_rows = np.arange(2030)
			fine_cols = np.arange(1354)

			interpolator = GeoInterpolator((long5km, lat5km), 
											(tie_rows, tie_cols), 
											(fine_rows, fine_cols), 
											2, 2)
			long1km, lat1km = interpolator.interpolate()

			mask = np.zeros(np.shape(mask1km)[:2])
			valx = bits_stripping(1,2,mask1km[:,:,0])

			square_size = 2*size_mean

			lonx = long1km.flatten()
			latx = lat1km.flatten()
			val = valx.flatten()

			idx_map = (lonx > (lon - size_map)) & (lonx < (lon+size_map))
			idx_map = idx_map & (latx > (lat - size_map)) & (latx < (lat + size_map))

			idx_mean = (lonx > (lon - size_mean)) & (lonx < (lon+size_mean))
			idx_mean = idx_mean & (latx > (lat - size_mean)) & (latx < (lat + size_mean))

			if len(val[idx_mean]) > (size_mean**2 * 25000.):

				mean = np.mean(val[idx_mean])

				grid_x, grid_y = np.mgrid[np.min(lonx[idx_map]):np.max(lonx[idx_map]):100j, np.min(latx[idx_map]):np.max(latx[idx_map]):200j]
				intp = griddata((lonx[idx_map],latx[idx_map]), val[idx_map], (grid_x,grid_y), method='nearest')

				fig, ax = plt.subplots(figsize=(6,5))
				img = ax.imshow(intp.T, extent=(
						  np.min(lonx[idx_map]),
						  np.max(lonx[idx_map]),
						  np.max(latx[idx_map]), 
						  np.min(latx[idx_map])),
						  cmap='bone',
						  vmin=0, vmax=3)
				ax.plot([lon], [lat], marker='x', 
						markersize=10, mew=3, color="red") #indicates place of interest
				ax.invert_yaxis()
				ax.set_ylabel('Latitude / deg')
				ax.set_xlabel('Longitude / deg')
				ax.text(0.05, 0.95, f'{location}\n{date_time.strftime("%Y-%m-%d %H:%M")}', 
					transform = plt.gca().transAxes,
					horizontalalignment='left', 
					verticalalignment='top',
					bbox=dict(facecolor='white', alpha=0.8)) 
				square = patches.Rectangle(((lon - size_mean), 
											(lat - size_mean)), 
											square_size, 
											square_size, 
											lw = 1, edgecolor = 'red', 
											facecolor = 'none')
				ax.add_patch(square) #creates square over area we are taking the mean of				
				ax.text(0.95, 0.95, 
					'Mean Cloud Index: {:.2f}'.format(mean), 
					transform = plt.gca().transAxes,
					horizontalalignment='right', 
					verticalalignment='top',
					bbox=dict(facecolor='white', alpha=0.8)) 
				# cloud index of 0 is cloudy, 3 is clear
				cbar = fig.colorbar(img)
				cbar.set_label('Cloud Index')
				fig.savefig(f'{output_folder}{location}_{date_time.date()}_{date_time.time()}.pdf')

				df = df.append({'date': date_time, 'visibility':mean}, ignore_index=True)

			else:
				print('Map contains not enough information')

		else:
			print('Strange shape')
	
	df = df.sort_values(by='date', ascending=True) #reorders dataframe so histogram will be in correct order
	if output_file  == None:
		df.to_csv(f'{output_folder}{location}_{df.date.min()}_{df.date.max()}.csv', index=False)
	else:
		df.to_csv(output_folder+output_file, index=False)



def bits_stripping(bit_start,bit_count,value):
	bitmask=pow(2,bit_start+bit_count)-1
	return np.right_shift(np.bitwise_and(value,bitmask),bit_start)


if __name__ == '__main__':
	main()