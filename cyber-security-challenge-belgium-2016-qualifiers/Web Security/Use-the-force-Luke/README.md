# Cyber Security Challenge 2016: Use the force Luke

**Category:** Web security  
**Points:** 40  
**Challenge designer:** Xavier Mertens  
**Description:**  
> The access to the flag has been locked by the Empire. To unlock the website, try to use the force but not the "brute" force ;-). There is nothing to break, nothing hidden. Just try to learn how the website replies to your submitted data, use your hearing!

> Hint: Do you know the "Emperor Arrives" theme?

## Write-up
This challenge does not require high technical reverse engineering or crypto skills. The player must be able to understand how the application reacts depending on the submitted data. Scripting skills are a plus to automate the discovery of patterns.

When the player visits the challenge page for the first time, he sees an HTML form with a text field and the "Play" button. By doing a view source, the player will see that the field is limited to maximum two characters. By sending some random values, he will receive the message "Unknown code". If he sends a music note ('do', 're', 'mi', ...), he gets another message: "Wrong choice". At that point, the player must understand that music notes are expected. If a correct note is entered, the message "Go Ahead" is displayed. This means that the application is expecting the next correct note. When a correct note is received, a cookie called 'melody' is created which contains the current melody base64 encoded. This cookie has a very limited lifetime (15 seconds). If the player waits too long to enter the next note or if a wrong one is selected, the cookie is deleted and the player must start over.

The goal is to play the "Emperor Arrives" theme (http://www.musicnotes.com/sheetmusic/mtd.asp?ppn=MN0149859 - starting from "Marcato"). If the player has some music knowledge and he can read partitions, it will deduce the notes to use, otherwise, he can try to script the submission of notes one by one. The expected notes sequence is: LA-LA-LA-LA-MI-DO-LA-MI-DO-LA.

The key is displayed when all the notes have been submited in the correct order.

Note: a clever player can enable a debug mode by adding the parameter "?debug=1". In this mode, the current recorded melody is display and help him to understand the challenge.
## Other write-ups and resources
