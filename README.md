# ProClubs

This project explores the data from https://proclubshead.com/ with the obtjective of identifying what factors, both short and long-term, can be used to predict the outcome of any given online game of FIFA 23 Pro Clubs. 

The braod steps were as follows. 

1. Python/BeautifulSoup was used to scrape the team data, match data, and individual player performance data for over 7,000 clubs, 30,000 games, and 300,000 individual player performances. This data was cleaned, and stored to csv files.  ***(More Info Below) 

2. The stored club and match csv files were uploaded to a SQL database where they were joined and imported into python. Scikit Learn was used to run supervised learning algorithms on the data collected. Both Random forest and KNN models were deployed on the dataset, and a accuracy of 81.9% was obtained. *** Details Below)



Point 1 - 
***Given the structure of the website (and EA Sports' https://www.ea.com/en-gb/games/fifa/pro-clubs from where the data is originally sourced), it's impossible to easily pull the club data for all 400k clubs (estimated) since each club has a unqiue ID# which can only be obtained if you know the name of the club. Only the top 100 clubs are publicly listed. The only means of obtaining data beyond the top 100 clubs is to create a repeatable script which scrapes their recent opponents list, and then looks up information about those clubs. 

The code provided here is capable of repeating that process, and theroetically obtaining all club data for the ~400k club. Given time and bandwidth concerns I elected to stop the scrape at ~7,000 clubs, and 30,000 games. 

Point 2 - 
***Joined Random Forest (.819_750) v1

The model attempts to predict if a team (Team A) with either win a game, or draw/lose the game against (Team B). The model looks at three primary types of data. 

1. Information about the performance of Team A in a game (# passes, # shots, # goals scored, etc)
2. Information about the long-term performance of Team A (Total Games played, average goals scored per game, goals concdeed per game, etc)
3. Comparative information about the long-term performance of Team A vs Team B (Team A goals/pg - Team B goals/pg, etc)

Notably, the model is NOT provided information about the in-game performance of Team B. This was done so that a team could reasonably use the model to answer the following question: 

"Supppose our team (Team A), is going against another team (Team B). Based upon our historical performances, and assuming we achieve X stat line, what will be our odds of winning?" 

![image](https://user-images.githubusercontent.com/111028732/228394968-f69a9813-05e5-47f8-9240-a3e332a7a13d.png)
![image](https://user-images.githubusercontent.com/111028732/228395029-fdbf3781-c05c-47da-bb9d-a0fd9e86d44d.png)

