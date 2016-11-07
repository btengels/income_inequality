import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import geopandas as geo

import matplotlib as mpl
mpl.rc('font', family='serif')

def export_df(df):
	'''
	'''
	#----------------------------------------------
	# startup_history_by_state
	# take logs of lhs variables
	#----------------------------------------------
	# df['inc_ineq1'] = np.log(df['Top10_adj'])
	# df['inc_ineq2'] = np.log(df['Top5_adj'])
	# df['inc_ineq3'] = np.log(df['Gini'])

	#----------------------------------------------
	# right-hand side variables
	#----------------------------------------------
	df.rename(columns={'Startup Density':'ent1',
						'Rate of New Entrepreneurs':'ent2',
						'Opportunity Share of New Entrepreneurs':'ent3',
						'Top10_adj':'inc_ineq1',
						'Top5_adj':'inc_ineq2',
						'Gini':'inc_ineq3'}, inplace=True)

	df['ln_ent1'] = np.log(df['ent1'])
	df['ln_ent2'] = np.log(df['ent2'])
	df['ln_ent3'] = np.log(df['ent3'])

	df['ln_fire_pct'] = np.log(df['fire_pct'])
	df['ln_fire_pct_sq'] = np.log(df['fire_pct'])**2

	df['ln_pct_black'] = np.log(df['pct_black'])
	df['ln_pct_black_sq'] = np.log(df['pct_black'])**2

	df['ln_pct_retired'] = np.log(df['pct_retired'])
	df['ln_pct_retired_sq'] = np.log(df['pct_retired'])**2

	#----------------------------------------------
	# education variables
	#----------------------------------------------
	df['HighSchool'] = df['HighSchool'].astype(float)
	df['College'] = df['College'].astype(float)
	df['ln_edu_hs'] = np.log( df['HighSchool'] )
	df['ln_edu_college'] = np.log( df['College'] )
	df['ln_edu_college_sq'] = np.log( df['College'] )**2

	#----------------------------------------------
	# patent variables
	#----------------------------------------------
	df['ln_patents'] = np.log( df['patents'] )
	df['ln_patents_sq'] = np.log( df['patents'] )**2

	#----------------------------------------------
	# exports variables
	#----------------------------------------------
	df['ln_exp_pct'] = np.log( df['exp_pct'] )
	df['ln_exp_pct_sq'] = np.log( df['exp_pct'] )**2

	#----------------------------------------------
	# export to stata for panel regressions
	#----------------------------------------------
	df_new = df[[y for y in df.columns if df[y].dtype != 'object']]
	df_new.drop_duplicates(inplace=True)
	df_new.to_stata('../data/income_startup_state.dta')
	df_new.to_pickle('../data/income_startup_state.p')

	return None


def make_spaghetti_plot(small_df, full_df, column, filename, title, xlabel, ylabel, ylim ):
	'''
	Makes a "spaghetti plot" from a "long" DataFrame (panel data). The variable specified
	by "column" is plotted in bold while the similar column in "full_df" is plotted very
	lightly for each state.

	INPUTS:
	----------------------------------------------------------------------------------
	small_df - pandas DataFrame  for one state of a larger panel
	full_df - pandas DataFrame for larger panel
	column - common variable for small_df and full_df
	filename - string, contains path for saved image
	title - string, contains title for image
	xlabel - string, contains label for x axis
	ylabel - string, contains label for y axis
	ylim - tuple, contains two scalars (ymin,ymax) for setting bounds on y axis

	OUTPUTS:
	----------------------------------------------------------------------------------
	No output. Function just saves the figure.
	'''
	sns.set_style(style='darkgrid')
	mpl.rc('font',family='serif')

	# set up figure and axis object
	fig, ax = sns.plt.subplots(1,1,figsize=(10,5))

	# plot main state (bold line)
	small_df[column].plot(ax=ax, alpha=1, linewidth=4)

	# plot other states (faint lines, just to provide context)
	for fip_id in full_df.cofips.unique():
		df = full_df[full_df.cofips==fip_id].set_index('year')
		df[column].plot(ax=ax, alpha=.2, linewidth=.7)


	# save figure
	# ax.set_title(title, fontsize=14)
	ax.set_ylabel(ylabel, fontsize=14)
	ax.set_xlabel(xlabel, fontsize=14)
	ax.tick_params(labelsize=14)
	ax.set_ylim(ylim)
	fig.savefig(filename,dpi=500, bbox_inches='tight')
	plt.close()


def make_USmap(df, column, filename, title, ylabel):
	'''
	This function takes a geopandas DataFrame and plots the contiguous states.
	The colors vary with 'column', which is also depicted in a color bar
	adjacent to the map.

	INPUTS:
	----------------------------------------------------------------------------------
	df - geopandas DataFrame with a column given by the input 'column'
	column - string, denotes which column determines the color of each state
	filename - string, path of figure when saved
	title - string, title of figure
	ylable - string, units of 'column' (plotted next to color bar)

	OUTPUTS:
	----------------------------------------------------------------------------------
	None, just plots the figure
	'''
	sns.set_style(style='dark')
	mpl.rc('font',family='serif')
	cmap = 'cool'

	df = df[df.in_map==1]
	df = df[(df.STUSPS != 'HI') & (df.STUSPS != 'AK')]
	fig, ax = sns.plt.subplots(1,1,figsize=(10,5))
	df.plot(column=column, ax=ax, linewidth=.5, linecolor='white', cmap=cmap, alpha=1)
	ax.set_ylim(24,51)
	ax.set_xlim(-127,-65)
	ax.set_xticklabels([])
	ax.set_yticklabels([])
	# ax.set_title(title, fontsize=14)

	# add colorbar...this is an ugly workaround
	cax = fig.add_axes([0.9, 0.1, 0.05, 0.8])
	cax.tick_params(labelsize=14)
	ax2 = cax.twinx()
	ax2.set_ylabel(ylabel,labelpad=40, fontsize=14)
	ax2.set_xticklabels([])
	ax2.set_yticklabels([])

	vmin, vmax = df[column].min(), df[column].max()
	sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=vmin, vmax=vmax))
	sm._A = []
	fig.colorbar(sm, cax=cax)
	fig.savefig(filename, dpi=500, bbox_inches='tight')
	plt.close()


def make_US_scatter(US_geo, xcol, ycol, filename, xlabel, ylabel):
	'''
	'''
	sns.set_style(style='darkgrid')
	mpl.rc('font',family='serif')

	US_geo = US_geo[US_geo.in_map>0]
	fig, ax = sns.plt.subplots(1,1, figsize=(10,5))
	for i in range(len(US_geo)):
		state = US_geo.STUSPS.values[i]
		xy = (US_geo[xcol].values[i], US_geo[ycol].values[i])
		ax.annotate(s=state, xy=xy)

	ax.set_xlabel(xlabel)
	ax.set_ylabel(ylabel)
	xmin,xmax = US_geo[xcol].min()-.1, US_geo[xcol].max()+.1

	ax.set_xlim(xmin,xmax)
	ax.set_ylim(0,1)
	fig.savefig(filename, dpi=500, bbox_inches='tight')
	plt.close()

if __name__ == '__main__':

	# read in demographic data
	age_df  = pd.read_pickle('../data/age_race_df.p')
	age_df.drop_duplicates(inplace=True)

	age_list = ['0-4','5-9','10-14','15-19','20-24','25-29','30-34','35-39','40-44','45-49','50-54','55-59','60-64','65-69','70-74','75-79','80-84','85+']

	# create a few additional variables of interest
	age_df.rename(columns={'total':'total_population'}, inplace=True)
	age_df['pct_black'] = age_df[['total_black_male','total_black_female']].sum(axis=1)/age_df['total_population']
	age_df['pct_minority'] = age_df[['total_black_male','total_black_female','total_other_male','total_other_female']].sum(axis=1)/age_df['total_population']
	age_df['pct_retired'] = np.array([age_df.filter(like=a).sum(axis=1) for a in age_list[13:]]).sum(axis=0)/age_df['total_population']
	age_df['pct_working'] = np.array([age_df.filter(like=a).sum(axis=1) for a in age_list[3:13]]).sum(axis=0)/age_df['total_population']
	age_df['pct_children'] = np.array([age_df.filter(like=a).sum(axis=1) for a in age_list[0:3]]).sum(axis=0)/age_df['total_population']
	age_df['dep_ratio'] = (age_df['pct_retired']+age_df['pct_children'])/age_df['pct_working']

	#----------------------------------------------
	# pull in data on income inequality and entrepreneurship and merge
	#----------------------------------------------
	incShare_df = pd.read_excel("../data/Frank_WTID_2013.xls",sheetname='IncomeShares')
	incThresh_df = pd.read_excel("../data/Frank_WTID_2013.xls",sheetname='PercentileThresholds')
	gini_df = pd.read_excel("../data/Frank_Gini_2013.xls")

	# merge all the inequality data
	ineq_df = pd.merge(incThresh_df, gini_df, left_on=['cofips','year'], right_on=['st','Year'])
	incomeRaw_df = pd.merge(incShare_df, ineq_df, left_on=['cofips','year'], right_on=['cofips','year'])
	incomeRaw_df.drop(['st','Year','State'],axis=1, inplace=True)

	# TAXSIM data on entrepreneurship
	tax_df1 = pd.read_excel("../data/TAXSIM_1984income_fixed.xlsx", sheetname='average_rates')
	tax_df = pd.read_excel("../data/TAXSIM_1984income_fixed.xlsx", sheetname='maximum_rates')
	tax_df = tax_df.merge(tax_df1, on=['year','state_name'], how='left')
	tax_df.drop('StateID_y', axis=1,inplace=True)
	tax_df.rename(columns={'StateID_x':'StateID'}, inplace=True)
	tax_df[['StateID','year']] = tax_df[['StateID','year']].astype(int)
	tax_df[['WageTax_fed','WageTax_state','WageTax_total']] = tax_df[['WageTax_fed','WageTax_state','WageTax_total']].astype(float)
	tax_df[['LongGains_fed','LongGains_state','LongGains_total']] = tax_df[['LongGains_fed','LongGains_state','LongGains_total']].astype(float)
	tax_df = tax_df[tax_df.year<2014]
	incomeRaw_df = pd.merge(incomeRaw_df, tax_df, left_on=['cofips','year'], right_on=['StateID','year'], how='left')
	incomeRaw_df.drop(['state_name','State_y'],axis=1, inplace=True)
	incomeRaw_df.rename(columns={'State_x':'State'}, inplace=True)

	# trade data
	trade_df = pd.read_excel("../data/DATA_Exports.xlsx", sheetname='real_2009')
	trade_df = pd.melt(trade_df, id_vars=['State'], var_name='year', value_name='exports')
	trade_df['State'] = trade_df['State'].str.title()
	trade_df = trade_df[trade_df.year<2014]
	incomeRaw_df = pd.merge(incomeRaw_df, trade_df, on=['State','year'], how='left')

	# patent data
	patent_df = pd.read_excel("../data/state_patents.xlsx")
	patent_df['State'] = patent_df['State'].str.title()
	patent_df = pd.melt(patent_df, id_vars=['State'], var_name='year', value_name='patents')
	incomeRaw_df = pd.merge(incomeRaw_df, patent_df, on=['State','year'], how='left')

	# gdp by industry (1997 and after)
	gdp_df1 = pd.read_excel("../data/industry_gdp_post1997.xls") #millions of 2009 dollars
	gdp_df1['Industry'] = gdp_df1['Industry'].str.strip()
	gdp_df1.replace(to_replace={'Industry':'Finance, insurance, real estate, rental, and leasing'}, value='fire', inplace=True)
	gdp_df1.replace(to_replace={'Industry':'All industry total'}, value='total', inplace=True)
	gdp_df1 = pd.melt(gdp_df1, id_vars=['Area','Fips','IndCode','Industry'], var_name='year',value_name='gdp')
	gdp_df = pd.merge(gdp_df1[gdp_df1.Industry=='total'],gdp_df1[gdp_df1.Industry=='Information'], on=['Area','year'])
	gdp_df = gdp_df.merge(gdp_df1[gdp_df1.Industry=='fire'], on=['Area','year'])
	gdp_df.rename(columns={'gdp_x':'gdp_total','gdp_y':'gdp_info','gdp':'gdp_fire'}, inplace=True)
	gdp_df.drop(['Fips_x','Fips_y','IndCode_x','IndCode_y','IndCode','Industry_x','Industry_y','Industry'], axis=1,inplace=True)

	gdp_df2 = pd.read_excel("../data/industry_gdp_pre1997.xls") #millions of 1997 dollars
	gdp_df2['Industry'] = gdp_df2['Industry'].str.strip()
	gdp_df2.replace(to_replace={'Industry':'Finance, insurance, and real estate'}, value='fire', inplace=True)
	gdp_df2.replace(to_replace={'Industry':'All industry total'}, value='total', inplace=True)
	gdp_df2 = pd.melt(gdp_df2, id_vars=['Area','Fips','IndCode','Industry'], var_name='year',value_name='gdp')
	gdp_df2 = gdp_df2[gdp_df2.gdp!='(NA)']

	# put it all in 2009 dollars
	gdp_df2.gdp = gdp_df2.gdp.values.astype(float)*1.34
	gdp_df3 = pd.merge(gdp_df2[gdp_df2.Industry=='total'], gdp_df2[gdp_df2.Industry=='fire'], on=['Area','year'])
	gdp_df3.rename(columns={'gdp_x':'gdp_total','gdp_y':'gdp_fire','Fips_x':'Fips'}, inplace=True)
	gdp_df3.drop(['IndCode_x','Industry_x','IndCode_y','Industry_y','Fips_y'], axis=1, inplace=True)
	gdp_df = gdp_df3.append(gdp_df)
	gdp_df['Fips'] = gdp_df['Fips'].astype(str).str[:-3]
	gdp_df.loc[gdp_df['Area']=='United States','Fips']=0
	gdp_df[['Fips','year']] = gdp_df[['Fips','year']].astype(int)
	gdp_df['gdp_info_pct'] = gdp_df['gdp_info']/gdp_df['gdp_total']
	gdp_df['gdp_fire_pct'] = gdp_df['gdp_fire']/gdp_df['gdp_total']
	gdp_df.rename(columns={'Fips':'cofips'}, inplace=True)

	# education data
	edu_df = pd.read_excel("../data/Frank_Education_2015.xlsx", sheetname='Data')
	edu_df.replace('.', np.nan, inplace=True)
	edu_df[['College','HighSchool']] = edu_df[['College','HighSchool']].astype(float)
	income_df = pd.merge(incomeRaw_df, edu_df, on=['cofips','year'])
	income_df.drop(['StateID'], axis=1, inplace=True)

	# data indicating economic regions (clustering of standard errors - maybe)
	regions_df = pd.read_excel("../data/census_regions.xlsx")
	regions_df.drop_duplicates(inplace=True)
	income_df = pd.merge(income_df, regions_df, left_on=['State_x'], right_on=['NAME'])
	income_df.drop(['cofips','State_x','State_y'], axis=1, inplace=True)

	# change from the Mark Frank's cofips convention to the census convention
	income_df.rename(columns={'STATE':'cofips'}, inplace=True)

	# kauffman data on entrepreneurship
	startup_df = pd.read_excel("../data/startup_history_by_state.xlsx",sheetname='Data_State')
	df = pd.merge(income_df, startup_df, on=['cofips','year'])

	# merge gdp data
	df = pd.merge(df, gdp_df, left_on=['cofips','year'], right_on=['cofips','year'], how='left')

	#----------------------------------------------
	# merge with demographic variables
	#----------------------------------------------
	df = df.merge(age_df, left_on=['cofips','year'], right_on=['fips','year'])
	df['patents_percapita'] = df['patents']/(df['total_population']/100000)
	df.sort_values(by=['cofips','year'], inplace=True)


	#-------------------------------------------------
	# economic variables (share of employment in FIRE)
	#-------------------------------------------------
	fire_df = pd.read_excel("../data/FIRE_gdp_by_state.xls")
	fire_df = pd.melt(fire_df, id_vars=['GeoFips','GeoName'],var_name='year', value_name='fire_employment')

	fi_df = pd.read_excel("../data/FI_gdp_by_state.xls")
	fi_df = pd.melt(fi_df, id_vars=['GeoFips','GeoName'],var_name='year', value_name='fi_employment')

	re_df = pd.read_excel("../data/RE_gdp_by_state.xls")
	re_df = pd.melt(re_df, id_vars=['GeoFips','GeoName'],var_name='year', value_name='re_employment')

	fire_df2 = pd.merge(fi_df,re_df, on=['GeoFips','year'])
	fire_df2['fire_employment2'] = fire_df2[['re_employment','fi_employment']].sum(axis=1)
	fire_df = pd.merge(fire_df, fire_df2, how='outer', on=['GeoFips','year'])
	fire_df['fire'] = fire_df[['fire_employment','fire_employment2']].sum(axis=1)
	fire_df = fire_df[['GeoFips','year','fire']]

	emp_df = pd.read_excel("../data/state_employment_total.xls")
	emp_df = pd.melt(emp_df, id_vars=['GeoFips','GeoName'],var_name='year', value_name='total_employment')
	emp_df = pd.merge(emp_df, fire_df, on=['GeoFips','year'])

	emp_df = emp_df[emp_df['GeoFips']!=0]
	emp_df['GeoFips'] = emp_df['GeoFips'].astype(str)
	emp_df['cofips'] = emp_df['GeoFips'].str[:-3].astype(int)
	emp_df['year'] = emp_df['year'].astype(int)
	emp_df['fire_pct'] = emp_df['fire']/emp_df['total_employment']


	df = df.merge(emp_df, on=['cofips','year'])
	df.sort_values(by=['cofips','year'], inplace=True)
	df['exp_pct'] = df['exports']/(df['gdp_total']*1000000)

	# export data to stata, drops duplicates
	df.drop_duplicates(inplace=True)
	export_df(df)

	# # ----------------------------------------------------------------------------
	# # make map DataFrame
	# # ----------------------------------------------------------------------------
	# US_geo = geo.GeoDataFrame.from_file('../data/US_map/cb_2015_us_state_500k.shp')
	# US_geo['STATEFP'] = US_geo.STATEFP.astype(int)
	# US_geo['change_inc90'] = 0
	# US_geo['change_gini'] = 0
	# US_geo['change_theil'] = 0
	# US_geo['change_atkin'] = 0
	# US_geo['change_rmeandev'] = 0
	# US_geo['change_eduHigh'] = 0
	# US_geo['change_eduCollege'] = 0
	# US_geo['change_RetireAge'] = 0
	# US_geo['change_DepRatio'] = 0
	# US_geo['change_population'] = 0
	# US_geo['change_FirePct'] = 0
	# US_geo['change_entrepreneur'] = 0
	# US_geo['change_tax'] = 0
	# US_geo['in_map'] = 0

	# # ----------------------------------------------------------------------------
	# # make some figures
	# # ----------------------------------------------------------------------------
	# inc_df = income_df[income_df.year>1969]
	# edu_df = edu_df[(edu_df.year>1969) & (edu_df.year<2014)]
	# age_df = age_df[age_df.year<2014]
	# emp_df = emp_df[(emp_df.year>1969) & (emp_df.year<2014)]
	# startup_df = startup_df[startup_df.year<2014]

	# fip_id_list = [0] + list(df.cofips.unique())
	# for fip_id in fip_id_list:

	# 	# plot a figure for each state
	# 	state_df = inc_df[inc_df.cofips==fip_id].set_index('year')
	# 	location = state_df.NAME.values[0]

	# 	# speghetti plot for top 10% income share
	# 	xlabel = ' '
	# 	ylabel = 'Percent'
	# 	column = 'Top10_adj'
	# 	filename = '../figures/inc_inequality/'+location.replace(' ','')+'_Inc10_timeline.pdf'
	# 	title = location+': top 10% income share 1970-2013'
	# 	ylim = (15,65)
	# 	make_spaghetti_plot(state_df, inc_df, column, filename, title, xlabel, ylabel, ylim )

	# 	# speghetti plot for top 1% income share
	# 	column = 'Top1_adj'
	# 	filename = '../figures/inc_inequality/'+location.replace(' ','')+'_Inc1_timeline.pdf'
	# 	title = location+': top 1% income share 1970-2013'
	# 	ylim = (1,40)
	# 	make_spaghetti_plot(state_df, inc_df, column, filename, title, xlabel, ylabel, ylim )

	# 	# speghetti plot for gini coefficients
	# 	column = 'Gini'
	# 	ylabel = 'Gini Coefficient'
	# 	filename = '../figures/inc_inequality/'+location.replace(' ','')+'_Gini_timeline.pdf'
	# 	title = location+': Gini Coefficient 1970-2013'
	# 	ylim = (.3,.8)
	# 	make_spaghetti_plot(state_df, inc_df, column, filename, title, xlabel, ylabel, ylim )

	# 	# speghetti plot for Atkin05 index
	# 	column = 'Atkin05'
	# 	ylabel = 'Atkinson Index'
	# 	filename = '../figures/inc_inequality/'+location.replace(' ','')+'_Atkin_timeline.pdf'
	# 	title = location+': Atkin05 index 1970-2013'
	# 	ylim = (.1,.5)
	# 	make_spaghetti_plot(state_df, inc_df, column, filename, title, xlabel, ylabel, ylim )

	# 	# speghetti plot for RMeanDev
	# 	column = 'RMeanDev'
	# 	ylabel = 'Rmean Dev'
	# 	filename = '../figures/inc_inequality/'+location.replace(' ','')+'_RmeanDev_timeline.pdf'
	# 	title = location+': RmeanDev 1970-2013'
	# 	ylim = (.5,1.1)
	# 	make_spaghetti_plot(state_df, inc_df, column, filename, title, xlabel, ylabel, ylim )

	# 	# speghetti plot for Theil Index
	# 	column = 'Theil'
	# 	ylabel = 'Theil Entropy Index'
	# 	filename = '../figures/inc_inequality/'+location.replace(' ','')+'_Theil_timeline.pdf'
	# 	title = location+': Theil Index 1970-2013'
	# 	ylim = (.2,1.2)
	# 	make_spaghetti_plot(state_df, inc_df, column, filename, title, xlabel, ylabel, ylim )

	# 	# speghetti plot for share of pop. with college education
	# 	column = 'College'
	# 	ylabel = 'Percent of pop.'
	# 	filename = '../figures/education/'+location.replace(' ','')+'_edu_timeline.pdf'
	# 	title = location+': share of population with college education'
	# 	ylim = (0,.4)
	# 	make_spaghetti_plot(state_df, inc_df, column, filename, title, xlabel, ylabel, ylim )

	# 	# speghetti plot for FIRE gdp
	# 	xlabel = ' '
	# 	ylabel = 'Percent'
	# 	column = 'gdp_fire_pct'
	# 	filename = '../figures/fire/'+location.replace(' ','')+'_fire_gdp_timeline.pdf'
	# 	title = location+': Employment in FIRE (pct) 1970-2013'
	# 	ylim = (0,.60)
	# 	small_df = gdp_df[gdp_df.cofips==fip_id].set_index('year')
	# 	make_spaghetti_plot(small_df, gdp_df, column, filename, title, xlabel, ylabel, ylim )

	# 	if fip_id != 0:

	# 		# speghetti plot for FIRE employment
	# 		xlabel = ' '
	# 		ylabel = 'Percent'
	# 		column = 'fire_pct'
	# 		filename = '../figures/fire/'+location.replace(' ','')+'_fire_emp_timeline.pdf'
	# 		title = location+': GDP in FIRE (pct) 1970-2013'
	# 		ylim = (0,.2)
	# 		small_df = emp_df[emp_df.cofips==fip_id].set_index('year')
	# 		make_spaghetti_plot(small_df, emp_df, column, filename, title, xlabel, ylabel, ylim )

	# 		# speghetti plot for maximum tax rates
	# 		ylabel = 'Percent'
	# 		column = 'WageTax_state'
	# 		filename = '../figures/tax_rates/'+location.replace(' ','')+'_MaxTaxRate_timeline.pdf'
	# 		title = location+': Maximum Income Tax Rates '
	# 		ylim = (0,22)
	# 		small_df = df[df.cofips==fip_id].set_index('year')
	# 		make_spaghetti_plot(small_df, df, column, filename, title, xlabel, ylabel, ylim )

	# 		# speghetti plot for patents per capita
	# 		column = 'patents_percapita'
	# 		filename = '../figures/patents/'+location.replace(' ','')+'_patents_timeline.pdf'
	# 		title = location+': new patents per 100k people'
	# 		ylim = (0,140)
	# 		make_spaghetti_plot(small_df, df, column, filename, title, xlabel, ylabel, ylim )

	# 		# speghetti plot for dependancy ratio
	# 		xlabel = 'Year'
	# 		ylabel = 'Percent'
	# 		column = 'dep_ratio'
	# 		filename = '../figures/dep_ratio/'+location.replace(' ','')+'_timeline.pdf'
	# 		title = location+': dependancy ratio 1970-2013'
	# 		ylim = (.4,.9)
	# 		small_df = df[df.cofips==fip_id].set_index('year')
	# 		make_spaghetti_plot(small_df, df, column, filename, title, xlabel, ylabel, ylim )

	# 		# speghetti plot for exports as a share of GDP
	# 		xlabel = 'Year'
	# 		ylabel = 'Percent'
	# 		column = 'exp_pct'
	# 		filename = '../figures/exports/'+location.replace(' ','')+'_timeline.pdf'
	# 		title = location+': dependancy ratio 1970-2013'
	# 		ylim = (0,.3)
	# 		small_df = df[df.cofips==fip_id].set_index('year')
	# 		make_spaghetti_plot(small_df, df, column, filename, title, xlabel, ylabel, ylim )

	# 		# speghetti plot for retired population
	# 		xlabel = 'Year'
	# 		ylabel = 'Percent'
	# 		column = 'pct_retired'
	# 		filename = '../figures/retirees/'+location.replace(' ','')+'_timeline.pdf'
	# 		title = location+': dependancy ratio 1970-2013'
	# 		ylim = (0,.25)
	# 		small_df = df[df.cofips==fip_id].set_index('year')
	# 		make_spaghetti_plot(small_df, df, column, filename, title, xlabel, ylabel, ylim )

	# 		# speghetti plot for black population
	# 		xlabel = 'Year'
	# 		ylabel = 'Percent'
	# 		column = 'pct_black'
	# 		filename = '../figures/race/'+location.replace(' ','')+'black_timeline.pdf'
	# 		title = location+': dependancy ratio 1970-2013'
	# 		ylim = (0,.6)
	# 		small_df = df[df.cofips==fip_id].set_index('year')
	# 		make_spaghetti_plot(small_df, df, column, filename, title, xlabel, ylabel, ylim )

	# 		# speghetti plot for minority population
	# 		xlabel = 'Year'
	# 		ylabel = 'Percent'
	# 		column = 'pct_minority'
	# 		filename = '../figures/race/'+location.replace(' ','')+'minority_timeline.pdf'
	# 		title = location+': dependancy ratio 1970-2013'
	# 		ylim = (0,.6)
	# 		small_df = df[df.cofips==fip_id].set_index('year')
	# 		make_spaghetti_plot(small_df, df, column, filename, title, xlabel, ylabel, ylim )

	# 		# speghetti plot for entrepreneurship rate
	# 		ylabel = 'Age 0 firms per 100k'
	# 		column = 'Startup Density'
	# 		filename = '../figures/entrep_data/'+location.replace(' ','')+'_startup_density.pdf'
	# 		title = location+': startup density 1977-2014'
	# 		ylim = (60,500)
	# 		small_df = startup_df[startup_df.cofips==fip_id].set_index('year')
	# 		make_spaghetti_plot(small_df, startup_df, column, filename, title, xlabel, ylabel, ylim )

	# 	# extract some data for the map figures, save in map dataframe
	# 	inc_data = state_df.Top10_adj.values
	# 	gini_data = state_df.Gini.values
	# 	theil_data = state_df.Theil.values
	# 	atkin_data = state_df.Atkin05.values
	# 	RmeanDev_data = state_df.RMeanDev.values

	# 	highschool_data = state_df.HighSchool.values
	# 	college_data = state_df.College.values
	# 	retire_data = age_df[age_df.fips==fip_id].pct_retired.values
	# 	dep_ratio_data = age_df[age_df.fips==fip_id].dep_ratio.values
	# 	pop_data = age_df[age_df.fips==fip_id].total_population.values
	# 	fire_data = emp_df[emp_df.cofips==fip_id].fire_pct.values
	# 	entrep_data = startup_df[startup_df.cofips==fip_id]['Startup Density'].values[:-1]
	# 	tax_data = df[df.cofips==fip_id]['WageTax_state'].values

	# 	# put percent changes in map dataframe
	# 	US_geo.loc[US_geo.NAME ==location, 'change_inc90'] = (inc_data[-5:].mean() - inc_data[:5].mean())/inc_data[:5].mean()
	# 	US_geo.loc[US_geo.NAME ==location, 'change_gini'] = (gini_data[-5:].mean() - gini_data[:5].mean())/gini_data[:5].mean()
	# 	US_geo.loc[US_geo.NAME ==location, 'change_theil'] = (theil_data[-5:].mean() - theil_data[:5].mean())/theil_data[:5].mean()
	# 	US_geo.loc[US_geo.NAME ==location, 'change_atkin'] = (atkin_data[-5:].mean() - atkin_data[:5].mean())/atkin_data[:5].mean()
	# 	US_geo.loc[US_geo.NAME ==location, 'change_rmeandev'] = (RmeanDev_data[-5:].mean() - RmeanDev_data[:5].mean())/RmeanDev_data[:5].mean()

	# 	US_geo.loc[US_geo.NAME ==location, 'change_eduHigh'] = (highschool_data[-5:].mean() - highschool_data[:5].mean())/highschool_data[:5].mean()
	# 	US_geo.loc[US_geo.NAME ==location, 'change_eduCollege'] = (college_data[-5:].mean() - college_data[:5].mean())/college_data[:5].mean()
	# 	US_geo.loc[US_geo.NAME ==location, 'change_RetireAge'] = (retire_data[-5:].mean() - retire_data[:5].mean())/retire_data[:5].mean()
	# 	US_geo.loc[US_geo.NAME ==location, 'change_DepRatio'] = (dep_ratio_data[-5:].mean() - dep_ratio_data[:5].mean())/dep_ratio_data[:5].mean()
	# 	US_geo.loc[US_geo.NAME ==location, 'change_population'] = (pop_data[-5:].mean() - pop_data[:5].mean())/pop_data[:5].mean()
	# 	US_geo.loc[US_geo.NAME ==location, 'change_FirePct'] = (fire_data[-5:].mean() - fire_data[:5].mean())
	# 	US_geo.loc[US_geo.NAME ==location, 'change_entrepreneur'] = (entrep_data[-5:].mean() - entrep_data[:5].mean())
	# 	US_geo.loc[US_geo.NAME ==location, 'change_tax'] = (tax_data[-5:].mean() - tax_data[:5].mean())
	# 	US_geo.loc[US_geo.NAME ==location, 'in_map'] +=1

	# #---------------------------------------------------------------------------------
	# # make map of changes in inequality
	# #---------------------------------------------------------------------------------
	# title = 'Change in Income Inequality: 1970-1975 to 2008-2013'
	# ylabel = 'Percent Change'
	# column = 'change_inc90'
	# make_USmap(US_geo, column, '../figures/maps/inc10_map.pdf', title, ylabel)

	# #---------------------------------------------------------------------------------
	# # make map of changes in inequality
	# #---------------------------------------------------------------------------------
	# title = 'Change in Income Inequality: 1970-1975 to 2008-2013'
	# ylabel = 'Percent Change'
	# column = 'change_gini'
	# make_USmap(US_geo, column, '../figures/maps/gini_map.pdf', title, ylabel)

	# #---------------------------------------------------------------------------------
	# # make map of changes in inequality
	# #---------------------------------------------------------------------------------
	# title = 'Change in Income Inequality: 1970-1975 to 2008-2013'
	# ylabel = 'Percent Change'
	# column = 'change_theil'
	# make_USmap(US_geo, column, '../figures/maps/theil_map.pdf', title, ylabel)

	# #---------------------------------------------------------------------------------
	# # make map of changes in inequality
	# #---------------------------------------------------------------------------------
	# title = 'Change in Income Inequality: 1970-1975 to 2008-2013'
	# ylabel = 'Percent Change'
	# column = 'change_atkin'
	# make_USmap(US_geo, column, '../figures/maps/atkin_map.pdf', title, ylabel)

	# #---------------------------------------------------------------------------------
	# # make map of changes in inequality
	# #---------------------------------------------------------------------------------
	# title = 'Change in Income Inequality: 1970-1975 to 2008-2013'
	# ylabel = 'Percent Change'
	# column = 'change_rmeandev'
	# make_USmap(US_geo, column, '../figures/maps/rmeandev_map.pdf', title, ylabel)

	# #---------------------------------------------------------------------------------
	# # make map of changes in high school education rate
	# #---------------------------------------------------------------------------------
	# title = 'Change in High School Education Rate: 1970-1975 to 2008-2013'
	# ylabel = 'Percent Change'
	# column = 'change_eduHigh'
	# make_USmap(US_geo, column, '../figures/maps/highschool_map.pdf', title, ylabel)

	# #---------------------------------------------------------------------------------
	# # make map of changes in college education rate
	# #---------------------------------------------------------------------------------
	# title = 'Change in College Education Rate: 1970-1975 to 2008-2013'
	# ylabel = 'Percent Change'
	# column = 'change_eduCollege'
	# make_USmap(US_geo, column, '../figures/maps/college_map.pdf', title, ylabel)

	# #---------------------------------------------------------------------------------
	# # make map of changes in retirement age share of population
	# #---------------------------------------------------------------------------------
	# title = 'Change in Dependency Ratio of Population: 1970-1975 to 2008-2013'
	# ylabel = 'Percent Change'
	# column = 'change_RetireAge'
	# make_USmap(US_geo, column, '../figures/maps/retire_map.pdf', title, ylabel)

	# #---------------------------------------------------------------------------------
	# # make map of changes in retirement age share of population
	# #---------------------------------------------------------------------------------
	# title = 'Change in Population: 1970-1975 to 2008-2013'
	# ylabel = 'Percent Change'
	# column = 'change_population'
	# make_USmap(US_geo, column, '../figures/maps/population_map.pdf', title, ylabel)

	# #---------------------------------------------------------------------------------
	# # make map of changes in retirement age share of population
	# #---------------------------------------------------------------------------------
	# title = 'Change in FIRE Employment (pct of total): 1970-1975 to 2008-2013'
	# ylabel = 'Percent Change'
	# column = 'change_FirePct'
	# make_USmap(US_geo, column, '../figures/maps/fire_map.pdf', title, ylabel)

	# #---------------------------------------------------------------------------------
	# # make map of changes in entrepreneurship rates
	# #---------------------------------------------------------------------------------
	# title = 'Change in Startup Density: 1977-1982 to 2007-2012'
	# ylabel = 'Percent Change'
	# column = 'change_entrepreneur'
	# make_USmap(US_geo, column, '../figures/maps/startupdensity_map.pdf', title, ylabel)

	# #---------------------------------------------------------------------------------
	# # make map of changes in maximum tax rates
	# #---------------------------------------------------------------------------------
	# title = 'Change in Maximum Tax Rates: 1977-1982 to 2007-2012'
	# ylabel = 'Absolute Change (levels)'
	# column = 'change_tax'
	# make_USmap(US_geo, column, '../figures/maps/tax_map.pdf', title, ylabel)

	# #---------------------------------------------------------------------------------
	# # scatterplot of change in inequality against change in share of elderly
	# #---------------------------------------------------------------------------------
	# xlabel = 'Change in Share of Retired Population'
	# ylabel = 'Change in Income Inequality'
	# filename = '../figures/scatterplots/retire_v_ineq.pdf'
	# make_US_scatter(US_geo, 'change_RetireAge', 'change_inc90', filename, xlabel, ylabel)

	# xlabel = 'Change in Share of Population with College Degrees'
	# filename = '../figures/scatterplots/college_v_ineq.pdf'
	# make_US_scatter(US_geo, 'change_eduCollege', 'change_inc90', filename, xlabel, ylabel)

	# xlabel = 'Change in Share of Population with High School Diplomas'
	# filename = '../figures/scatterplots/high_v_ineq.pdf'
	# make_US_scatter(US_geo, 'change_eduHigh', 'change_inc90',  filename, xlabel, ylabel)

	# xlabel = 'Change in Total Population'
	# filename = '../figures/scatterplots/pop_v_ineq.pdf'
	# make_US_scatter(US_geo, 'change_population', 'change_inc90', filename, xlabel, ylabel)

	# xlabel = 'Change in Dependency Ratio'
	# filename = '../figures/scatterplots/depratio_v_ineq.pdf'
	# make_US_scatter(US_geo, 'change_DepRatio', 'change_inc90', filename, xlabel, ylabel)

	# xlabel = 'Change in Entrepreneurship (startup density)'
	# filename = '../figures/scatterplots/depratio_v_ineq.pdf'
	# make_US_scatter(US_geo, 'change_entrepreneur', 'change_inc90', filename, xlabel, ylabel)

	# xlabel = 'Change in Tax Rates'
	# filename = '../figures/scatterplots/taxes_v_ineq.pdf'
	# make_US_scatter(US_geo, 'change_tax', 'change_inc90', filename, xlabel, ylabel)
