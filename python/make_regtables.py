from __future__ import division
import numpy as np
import pandas as pd

def make_pretty_table(path_str_in, path_str_out):
	'''
	'''
	# read in regression table
	with open(path_str_in, 'r') as f:
		text = f.readlines()

	# turn into DataFrame
	text_dict = {i:[j.strip('\\\n') for j in text[i].split('&') ] for i in range(len(text)) if len(text[i].split('&'))>1 }
	df = pd.DataFrame(text_dict).T

	# sum up columns across short-term and long-term coefficients
	df['col1'] = df[1] + df[2]
	df['col2'] = df[3] + df[4]
	df['col3'] = df[5] + df[6]

	# fix row labels
	df.loc[df[0]=='err ', 0] = '$\hat{\phi}$'
	df[0] = df[0].str.replace('D.', '$\Delta$')


	# make new latex table
	hline = np.argmax(df[0].str.contains('D.').cumsum())

	with open(path_str_out, 'w') as f:
		f.write('\\begin{tabular}{l|lccc} \\hline \n')
		f.write('& Variable & MG & PMG & DFE \\\ \\hline \n')
		f.write('\parbox[t]{2mm}{\multirow{12}{*}{\\rotatebox[origin=c]{90}{Short Run}}} & & & \\\ \n')
		for i in range(3,len(df)-2):	
			
			num1 = df.iloc[i]['col1']
			line = '&' + df.iloc[i][0] + '&' + df.iloc[i]['col1'] + '&' + df.iloc[i]['col2'] + '&' + df.iloc[i]['col3'] + "\\\\"
			f.write(line); f.write('\n')
			
			if i == hline:						
				f.write('&  &  &  &  \\\ \hline \n')			
				f.write('\parbox[t]{2mm}{\multirow{12}{*}{\\rotatebox[origin=c]{90}{Long Run}}} & & & \\\ \n')

		
		# observations and such
		f.write('&'+   '&' +   '&' +   '&' +   '\\\ \hline \n'); f.write('\n')
		i+=2
		line ='&' + df.iloc[i][0].replace(',','') + '&' + df.iloc[i][1] + '&' + df.iloc[i][2] + '&' + df.iloc[i][3] + '\\\ \n'
		f.write(line); f.write('\n')

		num_panels = str( int( int(df.iloc[i][1].strip().replace(',',''))/50 ))
		f.write('& Num. groups  & 50 & 50 & 50 \\\ \n'); f.write('\n')
		f.write('& Obs. per group  &'+num_panels+ '&'+ num_panels+ '&' + num_panels + '\\\ \n')
		f.write('\\end{tabular} \n')


if __name__ == '__main__':
	make_pretty_table('../tables/top10_benchmark.tex', '../tables/top10_benchmark_pretty.tex')
	make_pretty_table('../tables/top1_benchmark.tex', '../tables/top1_benchmark_pretty.tex')
	make_pretty_table('../tables/gini_benchmark.tex', '../tables/gini_benchmark_pretty.tex')
