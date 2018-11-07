# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 09:16:08 2018

@author: William Keilsohn
"""

'''
Questions from Class:
    3) Find all movies where there are no ratings for men and no ratings for women.
    7) Year difference between top rated movies. How often does a high rated movie come along?
    12) Type zip code and get most popular movie.
'''

# Import Packages
#import calendar
#import time
import pandas as pd
#import nltk
import re
import numpy as np

# Load in the data
### All from class
udata = ['user_id', 'gender', 'age', 'occupation','zip']
users = pd.read_table('/ml20//users.dat',sep='::',
                      header=None, names = udata, engine = 'python')
mdata=['movie_id', 'title', 'genre']
movies = pd.read_table('/ml20//movies.dat', 
                       sep='::', header=None, names=mdata,engine = 'python')
rdata=['user_id','movie_id', 'rating', 'time']
ratings = pd.read_table('/ml20//ratings.dat', 
                       sep='::', header=None, names=rdata,engine = 'python')

# Merge the data frames to create one central dataset
data = pd.merge(pd.merge(ratings,users),movies) ### Also from class

# Begin answering questions
## Question 3
meanGenderRatings = data.pivot_table('rating',index='title', columns='gender', aggfunc='mean')# From class. Creates a pivot table based on gender.
meanGenderRatings = meanGenderRatings.fillna(0) ### Making the assumption that it was a 1-5 star scale
# Also, this is from the online resource provided.
genderInput = input("Please enter a prefered sex as either 'M' or 'F': ")
genderRateLis = []
for i in range(0, len(meanGenderRatings)):
    if (meanGenderRatings.iloc[i][genderInput] == 0): #https://stackoverflow.com/questions/16729574/how-to-get-a-value-from-a-cell-of-a-dataframe
        genderRateLis.append(meanGenderRatings.index[i])
print('\n')
print(genderRateLis) #Answers Question

## Question 7, and by default number 1
### I hate regular expressions...
## https://stackoverflow.com/questions/43278967/how-to-find-a-pair-of-numbers-between-parentheses-using-a-regular-expression

# Due to needing the same data table down below, I'm going to make a copy of the data
newData = data
titleLis = newData['title'].tolist() #https://stackoverflow.com/questions/22341271/get-list-from-pandas-dataframe-column
titleStr = ', '.join(titleLis) #https://www.decalage.info/en/python/print_list
dateLis = re.findall(r'(?<=\()\d{4}(?=\))', titleStr) #See link at top of section
newData['year'] = dateLis # Would solve number 1

### Look for reviewers
reviewerData = newData.pivot_table('user_id', index = 'rating', columns = 'title' , aggfunc = 'count')
reviewerData = reviewerData.fillna(0) #Online source provided
titles = list(reviewerData) #https://stackoverflow.com/questions/19482970/get-list-from-pandas-dataframe-column-headers
sumedColumns = reviewerData[titles].sum() #https://stackoverflow.com/questions/41286569/get-total-of-pandas-column/41286607
sumedColumns = pd.Series.to_frame(sumedColumns) # https://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.to_frame.html
filteredData = []
for b in range(0, len(sumedColumns)):
    if sumedColumns[0][b] < 5: #General Consensus was that atleast 5 people had to review a movie
        fliteredData = filteredData.append(str(sumedColumns[0].index.values[b])) #https://stackoverflow.com/questions/18358938/get-row-index-values-of-pandas-dataframe-as-list

for c in filteredData: #This takes a little time but it eliminates all the underreviewed movies.
    newData = newData[newData.title != c] #https://stackoverflow.com/questions/18172851/deleting-dataframe-row-in-pandas-based-on-column-value

### Filter out what we do/don't want
meanYearRatings = newData.pivot_table('rating', index = 'title', columns = 'year' , aggfunc = 'mean')
columns = list(meanYearRatings) #https://stackoverflow.com/questions/19482970/get-list-from-pandas-dataframe-column-headers
filteredYearRatings = meanYearRatings[(meanYearRatings[columns]) > 4.5] #Assumes that a top rated movie is a 4.5 or above. 
#https://stackoverflow.com/questions/44482095/dataframe-filtering-rows-by-column-values
filledYearRatings = filteredYearRatings.fillna(0) # Online source provided

yearLis = []
for j in filledYearRatings: #https://stackoverflow.com/questions/28218698/how-to-iterate-over-columns-of-pandas-dataframe-to-run-regression
    totalVal = filledYearRatings[j].sum() #https://stackoverflow.com/questions/41286569/get-total-of-pandas-column/41286607
    if totalVal > 0:
        yearLis.append(int(j))
        

spanLis = [yearLis[a + 1] - yearLis[a] for a in range(len(yearLis) - 1)] #https://stackoverflow.com/questions/2400840/python-differences-between-elements-of-a-list
averageYears = sum(spanLis) / len(spanLis) #https://stackoverflow.com/questions/9039961/finding-the-average-of-a-list
print('\n')
print('The average number of years between new "top rated" movies is:')
print(str(averageYears))


'''
I wrote this, and then realized I didn't need it, but it took me like 40min to come up with so now it's a comment.
#sortedYearRatings = filledYearRatings.sort_values(by = columns, ascending = False)
'''


## Question 12
meanZipRatings = data.pivot_table('rating',index='title', columns='zip', aggfunc='mean')
zipPut = input('Please enter a Zip Code: ')
yourZipMovies = meanZipRatings.loc[:, zipPut] #Online resource provided
yourZipMovies = yourZipMovies.fillna(0) #Online resource provided
yourZipMovies = yourZipMovies.sort_values(ascending = False)
if (yourZipMovies[0] == 0):
    print('''Sorry, but no reviews yet exist in your area.
          May I instead suggest Aliens and/or Toy Story?''')
else:
    #print(yourZipMovies.index[0]) # Technically this is the "Top Movie" in the area, but given the nature of the data, it's not very informative.
    topScore = yourZipMovies[0]
    topLis = []
    for z in range(0, len(yourZipMovies)):
        if yourZipMovies[z] == topScore:
            topLis.append(yourZipMovies.index[z])
    print(topLis) #Fully Aswers the question by providing all of the "Top rated" movies in the area.


