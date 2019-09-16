import cPickle as pickle
import sys

"""
Extract the LINE-1 transcript estimates from L1EM. This version is intended for use on CGC
to analyze TCGA data.

Copyright (C) 2019 Wilson McKerrow

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""

X_est = dict(zip(pickle.load(open(sys.argv[1])),pickle.load(open(sys.argv[2]))))

proper_pairs_in_original_bam = float(sys.argv[3])

total = float(sys.argv[4])

written_seqs = set([])

print "family.category.locus.strand\tonly\t3prunon"

names = X_est.keys()

for name in names:
	if 'L1HS' in name:
		seq_name = '_'.join(name.split('_')[:-1])
		if seq_name in written_seqs:
			continue
		written_seqs.add(seq_name)
		print_string = seq_name.split('(')[0]
		only_name = seq_name+'_only'
		if only_name not in X_est:
			X_est[only_name]=0.0
		only_pairs = total*X_est[only_name]
		runon_name = seq_name+'_3prunon'		
		if runon_name not in X_est:
			X_est[runon_name]=0.0
		runon_pairs = total*X_est[runon_name]
		runthroughS_name = seq_name+'_senserunthrough'
		if runthroughS_name not in X_est:
			X_est[runthroughS_name]=0.0
		runthrough_pairs = total*X_est[runthroughS_name]
		runthroughA_name = seq_name+'_antisenserunthrough'
		if runthroughA_name not in X_est:
			X_est[runthroughA_name]=0.0
		runthrough_pairs += total*X_est[runthroughA_name]
		if (only_pairs+runon_pairs > 3*runthrough_pairs) & (only_pairs+runon_pairs>100):
			print seq_name.split('(')[0]+'\t'+str(only_pairs)+'\t'+str(runon_pairs)