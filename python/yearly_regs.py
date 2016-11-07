import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import geopandas as geo

import matplotlib as mpl
mpl.rc('font', family='serif')


if __name__ == '__main__':

	# export data to stata, drops duplicates
	big_df = pd.read_pickle('../data/income_startup_state.p')
	big_df['ln_WageTax_total'] = np.log(big_df['WageTax_total'])

	beta_dict = {}
	tstat_dict = {}

	for year in range(1999, 2014):
		df = big_df[big_df.year == year]

		Yvar = 'inc_ineq1'
		Xvar = ['ln_WageTax_total',
				# 'ln_pct_retired',
				'ln_edu_college',
				'ln_patents',
				'ln_exp_pct',
				'ln_fire_pct',
				'ln_pct_black']


		beta_dict[year] = pd.ols(y=df[Yvar], x=df[Xvar]).beta
		tstat_dict[year] = pd.ols(y=df[Yvar], x=df[Xvar]).t_stat

	ols_df = pd.DataFrame(beta_dict).T
	ols_df.drop('intercept', axis=1, inplace=True)


	fig, ax = sns.plt.subplots(1, 1, figsize=(7, 4))
	ols_df.plot(ax=ax, linewidth=2)
	ax.legend(bbox_to_anchor=(.9, -.13),fontsize=13, ncol=2)		
	fig.savefig('../figures/top1_yearly_regs.pdf', bbox_inches='tight')	
		
