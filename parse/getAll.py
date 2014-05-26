#!/usr/bin/python

import pymongo, urllib2
from BeautifulSoup import BeautifulSoup
from pprint import pprint

baseURL = "https://duapp2.drexel.edu"
tmsAppURL = "webtms_du/app"
classAtt = ['Subject_Code', 'Course_Number', 'Instr_Type', 'Section', 'CRN', 'Course_Title', 'Days', 'Time', 'Instructor' ]

def getTerms():
   tmsURL = baseURL + tmsAppURL
   response = urllib2.urlopen("https://duapp2.drexel.edu/webtms_du/app")
   htmlSoup = BeautifulSoup(response)

   for div in htmlSoup.findAll('div'):
      # All divs containing Quarter/Semester info have class="term"
      if div.get('class') == 'term':
         href = div.find('a')
         termName = href.getText()
         termURL = href.get('href').replace('&amp;', '&')
         getColleges(termURL, termName)
    
         
def getColleges(url, term):
   response = urllib2.urlopen(baseURL + url)
   htmlSoup = BeautifulSoup(response)

   # Colleges are the only hyperlinks in the left sidebar
   colleges = htmlSoup.find(id='sideLeft')
   for school in colleges.findAll('a'):
      schoolName = school.getText()
      nextUrl = school.get('href').replace('&amp;', '&')
      getSubjects(url, term)
     

def getSubjects(url, term):
   response = urllib2.urlopen(baseURL + url)
   htmlSoup = BeautifulSoup(response)

   # The Subjects are listed in a table of class='collegePanel'
   subjectTable = htmlSoup.find('table', 'collegePanel')
   for subject in subjectTable.findAll('a'):
      subjectName = subject.getText()
      nextUrl = subject.get('href').replace('&amp;', '&')
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
