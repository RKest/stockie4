import subprocess
import sys

import main as ai

def main():
	for i, arg in enumerate(sys.argv):
		if arg == 'train':
			print("Training")
			ai.big_data_slope_send_it()
		if arg == 'load':
			try:
				a = subprocess.run(['node', '-r', 'ts-node/register', '--max-old-space-size=4096', 'src/test.ts', sys.argv[i+1]])
			except IndexError:
				print('Provide number of stock data folders')

if __name__ == '__main__':
	main()