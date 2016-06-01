import scraperwiki, urllib2
import lxml
import re
import sys

u=urllib2.urlopen("http://pilbaraports.com.au/Shipping_Schedule/Current_Shipping_Schedule.pdf")
 
x=scraperwiki.pdftoxml(u.read())
# Get Schedule Date
Schedule_Date = re.search(r'jpg((.|\n)+)</text>', x).group(0)
Schedule_Date = re.search(r'<b>(.*?)</b>', Schedule_Date).group(0).replace('<b>', '').replace('</b>', '').strip(' ')
print Schedule_Date

# Scan PDF
test1 = re.search(r'Duty Helo:((.|\n)+)TIDES', x).group(0)
#print test1

tuples = re.findall(r'((left="|">)(.*?)(</text>|"))', test1.replace('<b>', '').replace('</b>', ''))
#cnt=0
#obj = ''
#row=''
lineout=''
#headers=1
headerrow=1
runcnt=1
#hdcnt=0
#HeadersList = []
recflag = 0
prevloc = 0
#alignment=0
#vesselflag=1
colcnt=0
ColList = [0, 1.26,1.14,1.12,1.12,1.08,1.13,1.1,1.09,1.08,1.07,1.04,1.05];

for tuple in tuples:
 
  print runcnt

  if headerrow==0:
   if (runcnt % 2) == 0:
   # ojb
     obj = tuple[2].strip(' ').replace(',', '')
     recflag = 1
   else:
   # loc   
     loc = int(tuple[2].strip(' '))
     recflag = 0
  
  elif runcnt==14:
    headerrow=1
  
  
  # Record the Object
  if recflag == 1:
    if prevloc == 0:
      lineout = lineout + obj + ','
      colcnt=colcnt+1
      prevloc=loc
    else:
      if loc/prevloc >= ColList[colcnt]+.01 and loc/prevloc <= ColList[colcnt]-.01:
        lineout = lineout + obj + ','
        colcnt=colcnt+1
        prevloc=loc
  
    if colcnt == 14: 
      print lineout[:-1]
      colcnt=0
      prevloc=0
      runcnt=0

  runcnt=runcnt+1

