import numpy as np
import glob
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

import click

@click.command()
@click.argument('input_folder')
@click.option('--plot/--no-plot', default=False)


def main(input_folder, plot):

	for location in ['WesternAustralia', 'Mereenie', 'Arkaroola', 'FowlersGap', 'Woomera', 'SidingSpring', 'Koonamoore', 'Riverland']:

		for measure in ['clouddays', 'cloudmask', 'cloudfraction', 'cloudheight']:

			make_mean_image_year(input_folder, location, measure, plot)
			make_mean_image_season(input_folder, location,  measure, plot)
			make_mean_image_month(input_folder, location, measure, plot)

			print(f'{location} and {measure} done.')


def make_mean_image_year(input_folder, location, measure='cloudmask', plot=False):
    images = glob.glob(f'{input_folder}{location}_{measure}_20*-*-*.npy')
    
    dlon = 1
    dlat = 1
    
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
    elif location == 'Riverland':
        lat = -34.4235
        lon = 139.897
        
    all_images = np.zeros((len(images), np.load(images[0]).shape[0], np.load(images[0]).shape[1]))
    for i in range(len(images)):
        all_images[i] = np.load(images[i])
        
    if measure == 'cloudheight':
        all_images[all_images<0.1] = np.nan
    mean_image = np.nanmean(all_images, axis=0)
    
    if measure == 'clouddays':
        mean_image = np.nansum(all_images < 1.5, axis=0) / np.nansum(all_images < 5, axis=0) * 365

    np.save(f'{location}-{measure}.npy', mean_image)

    if plot:
    
	    plt.imshow(mean_image.T,
	    			vmin=0, 
	               extent=(lon-dlon, lon+dlon, lat+dlat, lat-dlat))
	    
	    if location == 'WesternAustralia':
	        # MtMeharry
	        plt.plot(118.588, -22.980, 'ro')
	        # MtBruce
	        plt.plot(118.144, -22.608, 'ro')
	    else:
	        plt.plot(lon, lat, 'ro')
	        
	    plt.gca().invert_yaxis()
	    plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(0.5))
	    plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(0.5))

	    cbar = plt.colorbar(pad=0.01)

	    if measure == 'cloudmask':
	        plt.clim(0,3)
	        cbar.set_label('Cloud Index', rotation=270, labelpad=10)
	    elif measure == 'cloudheight':
	        #plt.clim(0,4000)
	        cbar.set_label('Cloud Height / m', rotation=270, labelpad=10)
	    elif measure == 'cloudfraction':
	        plt.clim(0,100)
	        cbar.set_label('Cloud Fraction / %', rotation=270, labelpad=10)
        elif measure == 'clouddays':
            cbar.set_label('Number of Days with Clouds', rotation=270, labelpad=10)


	    plt.xlabel('Longitude / deg')
	    plt.ylabel('Latitude / deg')
	    plt.savefig(f'{location}-{measure}.pdf')
	    plt.close()


def make_mean_image_month(input_folder, location, measure='cloudmask', plot=False):
    
    dlon = 1
    dlat = 1
    
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
    elif location == 'Riverland':
        lat = -34.4235
        lon = 139.897
        
    for month in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']:
        
        images = glob.glob(f'{input_folder}{location}_{measure}_20*-{month}-*.npy')

        all_images = np.zeros((len(images), np.load(images[0]).shape[0], np.load(images[0]).shape[1]))
        for i in range(len(images)):
        	all_images[i] = np.load(images[i])
        
        if measure == 'cloudheight':
        	all_images[all_images<0.1] = np.nan
        mean_image = np.nanmean(all_images, axis=0)

        if measure == 'clouddays':
            mean_image = np.nansum(all_images < 1.5, axis=0) / np.nansum(all_images < 5, axis=0) * 365 / 12

        np.save(f'{location}-{measure}-{month}.npy', mean_image)

        if plot: 

	        plt.imshow(mean_image.T,
	        			vmin=0, 
	                   extent=(lon-dlon, lon+dlon, lat+dlat, lat-dlat))

	        if location == 'WesternAustralia':
	            # MtMeharry
	            plt.plot(118.588, -22.980, 'ro')
	            # MtBruce
	            plt.plot(118.144, -22.608, 'ro')
	        else:
	            plt.plot(lon, lat, 'ro')

	        plt.gca().invert_yaxis()
	        plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(0.5))
	        plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(0.5))

	        cbar = plt.colorbar(pad=0.01)

	        if measure == 'cloudmask':
	            plt.clim(0,3)
	            cbar.set_label('Cloud Index', rotation=270, labelpad=10)
	        elif measure == 'cloudheight':
	        	#plt.clim(0,4000)
	            cbar.set_label('Cloud Height / m', rotation=270, labelpad=10)
	        elif measure == 'cloudfraction':
	            plt.clim(0,100)
	            cbar.set_label('Cloud Fraction / %', rotation=270, labelpad=10)
            elif measure == 'clouddays':
                cbar.set_label('Number of Days with Clouds', rotation=270, labelpad=10)

	        plt.xlabel('Longitude / deg')
	        plt.ylabel('Latitude / deg')
	        plt.savefig(f'{location}-{measure}-{month}.pdf')
	        plt.close()


def make_mean_image_season(input_folder, location, measure='cloudmask', plot=False):
    
    dlon = 1
    dlat = 1
    
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
    elif location == 'Riverland':
        lat = -34.4235
        lon = 139.897
        
    for season in ['spring', 'summer', 'autumn', 'winter']:
        
        if season == 'spring':
            images = glob.glob(f'{input_folder}{location}_{measure}_20*-09-*.npy')
            images = np.append(images, glob.glob(f'{input_folder}{location}_{measure}_20*-10-*.npy'))
            images = np.append(images, glob.glob(f'{input_folder}{location}_{measure}_20*-11-*.npy'))
        elif season == 'summer':
            images = glob.glob(f'{input_folder}{location}_{measure}_20*-12-*.npy')
            images = np.append(images, glob.glob(f'{input_folder}{location}_{measure}_20*-01-*.npy'))
            images = np.append(images, glob.glob(f'{input_folder}{location}_{measure}_20*-02-*.npy'))
        elif season == 'autumn':
            images = glob.glob(f'{input_folder}{location}_{measure}_20*-03-*.npy')
            images = np.append(images, glob.glob(f'{input_folder}{location}_{measure}_20*-04-*.npy'))
            images = np.append(images, glob.glob(f'{input_folder}{location}_{measure}_20*-05-*.npy'))
        elif season == 'winter':
            images = glob.glob(f'{input_folder}{location}_{measure}_20*-06-*.npy')
            images = np.append(images, glob.glob(f'{input_folder}{location}_{measure}_20*-07-*.npy'))
            images = np.append(images, glob.glob(f'{input_folder}{location}_{measure}_20*-08-*.npy'))
                  
        all_images = np.zeros((len(images), np.load(images[0]).shape[0], np.load(images[0]).shape[1]))
        for i in range(len(images)):
        	all_images[i] = np.load(images[i])
        
        if measure == 'cloudheight':
        	all_images[all_images<0.1] = np.nan
        mean_image = np.nanmean(all_images, axis=0)

        if measure == 'clouddays':
            mean_image = np.nansum(all_images < 1.5, axis=0) / np.nansum(all_images < 5, axis=0) * 365 / 4

        np.save(f'{location}-{measure}-{season}.npy', mean_image)

        if plot:
	        plt.imshow(mean_image.T, 
	        			vmin=0,
	                   extent=(lon-dlon, lon+dlon, lat+dlat, lat-dlat))

	        if location == 'WesternAustralia':
	            # MtMeharry
	            plt.plot(118.588, -22.980, 'ro')
	            # MtBruce
	            plt.plot(118.144, -22.608, 'ro')
	        else:
	            plt.plot(lon, lat, 'ro')

	        plt.gca().invert_yaxis()
	        plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(0.5))
	        plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(0.5))

	        cbar = plt.colorbar(pad=0.01)

	        if measure == 'cloudmask':
	            plt.clim(0,3)
	            cbar.set_label('Cloud Index', rotation=270, labelpad=10)
	        elif measure == 'cloudheight':
	            #plt.clim(0,4000)
	            cbar.set_label('Cloud Height / m', rotation=270, labelpad=10)
	        elif measure == 'cloudfraction':
	            plt.clim(0,100)
	            cbar.set_label('Cloud Fraction / %', rotation=270, labelpad=10)
            elif measure == 'clouddays':
                cbar.set_label('Number of Days with Clouds', rotation=270, labelpad=10)

	        plt.xlabel('Longitude / deg')
	        plt.ylabel('Latitude / deg')
	        plt.savefig(f'{location}-{measure}-{season}.pdf')
	        plt.close()

if __name__ == '__main__':
	main()
    
    