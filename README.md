A short disclaimer: I might've said here or there that "this model actually works". Since then I've noticed an error which massively overestimated model's performance; this is NOT a profitable model. But it works in a way that if this were a zero-sum game, the best performing model would yield 1.05 ROB (Return on Bet). A 5% edge would be massive in, for example, stock market; it's just not enough to beat bookmaker margins.

## What is it?
- A data analysis personal project that scrapes real-world data to find an optimal betting strategy for Ekstraklasa matches. It's a decision tree that uses each team's performance during previous season to give a probability score of each scenario (hosts winning, tie, guests winning), which combined with betting odds for each match gives us an option with the highest Expected Value.
- Initially I'd created a more sophisticated model (a RandomForest with 36 variables instead of a DecisionTree with 12), but it performed so well that I'm reluctant to share it publicly. This is a significantly numbed down version (and yet it performs almost as well as the other)

## What do I need to run it?
- All you need is a working Google Chrome Driver (download here: https://developer.chrome.com/docs/chromedriver/downloads), and Python packages listed in requirements.txt.
- If you just want to perform the analysis, download wszystko_znormalizowane.csv from data.zip and take analysis.ipynb.
Before running any scripts on your device, make sure you correctly set up necessary PATHs (these are marked accordingly with comments).
- If you want to build necessary data, normally you'd have to use oddsportal_scraping.py and ekstrastats_scraping.py, and then put both received CSVs into preprocessing.py. However, the script that's here would only build a fraction of used data - read below as to why.

## Info about scripts
- If you want to get the data, oddsportal_scraping.py is a script that scrapes basically all historical odds of Ekstraklasa starting at season 11/12 all the way to 24/25. However, we will only be using data starting at season 15/16, since other data is only available since then.
- Oddsportal.org is a dynamic page, so scraping it is a much more lengthy process - the script uses requests library, and it has exactly 80 pages to scrape, each one of them has to be loaded individually, so this script takes between 7 and 10 minutes to run. The upside is that it returns a single CSV file with all possible data.
- Ekstrastats-Scraping_17-18_to_23-24.py is named accordingly because this script only scrapes afforementioned seasons. This is because older data has to be parsed differently, and I originally used selenium to scrape it, but I found it to be working very inconsistently, so I rewrote this script to be based on BeautifulSoup. Enhancing this script to include all data is on top of my TODO list.
- AI usage is restricted to a few bugfixes, other than that nothing had been auto-generated

## TODO list in nearby future:
- Complete ekstrastats scraping script so that it also includes other seasons
- Some vizualizations wouldn't hurt (probably)

## Main takeaways
- It's a stupidly simple algorithm (all it takes is each team's previous season performance), and yet it's almost profitable.
- model.predict_proba isn't really working as intended (or my database of 3000 entries is just too small for it to work properly)



