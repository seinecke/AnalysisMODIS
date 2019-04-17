import pandas as pd
import click

@click.command()
@click.argument('query')
@click.option('-a', '--app_key', 
			  help='Your APP_KEY from LADS')


def main(query, app_key):
	"""
	This script creates a shell script to download multiple files.
	To specify the file to download, input a .csv, created from ladsweb.
	"""
	df = pd.read_csv(query, 
                 	names=['ID', 'file', 'size'], skiprows=1)

	f = open("download.sh", "w+")

	for file in df.file:
		f.write(create_command(file, app_key)+'\n')
    
	f.close()

def create_command(file, app_key):
	command = 'wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=3' 
	command += ' \"https://ladsweb.modaps.eosdis.nasa.gov'+file+'\"'+' --header'
	command += ' \"Authorization: Bearer {}\"'.format(app_key)
	command += ' -P \"./\"'
	return command

if __name__ == '__main__':
	main()