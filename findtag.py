# -*- coding: utf-8 -*-
"""
reads FASTQ format files of sequences, looks for a specified nucleotide sequence
and finds the following N nucleotides, then lists the unique versions and their
frequency

Created on Thu Dec 31 14:08:55 2015

modified 31 Dec - Jim Lux - check reasonableness and trap some error conditions
@author: jimlux
"""

from operator import itemgetter
import sys 

def findtags(filename,outfile,searchstring,howmany):
    #filename='rawdata2.txt'
    #outfile='sortedtags.csv'
    #searchstring='GGACGAAACACC'
    lensearchstring = len(searchstring)
    #howmany = 20
    results = []
    n=0
    with open(filename,'r') as fp:
        
        for l in fp:
            n=n+1
           
            if (n % 4) == 2:
                #print l        
                f = l.find(searchstring)
                #print f
                if f>0:
                    startidx = f+lensearchstring
                    endidx = startidx + howmany -1
                    if endidx<=len(l):
                        results.append(l[startidx:endidx]) #append it
                    else:
                        print 'sequence found too close to end'
    
    print (str(n)+' lines read, '+str(n/4)+' sequences')
    nn=len(results)
    print (str(nn) + ' matching results found. '+
           str(n/4-nn)+' sequences with no match ('+
           str(100-int(100.0*nn/(n/4.0)))+'%)')
  
    if len(results)<=0:
        print 'no matching results found'
        
    # sort them all and find how many of each sequence there are
    results.sort()
    n=0
    k=0
    lastr =''
    tally=[]
    for r in results:
        if n != 0:
            if r != lastr:
                tally.append( ( lastr,k))
                k=0
                
            k=k+1
        lastr = r
        n=n+1
    
    if len(tally)<1:
        print 'nothing to sort or tally'
    # sort into descending order of frequency
    tallys = sorted(tally,key=itemgetter(1),reverse=True)  
    # dump it to a file
    
    
    fp=open(outfile,'w')
    for item in tallys:
        fp.write(item[0]+','+str(item[1])+'\n')
    fp.close()

if __name__ =="__main__":
   
    if len(sys.argv)<5:
        print "syntax is findtag {inputfile} {outputfile} {sequence to search} {#of characters}"
        print "{inputfile} is the text file in FASTQ format (4 lines per sequence)"
        print "{outputfile} is the name of the file to write the sequences and their frequencies to"
        print "{sequence to search} is the sequence to look for (a series of ACTG, in upper case)"
        print "{#of characters} is the number of characters AFTER the search sequence to record"
    else:
        findtags(sys.argv[1],sys.argv[2],sys.argv[3],int(sys.argv[4]))
        