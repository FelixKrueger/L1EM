import sys
import cPickle as pickle

exp_prob_pkls_list = sys.argv[1]
bam_info_list = sys.argv[2]

exp_probs = dict()
seqs = set([])

for line in open(exp_prob_pkls_list):
	names_file, X_file = line.strip().split('\t')
	name = names_file.split('/')[-1][:-16]
	exp_probs[name] = dict(zip(pickle.load(open(names_file)),pickle.load(open(X_file))))
	seqs = seqs | set(exp_probs[name].keys())

l1pa_pairs = dict()
mapped_pairs = dict()

for line in open(bam_info_list):
	name = line.strip().split('/')[-1][:-4]
	baminfo = open(line.strip()).readlines()
	mapped_pairs[name] = int(baminfo[1])
	l1pa_pairs[name] = int(baminfo[2])

print_string = "locus"
for name in exp_probs:
	print_string += "\t"+name+'-active'+"\t"+name+'-passive'

print(print_string)

completed = set()

for name in seqs:
	if name.split('.')[0] not in ['L1HS','L1PA2','L1PA3','L1PA4']:
		continue
	seq_name = '_'.join(name.split('_')[:-1])
	if seq_name in completed:
		continue
	else:
		completed.add(seq_name)
	print_string = seq_name.split('(')[0]
	only_name = seq_name+'_only'
	runon_name = seq_name+'_3prunon'
	runthrough_name = seq_name+'_runthrough'
	for name in exp_probs:
		FPM = 0.0
		runthrough_FPM = 0.0
		if only_name in exp_probs[name]:
			FPM += exp_probs[name][only_name]*l1pa_pairs[name]/mapped_pairs[name]*10**6
		if runon_name in exp_probs[name]:
			FPM += exp_probs[name][runon_name]*l1pa_pairs[name]/mapped_pairs[name]*10**6
		if runthrough_name in exp_probs[name]:
			runthrough_FPM += exp_probs[name][runthrough_name]*l1pa_pairs[name]/mapped_pairs[name]*10**6
		print_string += '\t'+str(FPM)+'\t'+str(runthrough_FPM)
	print(print_string)
