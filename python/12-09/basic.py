import sys
def print_n_times(values,n=2,end='\n',sep=' ',file=sys.stdout,flush=False):
    for i in range(n):
        print(values)

print_n_times("안녕하세요")
