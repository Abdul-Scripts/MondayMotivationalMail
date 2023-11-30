# MondayMotivationalMail

Welcome to my Project called Monday Motivational Mail! This is my final project for my HarvardEdX CS50 course, and it showcases a little snippet of the favorite things I learned throughout the course.

## Overview/Description:

You and I both hate Monday, right? According to Urban Dictionary, Mondayitis is a feeling of weariness, sadness, apathy and general distress that people feel when starting the Monday work week and I suffer from chronic Mondayitis. Monday is infamously known throughtout all levels of society as the worst day of the week. Whether you're a high-school student, college student, professor, McDonald's worker or any other regular Joe, chances are that you probably fit among the group of people who resent this day for existing. It painfully reminds you that you have work and effort to put into your mundane but necessary routine, likely also meaning that there is plenty of failure ahead. This grand notoriety of Monday's is so wide-spread, that the term mentioned earlier was coined to describe this dreadful feeling that Monday tends to bring out of people. This highlights a pattern of clear lack of motivation within society on this day. Although you or your friend may not be afflicted with this phenomenon or to the extent where you find it concerning, it definetly deals a significant negative impact that is worth heeding to. Enter, Monday Motivational Mail, or MMM for short. With MMM, you'll be able to start your week just a tad bit less annoyed and maybe even completely motivated and read to take on your week's challenges! With a every week, every Monday, you will slowly overcome your affliction of Mondayitis! Monday Motivational Mail is a program that takes a quote from an API called ZenQuotes, as well as an image from another API called Pixabay, and combines the two using image processing by PIL. The output is then emailed to the user's email of choice using smtplib and mime every week using a cron job. Now every week can be a little bit more meaningful to you, and that's what matters!

## How to use:

#### Step 1: Download all the files
#### Step 2: Create a new disposable gmail account that will do the sending (You don't want to clutter your main gmail, trust me)
#### Step 3: Create an app password in gmail account for this program. (google account > security > 2 step verification > App passwords)
#### Step 4: Sign up for a free account on Pixabay.com and go to their API docs and retrieve your API key.
#### Step 5: Making sure you're in the same directory as MondayMotivationalMail.py, create a new .env file using this command:
``` bash
touch .env
```
Now open this file and paste in this format:

``` .env
APP_PASS='google app password'
SENDER_EMAIL=your-new-email@gmail.com
API_KEY=apikey
```

#### Step 6: Paste your API key in the "API_KEY" variable
#### Step 7: Paste App Password you got from your new gmail account into the "APP_PASS" variable
#### Step 8: Paste in your new email into "SENDER_EMAIL" variable, then save and close .env file
#### Step 9: Open MondayMotivationalMail.py and put in as many receiver emails you want (These will be the people who will receive the motivational quotes)
#### Step 10: Your program is ready! You can test by running it. Now to schedule the program every monday using crontab! open your terminal and execute a new cron job using this command: 
``` bash
crontab -e
```
#### Step 11: Click i to enter insert mode
#### Step 12: type this into the editor and substite each part respectively: 
```bash
0 9 * * 1 cd /Users/user.name/folder && /usr/bin/python MondayMotivationalMail.py 
```
where '0 9 * * 1' means every monday at 9am and '/Users/user.name/folder' is the path to the location where the MondayMotivationalMail.py file is located and '/usr/bin/python' is the path to Python

#### Step 13: Press esc to exit the editing mode. and Type :wq to save and quit the file.
#### Step 14: You should get a message saying "crontab: installing new crontab" which tells you created the crontab.

## Final Thoughts:
There you go! now every monday at 9am the MondayMotivationalMail.py script will run, which will send you an email with a motivational quote! Done! You might receive your first mail in Junk or Spam folder but that's because your email is brand new. To fix this just reply to one of the motivational emails you receive in your Junk/Spam folder and from now on they should appear in your main inbox. (◠ ‿ ◠)
