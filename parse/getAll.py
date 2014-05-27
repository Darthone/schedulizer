#!/usr/bin/python

"""
   File: getAll.py
   Author: Dario Marasco
   Created: 2014-05-24

   A simple python scraper to grab information from Drexel's term
   master schedule and print it out.

"""

import pymongo, urllib2
from BeautifulSoup import BeautifulSoup
from pprint import pprint

baseURL = "https://duapp2.drexel.edu"
#classAtt = ['Subject_Code', 'Course_Number', 'Instr_Type', 'Section', 'CRN', 'Course_Title', 'Days', 'Time', 'Instructor' ]
classAtt = ['Subject_Code', 'Course_Number', 'Instr_Type', 'Section', 'CRN', 'Course_Title', 'Time', 'Instructor' ]

def getTerms():
   response = urllib2.urlopen("https://duapp2.drexel.edu/webtms_du/app")
   htmlSoup = BeautifulSoup(response)

   # All divs containing Quarter/Semester info have class="term"
   for div in htmlSoup.findAll('div', 'term'):
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
         count = 0 

         # Does not correctly handle dates, using recursive=False does simplify
         # the parse tree a little, but it makes it hard to identify the times
         # and days correctly.
         # All course data entries are enclosed in 'td' tags, use recursive=False
         # because days and times are child tags, and make things messy
         for attribute in course.findAll('td', recursive=False):
            attributeString = attribute.getText().replace('&amp;', '&')
            try:
               print classAtt[count] + ": " + attributeString
            except:
               print str(count) + ": " + attributeString 
            count += 1
         print ''
         

def pushMongo(din, term):
   print '' 


def main():
   getTerms()
   print ''


if __name__ == '__main__':
   main()
