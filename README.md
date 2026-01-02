## What is it?
- A data analysis personal project that scrapes real-world data to find an optimal betting strategy for Ekstraklasa matches. It's a decision tree that uses each team's performance during previous season to give a probability score of each scenario (hosts winning, tie, guests winning), which combined with betting odds for each match gives us an option with the highest Expected Value.
- Initially I'd created a more sophisticated model (a RandomForest with 36 variables instead of a DecisionTree with 12), but it performed so well that I'm reluctant to share it publicly. This is a significantly numbed down version (and yet it performs almost as well as the other)

## What do I need to run it?
- All you need is a working Google Chrome Driver (download here: https://developer.chrome.com/docs/chromedriver/downloads), and Python packages listed in requirements.txt.
- If you just want to perform the analysis, download prepared CSV files from data.zip and analysis_DecisionTreeClassifier.ipynb.
Before running any scripts on your device, make sure you set correctly up necessary PATHs (these are marked accordingly).
- If you want to build necessary data, use oddsportal_scraping.py and ekstrastats_scraping_17-18_to_23-24.py, and then put both received CSVs into preprocessing.py. This ensures that we actually can merge these two tables.

## Info about scripts
- If you want to get the data, oddsportal_scraping.py is a script that scrapes basically all historical odds of Ekstraklasa starting at season 11/12 all the way to 24/25. However, we will only be using data starting at season 15/16, since other data is only available since then.
- Oddsportal.org is a dynamic page, so scraping it is a much more lengthy process - the script uses requests library, and it has exactly 80 pages to scrape, each one of them has to be loaded individually, so this script takes between 7 and 10 minutes to run. The upside is that it returns a single CSV file with all possible data.
- Ekstrastats-Scraping_17-18_to_23-24.py is named accordingly because this script only scrapes afforementioned seasons. This is because older data has to be parsed differently, and I originally used selenium to scrape it, but it seems to no longer work, so I rewrote this script so that now it uses BeautifulSoup. I may enhance this script to also contain 14/15, 15/16, and 16/17 seasons.

## TODO list in nearby future:
- Complete ekstrastats script so that it also includes other seasons
- Try different ML models
- Publish an attempt to use this model to predict 25/26 outcomes (already done it with initial RandomForest, but it's not going public any time soon)

## Main takeaways
- It's a stupidly simple algorithm (all variables it takes are: Points, Wins, Draws, Losses, Goals For, Goals Against, analyzed separately for hosts and guests), and yet it's profitable. Actually it's way more than just profitable.
- Picking the most probable outcome is a horrible way to bet on games



