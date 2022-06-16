import os
os.chdir('C:/Users/Jeff/Desktop')

trial = 10
# function to merge groups with repeated entries
def merge(old):

    temp = old
    new = []

    while temp != []:

        union = []
        for group in old:

            if group != temp[0] and list(set(group) & set(temp[0])) != []:
                union = union + group
                temp.remove(group)

        new.append(temp[0] + union)
        temp.remove(temp[0])

    for i,group in enumerate(new): new[i] = list(dict.fromkeys(group))

    return(new)


#### entry matching

# a raw matching
inFile = './table.txt'

all = []

with open(inFile) as f:

    for index,line in enumerate(f):

        a,b = line.strip().split('\t')

        if index == 0:
            all.append([a,b])
            continue

        match = 0
        for d in [a,b]:
            for i,group in enumerate(all):
                if d in group:
                    match = 1
                    break
            if match == 1:
                all[i] = all[i] + [a,b]
                break
        if match == 0: all.append([a,b])


# remove dups
for i,group in enumerate(all): all[i] = list(dict.fromkeys(group))


# a finer matching
t = 0
while t == 0:
    temp = len(all)
    new = merge(all)
    all = new
    if temp == len(new): t = 1


# output matching file

outFile = 'matched.txt'
out = open(outFile, 'w')
for group in all:
    out.write('\t'.join(group) + '\n')
out.close()



#### pick the logest entry for each group

# create length config

configFile = 'table_length.txt'

config = {}

with open(configFile) as f:

    for index,line in enumerate(f):

        entry,length = line.strip().split('\t')
        config[entry] = int(length)

# pick the longest entry in each group

picked = []
others = []

for group in all:

    temp = group
    pick = group[0]
    length = config[group[0]]

    for entry in group:
        if config[entry] > length:
            pick = entry
            length = config[entry]

    picked.append(pick)
    temp.remove(pick)
    others = others + temp

# output picked entries and unpicked entries

outFile = 'picked.txt'
out = open(outFile, 'w')
out.write('\n'.join(picked) + '\n')
out.close()

outFile = 'unpicked.txt'
out = open(outFile, 'w')
out.write('\n'.join(others) + '\n')
out.close()