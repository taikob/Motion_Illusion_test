import csv, os

def save_list(list, fname,md=None):
    if md==None:
        if os.path.isfile(fname):
            mode='a'
        else:
            mode='w'
    else: mode=md
    n=0
    fname=fname
    with open(fname, mode=mode) as tt:
        while n < len(list):
            tt.write(','.join([ str(x) for x in list[n]]) + '\n')
            n+=1

def load_list(fname):
    with open(fname) as f:
        reader = csv.reader(f)
        data = [row for row in reader]
    return data