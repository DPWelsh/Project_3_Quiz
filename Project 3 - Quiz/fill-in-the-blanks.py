# IPND Stage 2 Final Project

# You've built a Mad-Libs game with some help from Sean.
# Now you'll work on your own game to practice your skills and demonstrate what you've learned.

# For this project, you'll be building a Fill-in-the-Blanks quiz.
# Your quiz will prompt a user with a paragraph containing several blanks.
# The user should then be asked to fill in each blank appropriately to complete the paragraph.
# This can be used as a study tool to help you remember important vocabulary!

# Note: Your game will have to accept user input so, like the Mad Libs generator,
# you won't be able to run it using Sublime's `Build` feature.
# Instead you'll need to run the program in Terminal or IDLE.
# Refer to Work Session 5 if you need a refresher on how to do this.

# To help you get started, we've provided a sample paragraph that you can use when testing your code.
# Your game should consist of 3 or more levels, so you should add your own paragraphs as well!

# The answer for ___1___ is 'function'. Can you figure out the others?

# We've also given you a file called fill-in-the-blanks.pyc which is a working version of the project.
# A .pyc file is a Python file that has been translated into "byte code".
# This means the code will run the same as the original .py file, but when you open it
# it won't look like Python code! But you can run it just like a regular Python file
# to see how your code should behave.

# Hint: It might help to think about how this project relates to the Mad Libs generator you built with Sean.
# In the Mad Libs generator, you take a paragraph and replace all instances of NOUN and VERB.
# How can you adapt that design to work with numbered blanks?

# If you need help, you can sign up for a 1 on 1 coaching appointment: https://calendly.com/ipnd-1-1/20min/

levelList = ['easy','medium','hard']

sample = [""]
answers = [""]

sample_easy = '''A ___1___ is created with the def keyword. You specify the inputs a ___1___ takes by
adding ___2___ separated by commas between the parentheses. ___1___s by default return ___3___ if you
don't specify the value to return. ___2___ can be standard data types such as string, number, dictionary,
tuple, and ___4___ or can be more complicated such as objects and lambda functions.'''

sample_answers_easy = ["function","parameters","None","List"]

sample_medium = '''
___1___ statement:
    Terminates the ___2___ statement and transfers execution to the statement immediately following the ___2___.

continue statement:
    Causes the ___2___ to skip the remainder of its body and immediately retest its condition prior to reiterating.

___3___ statement:
    The ___3___ statement in Python is used when a statement is required syntactically but you do not want any command or code to ___4____.
    '''
sample_answers_medium = ["Break","loop","Pass","Execute"]


sample_hard = '''A ___1___ is created with the def keyword. You specify the inputs a ___1___ takes by
adding ___2___ separated by commas between the parentheses. ___1___s by default return ___3___ if you
don't specify the value to return. ___2___ can be standard data types such as string, number, dictionary,
tuple, and ___4___ or can be more complicated such as ___5___ and ___6___ functions.'''

sample_answers_hard = ["function","parameters","None","boolean","objects","lambda"]

## fucntion to choose the level - based on user input - returns the choice of the level.
def chooseLevel():
    while True:
        levelChoice = input()
        levelChoice = levelChoice.lower()
        for level in levelList:
            if levelChoice == level:
                print("you have chosen: "+levelChoice.upper())
                return levelChoice
                break
        print("That is not a level, please try again")

def findMax(string):
    max = 0
    index = 0
    for a in sample:
        if(a.isdigit() and sample[index +1] == '_' and sample[index -1] == '_'):
            digit = int(a)
            if(digit > max):
                max = digit
        index +=1
    return max


##Function to update the sample text for the level
def updateSample(level):
    if level == 'easy':
        sample = sample_easy
    elif level == 'medium':
        sample = sample_medium
    elif level == 'hard':
        sample = sample_hard
    print(sample)
    return sample

##Function to update the sample answers for the level
def updateSampleAnswers(level):
    if level == 'easy':
        sample_answers = sample_answers_easy
    elif level == 'medium':
        sample_answers = sample_answers_medium
    elif level == 'hard':
        sample_answers = sample_answers_hard
    return sample_answers

def correctGuess(guess,answers,wordNum):
    currentAnswer = answers[wordNum]
    if guess.upper() == currentAnswer.upper():
        return currentAnswer
    return None

def winOrLose(lives,chosenLives):
    if chosenLives == lives:
        print("you LOSE. :( .. Please try again another time.")
    else:
        print("you WIN!!")

def playGame(sample, answers):
    max_num = findMax(sample)
    lives = 0
    word_num = 0
    while(lives < 5 and word_num<max_num):
        print("** Lives remaining: "+str(5-lives)+" **")
        print("Choose a word for ___"+str(word_num+1)+"___:")
        guess = correctGuess(input(),answers,word_num)
        if guess == None:
            lives +=1
        else:
            toReplace = '___'+str(word_num+1)+'___'
            print()
            sample = sample.replace(toReplace,guess)
            print(sample)
            word_num +=1
    winOrLose(lives,5)

print("Hello, welcome to my game - Udacity Project 3 - Quiz - Practice")
print("which level would you like? Please Choose Easy, Medium or Hard")

levelChoice = chooseLevel()
sample = updateSample(levelChoice)
answers = updateSampleAnswers(levelChoice)
playGame(sample, answers)




