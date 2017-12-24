#!/usr/bin/env python2.7

thesisdir = '/Users/Tom/Documents/Work/PhD/Thesis/latest/'

from glob import glob
import os, sys
from subprocess import check_output
from datetime import datetime 

def main():
    filelist = glob(thesisdir+'/text/*.tex')

    excluded = ["abstract", 
                "dedication", 
                "originalityselection",
                "title",
                "acknowledgements", 
                "lhcb-symbols-def",
                "preamble",
                ]    

    totnum = 0


    currtime = datetime.now()

    string = currtime.strftime("%Y.%m.%d %H:%M:%S")
    print('The current time is', string)
    wordcountfile = open(thesisdir+"/monitoring/wordcount.txt","a")
    wordcountfile.write(string)

    totalwordcountfile = open(thesisdir+"/monitoring/wordcount_Tom.txt","a")
    totalwordcountfile.write(string)

    for file in filelist:
        num = 0 

        # Check name is not in excluded 
        name = file.split('/')[-1].split('.tex')[0].lower()
        if name in excluded: continue

        # Check for a sub-dir 
        #print( name.lower(), dirs)
        # if name.lower() in dirs:
        #     print('\tFound a directory with the same name as a .tex file. Delving in')
        #     print('\tFile {0}, directory {1}'.format(file, name))
        #     # do a mini sum of the sub-files
        #     subfolder = thesisdir+name+'/*.tex'.lower()
        #     print('\tSearching: '+subfolder)
        #     subfilelist = glob(subfolder)
        #     print('\tFound files: {0}'.format([x.split('/')[-1] for x in subfilelist]))
        #     for subfile in subfilelist:
        #         num += do_count(subfile)
                

        # else:
        
        num = do_count(file)


        print(name+":", num)

        wordcountfile.write(" "+name+" "+str(num))

        totnum += num

    pdftotnum = int(check_output(['./get_pdf_wordcount.sh','']))

    bonusnum = pdftotnum - totnum
    wordcountfile.write(" bonus "+str(bonusnum))
    print "bonus:", bonusnum
    totnum += bonusnum

    wordcountfile.write(" total "+str(totnum)+"\n")
    wordcountfile.close()

    totalwordcountfile.write(" "+str(totnum)+"\n")
    totalwordcountfile.close()

    print "total:", totnum

def do_count(file):
    print "do_count",file
    #try: output = check_output(('wc -w '+file).split())
    #except:
        #print("problem doing wordcount for", name)
        #continue
    output = check_output(('wc -w '+file).split())
    print "output:", output

    #try: num = int(output.split()[0])
    #except:
        #print(output, "can't be converted to int")
    num = int(output.split()[0])
    print "num:", num

    return num

if __name__ == "__main__":
    main()