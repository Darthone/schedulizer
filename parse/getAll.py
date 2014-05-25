import pymongo, urllib2
from BeautifulSoup import BeautifulSoup
from pprint import pprint

baseURL = "https://duapp2.drexel.edu"
classAtt = ['Subject_Code', 'Course_Number', 'Instr_Type', 'Section', 'CRN', 'Course_Title', 'Days', 'Time', 'Instructor' ]

def getTerms():
   response = urllib2.urlopen("https://duapp2.drexel.edu/webtms_du/app")
   htmlSoup = BeautifulSoup(response)
   for div in htmlSoup.findAll('div'):
      if "component=quarterTermDetails" in str(div):
         url = str(div).split(' href="')[1]
         term = (url.split('">')[1]).split('</a')[0].rsplit(' ', 1)[0].replace(' ', '')
         url =  url.split('">')[0].replace('&amp;', '&')
         getColleges(url, term)
    
         
def getColleges(url, term):
   response = urllib2.urlopen(baseURL + url)
   htmlSoup = BeautifulSoup(response)
   colleges = htmlSoup.find(id='sideLeft')
   collegeSoup = BeautifulSoup(str(colleges))
   for school in collegeSoup.findAll('a'):
      nextUrl = str(school).split('">',1)[0].replace('<a href="', '').replace('&amp;', '&')
      getSubjects(url, term)
     

def getSubjects(url, term):
   response = urllib2.urlopen(baseURL + url)
   htmlSoup = BeautifulSoup(response)
   for subject in htmlSoup.findAll('a'):
      if 'subjectDetails' in str(subject):
         nextUrl = str(subject).split('">',1)[0].replace('<a href="', '').replace('&amp;', '&')
         getClasses(nextUrl, term)
      
   
def getClasses(url, term):
   response = urllib2.urlopen(baseURL + url)
   htmlSoup = BeautifulSoup(response)
   for course in htmlSoup.findAll('tr'):
      if 'courseDetails' in str(course) and str(course).__len__() <= 1500:
         courseD = {}
         count = 0 
         if '34311' in course:
            print course
            break
         for attribute in str(course).split('<td '):
            if ', 2' in attribute or 'Final Exam' in attribute:
               continue
            string = attribute.split('">')[-1].replace('</td>', '').strip()
            string = string.split('</tr>')[0].split('</')[0].strip() 
            if string.startswith('<') or string == '':
               continue
          
            try:
               print classAtt[count] + " " + string
               #courseD[classAtt[count]] = string
            except:
               print str(count) + " " + string
               #print str(course)
            count += 1
         pushMongo(courseD, term)   
         
def pushMongo(din, term):
   print '' 
   #pprint(din)   

def main():
   getTerms()
   print ''

main()
