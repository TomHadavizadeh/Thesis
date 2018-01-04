#!/usr/bin/env python
"""
Show how to make date plots in matplotlib using date tick locators and
formatters.  See major_minor_demo1.py for more information on
controlling major and minor ticks

All matplotlib date plotting is done by converting date instances into
days since the 0001-01-01 UTC.  The conversion, tick locating and
formatting is done behind the scenes so this is most transparent to
you.  The dates module provides several converter functions date2num
and num2date

"""
import os, sys
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook

years = mdates.YearLocator()   # every year
months = mdates.MonthLocator()  # every month
weeks = mdates.WeekdayLocator()  # every week

yearsFmt = mdates.DateFormatter('%Y')
monthsFmt = mdates.DateFormatter('%m/%y')
daysFmt = mdates.DateFormatter('%d/%m/%y')

# some pretty colours from http://www.randalolson.com/2014/06/28/how-to-make-beautiful-data-visualizations-in-python-with-matplotlib/
tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),    
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),    
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),    
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),    
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]    
  
# Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.    
for i in range(len(tableau20)):    
    r, g, b = tableau20[i]    
    tableau20[i] = (r / 255., g / 255., b / 255.)    


"""
# load a numpy record array from yahoo csv data with fields date,
# open, close, volume, adj_close from the mpl-data/example directory.
# The record array stores python datetime.date as an object array in
# the date column
datafile = cbook.get_sample_data('goog.npy')
try:
    # Python3 cannot load python2 .npy files with datetime(object) arrays
    # unless the encoding is set to bytes. Hovever this option was
    # not added until numpy 1.10 so this example will only work with
    # python 2 or with numpy 1.10 and later.
    r = np.load(datafile, encoding='bytes').view(np.recarray)
except TypeError:
    r = np.load(datafile).view(np.recarray)
"""

thesisdir = '../'
infilename = 'wordcount_willF.txt'
infilename = 'wordcount.txt'
infile = open(infilename,'r')
inlines = infile.readlines()
infile.close()

datetimes = []
entries = []
sections = []

for line in inlines:
    ls = line.rstrip('\n').split()
    date = ls[0]
    time = ls[1]
    datetimeentry = datetime.datetime.strptime(date+'_'+time, '%Y.%m.%d_%H:%M:%S') #2014.12.22 21:59:59
    datetimes.append(datetimeentry)

    tempdict = {}
    itemname = ''
    itemcount = -1
    for item in ls[2:]:

        try:
            itemcount = int(item)
            tempdict[itemname] = itemcount
            itemname = ''
        except:
            itemname = item
            if itemname not in sections: sections.append(itemname)
            itemcount = -1
            
    entries.append(tempdict)

arrays = {}
for sec in sections:
    if 'bonus' in sec: continue
    templist = []
    for d in range(len(entries)):
        templist.append(entries[d][sec])
    arrays[sec] = np.array(templist)


#definitions 77 pmssm 2410 appendix 25 multijets 15 introduction 30 sparticles 173 summary 4 detector 3 acknowledgements 10 glossary 174 preface 82 theory 2 sct 4 bonus
#b2dskk 1090 b2dsphi 226 detector 12 introduction 9 originality 137 selection 3805 theory 15 bonus -1769 total 3525
#orderednames = ('preface', 'glossary', 'introduction', 'theory', 'detector', 'pmssm', 'multijets', 'summary', 'appendix')
orderednames = ('introduction', 'theory', 'detector', 'selection', 'b2dskk', 'b2dsphi','appendix_fitcategories')
orderedarrays = (arrays[sec] for sec in orderednames)

# MAKE SURE THAT ORDEREDNAMES CORRESPONDS TO EVERYTHING IT SHOULD DO (ot just add everything else to 'other')

datetimearray = np.array(datetimes)

x = datetimearray
y = np.row_stack(orderedarrays)


fig, ax = plt.subplots()
stack_coll = ax.stackplot(x, y, colors=tableau20[:len(orderednames)])
# plt.show()

# fig, ax = plt.subplots()
# ax.stackplot(x, orderedarrays[0], orderedarrays[1], orderedarrays[2], orderedarrays[3], orderedarrays[4], orderedarrays[5], orderedarrays[6], 
#                           orderedarrays[7], orderedarrays[8], orderedarrays[9], orderedarrays[10], orderedarrays[11], orderedarrays[12])
# plt.show()


# format the ticks
# ax.xaxis.set_major_locator(years)
# ax.xaxis.set_major_formatter(yearsFmt)
# ax.xaxis.set_minor_locator(months)

# datemin = datetime.date(datetimearray.min().year, 1, 1)
# datemax = datetime.date(datetimearray.max().year + 1, 1, 1)

ax.xaxis.set_major_locator(months)
ax.xaxis.set_major_formatter(monthsFmt)
# ax.xaxis.set_minor_locator(months)

datemin = datetime.date(2017,12,1)
datemax = datetime.date(2018,3,1)

ax.set_xlim(datemin, datemax)

# format the coords message box
# def price(x):
#     return '$%1.2f' % x
ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
# ax.format_ydata = price
ax.grid(True)

# rotates and right aligns the x labels, and moves the bottom of the
# axes up to make room for them
fig.autofmt_xdate()

ax.set_ylabel('Wordcount', fontsize=18)


from matplotlib.patches import Rectangle
proxy_rects = [Rectangle((0, 0), 1, 1, fc=pc.get_facecolor()[0]) for pc in stack_coll]
ax.legend(proxy_rects[::-1], orderednames[::-1])

fig.savefig(infilename.replace('.txt','.pdf'), bbox_inches='tight')
# plt.show()

ax.xaxis.set_major_locator(weeks)
ax.xaxis.set_major_formatter(daysFmt)
datemin = datetime.date(2017,11,22)
datemax = datetime.date(2018,3,31)
ax.set_xlim(datemin, datemax)
#fig.savefig(infilename.replace('.txt','_Dec.pdf'), bbox_inches='tight')

#os.system('scp wordcount_willF.txt '+os.environ['pp8'])
