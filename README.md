# ProClubs

This project explores the data from https://proclubshead.com/ with the obtjective of identifying what factors, both short and long-term, can be used to predict the outcome of any given online game of FIFA 23 Pro Clubs. 

The braod steps were as follows. 

1. Python/BeautifulSoup was used to scrape the team data, match data, and individual player performance data for over 47,000 clubs, 92,000 games, and 731,000 individual player performances. This data was cleaned, and stored to csv files.  ***(More Info Below) 

2. This data was then used to provide visualizations to allow for initial analyis of the collected data. Visualizations pertaining to club data, Man of the Match performances, and individual match data were all generated using Matplotlib. These visualizations can be found in the visualizations folder, with a sample of them located below. 

3. Random Forest models were generated to model classify both man of the match performances (Yes/No), and match outcomes (Win/Loss/Draw). 90.5% accuracy, and 68.1% accuracy were achieved on these models respectively. 



Point 1 - 
***Given the structure of the website (and EA Sports' https://www.ea.com/en-gb/games/fifa/pro-clubs from where the data is originally sourced), it's impossible to easily pull the club data for all 400k clubs (estimated) since each club has a unqiue ID# which can only be obtained if you know the name of the club. Only the top 100 clubs are publicly listed. The only means of obtaining data beyond the top 100 clubs is to create a repeatable script which scrapes their recent opponents list, and then looks up information about those clubs. 

The code provided here is capable of repeating that process, and theroetically obtaining all club data for the ~400k club. Given time and bandwidth concerns I elected to stop the scrape at ~47,000 clubs, and 92,000 games. 

Point 2 - 
***Match Result RF Model (.681 Acc - 750 Est).ipynb

The model attempts to predict if a team (Team A) with either win, draw, or lose the game against (Team B). The model looks at three primary types of data. 

1. Information about the performance of Team A and Team B in a game (# passes, # shots, # goals scored, etc)
2. Information about the long-term performance of Team A and Team B (Total Games played, average goals scored per game, goals concdeed per game, etc)

https://github.com/RainRad/ProClubs/blob/main/Visualizations/MOTM%20Average%20forward.png
https://github.com/RainRad/ProClubs/blob/main/Visualizations/Average%20Goals%20Scored%20or%20Conceded%20Per%20Match.jpg
https://github.com/RainRad/ProClubs/blob/main/Visualizations/Passing%20%26%20Shooting%20(Same%20Division).jpg
