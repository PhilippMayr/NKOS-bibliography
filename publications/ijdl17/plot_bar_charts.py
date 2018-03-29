### plot bar charts ####

import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import sys
import operator

fileIn = sys.argv[1]
#fileOut = sys.argv[2]

degree_dict = {}
btw_dict = {}
closeness_dict = {}
effsize_dict = {}

with open(fileIn) as f:
	next(f)
	for line in f:
		line = line.strip()
		print line
		name,degree,btw_cent,closeness_cent,effective_size = line.split(',')
		degree_dict[name] = int(degree)
		btw_dict[name] = float(btw_cent)
		closeness_dict[name] = float(closeness_cent)
		effsize_dict[name] = float(effective_size)

sorted_deg = sorted(degree_dict.items(), key=operator.itemgetter(1))
sorted_btw = sorted(btw_dict.items(), key=operator.itemgetter(1))
sorted_closeness = sorted(closeness_dict.items(), key=operator.itemgetter(1))
sorted_effsize = sorted(effsize_dict.items(), key=operator.itemgetter(1))
# show top 15 degree
############################################ plot degree #################################
x_list = []
y_list = []
for name,v in sorted_deg[-15:]:
	print name, v
	x_list.append(name)
	y_list.append(v)


fig, ax = plt.subplots()    
#objects = ('Python', 'C++', 'Java', 'Perl', 'Scala', 'Lisp')
y_pos = np.arange(len(x_list))
#performance = [10,8,6,4,2,1]
ind = np.arange(len(y_list))

width = 0.7


ax.barh(y_pos, y_list, width,align='center', alpha=0.5 )
ax.set_yticks(y_pos, x_list)
ax.set_yticks(ind+width/10)
ax.set_yticklabels(x_list,minor=False)
plt.xlabel('Degree')
#plt.title('Programming language usage')

# Hide the right and top spines
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

for i, v in enumerate(y_list):
    ax.text(v + 1 , i , str(v), color='black')

plt.tick_params(top='off', bottom='off', left='off', right='off', labelleft='on', labelbottom='on')

plt.savefig('degree.pdf' , bbox_inches='tight')
#plt.show()
plt.close()
############################################ plot btw #################################

x_list = []
y_list = []
for name,v in sorted_btw[-15:]:
	print name, v
	x_list.append(name)
	y_list.append('%.4f'%v)


fig, ax = plt.subplots()    
#objects = ('Python', 'C++', 'Java', 'Perl', 'Scala', 'Lisp')
y_pos = np.arange(len(x_list))
#performance = [10,8,6,4,2,1]
ind = np.arange(len(y_list))

width = 0.7


ax.barh(y_pos, y_list, width,align='center', alpha=0.5 )
ax.set_yticks(y_pos, x_list)
ax.set_yticks(ind+width/10)
ax.set_yticklabels(x_list,minor=False)
plt.xlabel('Betweenness centrality')
#plt.title('Programming language usage')

# Hide the right and top spines
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

for i, v in enumerate(y_list):
    ax.text(v   , i , str(v), color='black')

plt.tick_params(top='off', bottom='off', left='off', right='off', labelleft='on', labelbottom='on')

plt.savefig('betweenness.pdf' , bbox_inches='tight')
plt.close()

############################################ plot closeness #################################


x_list = []
y_list = []
for name,v in sorted_closeness[-15:]:
	print name, v
	x_list.append(name)
	y_list.append('%.4f'%v)


fig, ax = plt.subplots()    
#objects = ('Python', 'C++', 'Java', 'Perl', 'Scala', 'Lisp')
y_pos = np.arange(len(x_list))
#performance = [10,8,6,4,2,1]
ind = np.arange(len(y_list))

width = 0.7


ax.barh(y_pos, y_list, width,align='center', alpha=0.5 )
ax.set_yticks(y_pos, x_list)
ax.set_yticks(ind+width/10)
ax.set_yticklabels(x_list,minor=False)
plt.xlabel('Closeness centrality')
#plt.title('Programming language usage')

# Hide the right and top spines
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

for i, v in enumerate(y_list):
    ax.text(v  , i , str(v), color='black')

plt.tick_params(top='off', bottom='off', left='off', right='off', labelleft='on', labelbottom='on')

plt.savefig('closeness.pdf' , bbox_inches='tight')
plt.close()

############################################ plot effective size #################################


x_list = []
y_list = []
for name,v in sorted_effsize[-15:]:
	print name, v
	x_list.append(name)
	y_list.append(v)


fig, ax = plt.subplots()    
#objects = ('Python', 'C++', 'Java', 'Perl', 'Scala', 'Lisp')
y_pos = np.arange(len(x_list))
#performance = [10,8,6,4,2,1]
ind = np.arange(len(y_list))

width = 0.7


ax.barh(y_pos, y_list, width,align='center', alpha=0.5 )
ax.set_yticks(y_pos, x_list)
ax.set_yticks(ind+width/10)
ax.set_yticklabels(x_list,minor=False)
plt.xlabel('Effective size')
#plt.title('Programming language usage')

# Hide the right and top spines
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

for i, v in enumerate(y_list):
    ax.text(v + 1 , i , str(v), color='black')

plt.tick_params(top='off', bottom='off', left='off', right='off', labelleft='on', labelbottom='on')

plt.savefig('effective_size.pdf' , bbox_inches='tight')
plt.close()


