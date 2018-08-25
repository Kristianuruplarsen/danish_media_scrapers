# Scrapers for various danish media archives
Work in progress.

So far i can get berlingske and politiken - you need to specify a year and a month to get the articles from.

```python
from scraper.berlingske import berlingske
res = berlingske.get_all_content(1999,4, sample = True, samplefrac = 0.1)


from scraper.politiken import politiken
res = politiken.get_all_content(2006,4, sample = True, samplefrac = 0.1)
```

The `sample` and `samplefrac` params is mainly there so you can test if things work without downloading a full month of news coverage.


# Known issues:

The politiken scraper only handles articles correctly if they include an image.
