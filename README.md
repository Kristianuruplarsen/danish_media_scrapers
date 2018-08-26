# Scrapers for various danish media archives
Work in progress.

So far i can get Berlingske and Politiken - you need to specify a year and a month to get the articles from.

```python
from scraper.berlingske import berlingske
b = berlingske.get_all_content(1999,4, sample_days = True, samplefrac_days = 0.5, sample_articles = True, samplefrac_articles = 0.1)


from scraper.politiken import politiken
pol = politiken.get_all_content(1999,4, sample_days = True, samplefrac_days = 0.5, sample_articles = True, samplefrac_articles = 0.1)
```
The `sample` params set if you want to sample respectively the number of days in the month to scrape, and the articles for each day. The `samplefrac` params set the share of each we sample. I.e. in a 30 days month samplefrac_days = 0.5 scrapes 15 days, and samplefrac_articles scrapes 10% of the articles in those 15 days. 

## Background info
Most (if not all) of the major danish media players provide free access to their archives, although some articles from the last couple of years will still have restricted access.

# Known issues:
None right now
