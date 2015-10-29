How to run:
- python rtree.py
- change queryfile name, infilename file(sample data file) and outfilename(outfile name) according to the need

========================================================================================================================================

Comparison based on running time:

Most of the time taken by rtree algorithm is mainly on rtree formation.

Time in seconds

			INDEPENDENT			Correlated		  	Anticorrelated
-------------------------------------------------------------------------
BNL	 	|	 0.0476529598236 |	0.0135700702667	|	0.449230194092
SFS		|	0.0945188999176	|  0.0651550292969 |   0.377422094345
RTREE 	|	0.69646692276	|  0.680653095245  |	1.02262210846

So. from comparison Rtree is taking more time but most of that time is spent on implementing the rtree but after that a very less amount of time is required which can be evident from the number of comparisons that are required in the rtree implementation as compared to the other ones.


Number of comparisons

			INDEPENDENT			Correlated		  	Anticorrelated
-------------------------------------------------------------------------
BNL		|	 68944			 |	3181			|	632814
SFS		|	34596			 |  2202 			|   531624
RTREE 	|	18987			 |  257  			|	262619


Final conclusion:

We can conclude that the R-tree is much better than the other two in terms of number of comparisons difference which is very much on comparison.
But the time overhead in order tomake the tree is very much as well in Rtree implementation 