#!/bin/env/python

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
         extras = []
         for attribute in str(course).split('<td '):
            #print attribute
            string = attribute
            if 'Final Exam' in string:
               continue
            if '</tr>' in string:
               string = string.split('</tr>')[0]
            string = string.split('">')[-1].replace('</td>', '').strip().replace("</a></p>", '')
            if string.startswith('<') or string == '' or ', 20' in string:
               continue
          
            try:
               courseD[classAtt[count]] = string
            except:
               extras.append(string)
            count += 1
         if count >= 10:
            courseD['Days'] = courseD['Days'] + "  " + courseD['Instructor']
            courseD['Time'] = courseD['Time'] + "  "+ extras[0]
            courseD['Instructor'] = extras[1]
         pushMongo(courseD, term)   
         
def pushMongo(din, term):
   client = pymongo.MongoClient('localhost', 27017)
   db = client[term]
   collection = db['classes']
   collection.insert(din)

def main():
   getTerms()
   print ''

main()
