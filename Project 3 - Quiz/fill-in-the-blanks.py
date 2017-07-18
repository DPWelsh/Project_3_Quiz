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

level_list = ['easy','medium','hard']

game_text_easy = '''A ___1___ is created with the def keyword. You specify the inputs a ___1___ takes by
adding ___2___ separated by commas between the parentheses. ___1___s by default return ___3___ if you
don't specify the value to return. ___2___ can be standard data types such as string, number, dictionary,
tuple, and ___4___ or can be more complicated such as objects and lambda functions.'''

game_text_answers_easy = ["function","parameters","None","List"]

game_text_medium = '''
___1___ statement:
    Terminates the ___2___ statement and transfers execution to the statement immediately following the ___2___.

continue statement:
    Causes the ___2___ to skip the remainder of its body and immediately retest its condition prior to reiterating.

___3___ statement:
    The ___3___ statement in Python is used when a statement is required syntactically but you do not want any command or code to ___4____.
    '''
game_text_answers_medium = ["Break","loop","Pass","Execute"]

game_text_hard = '''A ___1___ is created with the def keyword. You specify the inputs a ___1___ takes by
adding ___2___ separated by commas between the parentheses. ___1___s by default return ___3___ if you
don't specify the value to return. ___2___ can be standard data types such as string, number, dictionary,
tuple, and ___4___ or can be more complicated such as ___5___ and ___6___ functions.'''

game_text_answers_hard = ["function","parameters","None","boolean","objects","lambda"]


# function allows the player to choose the level
# Input = User Input
# Output = returns the level of choice (will loop until easy, medium or hard is written)
def choose_level():
    while True:
        level_choice = input()
        level_choice = level_choice.lower()
        for level in level_list:
            if level_choice == level:
                print("you have chosen: "+level_choice.upper())
                return level_choice
        print("That is not a level, please try again")


# This function allows the player to choose the number of lives they wish to have - must be a positive digit,
# input = user input
# output = number of lives
def choose_lives():
    while True:
        print("How many lives do you want? Please enter a number: ")
        chosen_lives = input()
        if chosen_lives.isdigit() and int(chosen_lives)>0:  # Lives need to be positive number
            print("You have chosen: "+str(chosen_lives)+" lives!")
            return int(chosen_lives)
        print("that is not a positive number")


# Function to update the game_text text and answers for the level
# input = chosen level
# output is desired game level text with respective answers.
def update_game_text(level):
    text = ""
    text_answers = ""
    if level == 'easy':
        text = game_text_easy
        text_answers = game_text_answers_easy
    elif level == 'medium':
        text = game_text_medium
        text_answers = game_text_answers_medium
    elif level == 'hard':
        text = game_text_hard
        text_answers = game_text_answers_hard
    print(text)
    return text,text_answers


# Function is used to check if current guess is correct
# input = current guess, list of answers and the index of the current answer
# output = if guess equals the required answer (indexed from word_num) then it will return the answers,
# else it will return None which will cause the player to lose a life
def correct_guess(guess,answers,word_num):
    current_answer = answers[word_num]
    if guess.upper() == current_answer.upper():
        return current_answer
    return None


# Prints win or lose statement
# input is lives remaining and the amount of lives chosen by player
# If lives == chosen lives, then the playet has exhausted all lives and the game prints losing text.
def win_or_lose(lives,chosen_lives):
    if chosen_lives == lives:
        print("** You LOSE. :( .. Please try again another time. **")
    else:
        print("** You WIN!! **")


# Main portion of game - prompts user to guess the current blank word.
# if the guess is correct, fill the blank word, if the guess is
# incorrect, reduce a life
# keep playing until all lives are lost or there are no more answers.
def playGame(game_text, answers, num_lives):
    max_num = len(answers)
    num_guess = 0
    word_num = 0
    while num_guess < num_lives and word_num<max_num:
        print("** Lives remaining: "+str(num_lives-num_guess)+" **")
        print("Choose a word for ___"+str(word_num+1)+"___:")
        guess = correct_guess(input(),answers,word_num)
        if guess == None:
            num_guess +=1
        else:
            to_replace = '___'+str(word_num+1)+'___'
            print()
            game_text = game_text.replace(to_replace,guess)
            print(game_text)
            word_num +=1
    win_or_lose(num_guess,num_lives)

print("Hello, welcome to my game - Udacity Project 3 - Quiz - Practice")
print("which level would you like? Please Choose Easy, Medium or Hard")

levelChoice = choose_level()
num_lives = choose_lives()

# For neater and condensed code, a tuple is required for selection of the game_text and answers.
game_text,answers = update_game_text(levelChoice)
playGame(game_text, answers, num_lives)




