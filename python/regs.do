#delimit ;
cd "/Users/btengels/Dropbox/Econ/entreprenours/python";

*---------------------------------------------------------------------------- ;* Get data ;use ../data/income_startup_state, clear ;
set matsize 800;


xtset cofips year;

* put variables in logs;
replace inc_ineq1 = log(F1.inc_ineq1);
replace inc_ineq2 = log(F1.inc_ineq2);
replace inc_ineq3 = log(F1.inc_ineq3);
replace ent1 = log(ent1);
replace pct_black = log(pct_black);
replace pct_retired = log(pct_retired);
replace patents_percapita = log(patents_percapita);
replace College = log(College);
replace exp_pct = log(exp_pct);
replace fire_pct = log(fire_pct);
replace dep_ratio = log(dep_ratio);
replace WageTax_total = log(WageTax_total);


************ TOP 10\% income shares ***************************;
* long time series regression (no lags);
xtpmg d.inc_ineq1 d.WageTax_total d.ent1 d.pct_black d.pct_retired d.patents_percapita d.College d.fire_pct, lr(l.inc_ineq1 WageTax_total  ent1 pct_black pct_retired patents_percapita College fire_pct) mg ec("err") replace;
outreg2  using ../tables/top10_benchmark.tex, tex(frag)  nocons replace; 
xtpmg d.inc_ineq1 d.WageTax_total d.ent1 d.pct_black d.pct_retired d.patents_percapita d.College d.fire_pct, lr(l.inc_ineq1 WageTax_total  ent1 pct_black pct_retired patents_percapita College fire_pct) pmg ec("err") replace difficult;
outreg2  using ../tables/top10_benchmark.tex, tex(frag)  nocons append; 
xtpmg d.inc_ineq1 d.WageTax_total d.ent1 d.pct_black d.pct_retired d.patents_percapita d.College d.fire_pct, lr(l.inc_ineq1 WageTax_total  ent1 pct_black pct_retired patents_percapita College fire_pct) dfe ec("err") replace cluster(cofips);
outreg2  using ../tables/top10_benchmark.tex, tex(frag)  nocons append; 



************ TOP 1\% income shares ***************************;
* long time series regression (no lags);
xtpmg d.inc_ineq2 d.WageTax_total d.ent1 d.pct_black d.pct_retired d.patents_percapita d.College d.fire_pct, lr(l.inc_ineq2 WageTax_total  ent1 pct_black pct_retired patents_percapita College fire_pct) mg ec("err") replace;
outreg2  using ../tables/top1_benchmark_Lmix.tex, tex(frag)  nocons replace; 
xtpmg d.inc_ineq2 d.WageTax_total d.ent1 d.pct_black d.pct_retired d.patents_percapita d.College d.fire_pct, lr(l.inc_ineq2 WageTax_total  ent1 pct_black pct_retired patents_percapita College fire_pct) pmg ec("err") replace difficult;
outreg2  using ../tables/top1_benchmark_Lmix.tex, tex(frag)  nocons append; 
xtpmg d.inc_ineq2 d.WageTax_total d.ent1 d.pct_black d.pct_retired d.patents_percapita d.College d.fire_pct, lr(l.inc_ineq2 WageTax_total  ent1 pct_black pct_retired patents_percapita College fire_pct) dfe ec("err") replace cluster(cofips);
outreg2  using ../tables/top1_benchmark.tex, tex(frag)  nocons append; 


************ Gini Coefficients *******************************;
* long time series regression (no lags);
xtpmg d.inc_ineq3 d.WageTax_total d.ent1 d.pct_black d.pct_retired d.patents_percapita d.College d.fire_pct, lr(l.inc_ineq3 WageTax_total  ent1 pct_black pct_retired patents_percapita College fire_pct) mg ec("err") replace;
outreg2  using ../tables/gini_benchmark_Lmix.tex, tex(frag)  nocons replace; 
xtpmg d.inc_ineq3 d.WageTax_total d.ent1 d.pct_black d.pct_retired d.patents_percapita d.College d.fire_pct, lr(l.inc_ineq3 WageTax_total  ent1 pct_black pct_retired patents_percapita College fire_pct) pmg ec("err") replace difficult;
outreg2  using ../tables/gini_benchmark_Lmix.tex, tex(frag)  nocons append; 
xtpmg d.inc_ineq3 d.WageTax_total d.ent1 d.pct_black d.pct_retired d.patents_percapita d.College d.fire_pct, lr(l.inc_ineq3 WageTax_total  ent1 pct_black pct_retired patents_percapita College fire_pct) dfe ec("err") replace cluster(cofips);
outreg2  using ../tables/gini_benchmark.tex, tex(frag)  nocons append; 


