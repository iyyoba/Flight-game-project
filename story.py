
import  textwrap
story = ''' If you, the player, have the knack to be a secret agent then this game is for you.In this game you will chase after a criminal who has done some heinous crimes and is on the run in Europe.

The criminal is under the radar of interpol and the interpol has assigned you with the task of capturing him and bringing him to justice.

You start your pursuit from the first airport on your list. At this airport you will be welcomed with an initial money and mileage(range). To pursue and capture the criminal money and range will be your valuable assets. At some of the airports you will find loot boxes. If you decide to open them, you might be rewarded with money to fund your chase. Unfortunately, some of the loot boxes might have bandits that will  rob you of your money. So, Good luck with the loot boxes.

You have to use your wealth wisely to accomplish your ultimate goal - capture the criminal. At every airport you arrive you buy mileage(range) with your initial money or the money you won from the lootboxes.

If you run out of money and mileage before apprehending the criminal, you will lose the game. If you arrive at the airport that harbors the criminal you win the game.'''

wrapper = textwrap.TextWrapper(width = 80, break_long_words = False, replace_whitespace = False)
word_list = wrapper.wrap(text = story)

def getStory():
    return word_list

