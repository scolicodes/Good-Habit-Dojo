import datetime
from datetime import timedelta, date
from calendar import monthrange

beltMilestones = {'White': 0, 'Yellow': 10, 'Orange': 20, 'Green': 30,
                  'Purple': 40, 'Blue': 50, 'Brown': 60, 'Red': 70, 'Pink': 80, 'Black': 90}

beltRGBs = {'White': [255, 255, 255], 'Yellow': [255, 255, 0], 'Orange': [255, 140, 0], 'Green': [0, 128, 0],
            'Purple': [186, 85, 211], 'Blue': [0, 0, 255], 'Brown': [139, 69, 19], 'Red': [255, 0, 0],
            'Pink': [255, 192, 203], 'Black': [0, 0, 0]}

RESET_COLOR_FORMAT = '\033[39m'

print("Welcome to the Good Habit Dojo, where your discipline is rewarded with belt promotions akin to those in martial"
      " arts.\n")

while True:
    try:
        userInput = input("Please enter the month, day, and year (in the form, mm/dd/yyyy) that you began or want to "
                          "begin your good habit. If you\nare starting today, enter today's date: ")
        for i, char in enumerate(userInput):
            if len(userInput) != 10:
                raise ValueError("\nERROR: The format of the date you entered is incorrect. It should be in the form, "
                                 "mm/dd/yyyy. Please try again.\n")
            elif i == 2 or i == 5:
                if char != '/':
                    raise ValueError("\nERROR: The format of the date you entered is incorrect. It should be in the "
                                     "form, mm/dd/yyyy. Please try again.\n")
            else:
                if not char.isdigit():
                    raise ValueError(
                        "\nERROR: The format of the date you entered is incorrect. It should be in the form, "
                        "mm/dd/yyyy. Please try again.\n")

        month, day, year = userInput.split('/')
        month, day, year = int(month), int(day), int(year)

        if month < 1 or month > 12:
            raise ValueError("\nERROR: The month should be in the range [1, 12]\n")
        daysInMonth = monthrange(year, month)[1]
        if day < 1 or day > daysInMonth:
            raise ValueError("\nERROR: The day you entered is out of range\n")
        if year < datetime.MINYEAR or year > datetime.MAXYEAR:
            raise ValueError("\nERROR: The year you enter can't be less than 1 or greater than 9999\n")
        break
    except ValueError as e:
        print(e)


startDate = date(year, month, day)
daysCompleted = (startDate.today() - startDate).days
daysUntilStart = (startDate - startDate.today()).days


def colored(r, g, b, text):
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)


def getCurrBelt():
    currBelt = None
    for beltColor in beltMilestones.keys():
        # If today is in between the current belt color's acquisition day and the next belt's, then the user is
        # currently the current belt
        if (startDate + timedelta(days=beltMilestones[beltColor])) <= startDate.today() <= \
                (startDate + timedelta(days=beltMilestones[beltColor] + 10)):
            currBelt = beltColor
        if startDate.today() >= (startDate + timedelta(days=90)):
            currBelt = 'Black'
    return currBelt


def getDaysUntilNextPromotion(daysCompleted):
    daysUntilPromo = 0
    nextBeltColor = None

    if daysCompleted >= 90:
        return "Congratulations! You have completed your journey!\n"
    else:
        for beltColor in beltMilestones:
            if daysCompleted < beltMilestones[beltColor]:
                nextBeltColor = beltColor
                break
        if daysCompleted % 10 == 0:
            daysUntilPromo = 10
        else:
            while daysCompleted % 10 != 0:
                daysCompleted += 1
                daysUntilPromo += 1

        nextBeltColor = colored(beltRGBs[nextBeltColor][0], beltRGBs[nextBeltColor][1], beltRGBs[nextBeltColor][2],
                                nextBeltColor)
        if daysUntilPromo == 1:
            return str(daysUntilPromo) + ' more day until you get promoted to ' + nextBeltColor + RESET_COLOR_FORMAT + \
                   'belt!\n'
        else:
            return str(daysUntilPromo) + ' more days until you get promoted to ' + nextBeltColor + RESET_COLOR_FORMAT + \
                   'belt!\n'


print('\n' + 'Start Date:', startDate.strftime('%m/%d/%y') + '\n')

currBelt = getCurrBelt()

if currBelt is None:
    if daysUntilStart == 1:
        print("Your good habit journey begins in " + str(daysUntilStart) + " day\n")
    else:
        print("Your good habit journey begins in " + str(daysUntilStart) + " days\n")
elif currBelt == 'Orange':
    print("You have completed", daysCompleted, "days and are an " + colored(beltRGBs[currBelt][0],
                                                                            beltRGBs[currBelt][1],
                                                                            beltRGBs[currBelt][2],
                                                                            currBelt) +
          RESET_COLOR_FORMAT + "belt.\n")
else:
    if daysCompleted == 1:
        print("You have completed", daysCompleted, "day and are a " + colored(beltRGBs[currBelt][0],
                                                                              beltRGBs[currBelt][1],
                                                                              beltRGBs[currBelt][2], currBelt) +
              RESET_COLOR_FORMAT + "belt.\n")
    else:
        print("You have completed", daysCompleted, "days and are a " + colored(beltRGBs[currBelt][0],
                                                                               beltRGBs[currBelt][1],
                                                                               beltRGBs[currBelt][2], currBelt) +
              RESET_COLOR_FORMAT + "belt.\n")

if currBelt is not None:
    print(getDaysUntilNextPromotion(daysCompleted))

counter = 0
seenCurrBelt = False
for beltColor in beltMilestones.keys():
    if startDate.today() >= (startDate + timedelta(days=beltMilestones[beltColor] + 10)) or \
            (startDate.today() - startDate).days == 90:
        print(colored(beltRGBs[beltColor][0], beltRGBs[beltColor][1], beltRGBs[beltColor][2], beltColor) +
              RESET_COLOR_FORMAT + '- ' + (startDate + timedelta(days=beltMilestones[beltColor])).strftime('%m/%d') +
              ' (' + str(beltMilestones[beltColor]), 'Days)', u'\u2713')
    elif (startDate + timedelta(days=beltMilestones[beltColor])) <= startDate.today() <= \
            (startDate + timedelta(days=beltMilestones[beltColor] + 10)):
        print(colored(beltRGBs[beltColor][0], beltRGBs[beltColor][1], beltRGBs[beltColor][2], beltColor) +
              RESET_COLOR_FORMAT + '- ' + (startDate + timedelta(days=beltMilestones[beltColor])).strftime('%m/%d') +
              ' (' + str(beltMilestones[beltColor]), 'Days)', u'\u2610', u'\u2190', 'you are here')
    else:
        print(colored(beltRGBs[beltColor][0], beltRGBs[beltColor][1], beltRGBs[beltColor][2], beltColor) +
              RESET_COLOR_FORMAT + '- ' + (startDate + timedelta(days=beltMilestones[beltColor])).strftime('%m/%d') +
              ' (' + str(beltMilestones[beltColor]), 'Days)', u'\u2610')
