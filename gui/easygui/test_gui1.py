import easygui as eg
import sys
image   = "1.grass10.gif"
msg     = "Is this mowable?"
choices = ["Yes","No"]
reply   = eg.buttonbox(msg,image=image,choices=choices)
#choice = choicebox(msg, title, choices)
# note that we convert choice to string, in case
# the user cancelled the choice, and we got None.
#eg.msgbox("You chose: " + str(reply), "Result")
if reply == "Yes":
	eg.msgbox("Going to mow....:")
if reply == "No":
	eg.msgbox("NOT Going to mow....:")
