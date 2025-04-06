# Submission Questions

## What was your initial thought process when you first read the problem statement, and how did you break it down into smaller, manageable parts?

The first thing that came to mind was to treat this as a location-based search problem layered with fuzzy string matching. I broke it into three parts:

1. Accept and clean the user’s query (handling typos).
2. Convert the (corrected) location to coordinates.
3. Calculate distances from all known property locations and filter by 50km radius.\
   Keeping the flow simple and fast was the goal from the start.

## What specific tools, libraries, or online resources did you use to develop your solution, and why did you choose them over other options?

I used Flask for the API because it's lightweight and quick to set up. For geolocation, `geopy` with Nominatim worked well for converting city names to coordinates. I went with `pyspellchecker` for fixing typos since it’s straightforward and works offline. CSV was good enough for city and property data—no need for a database in this case. These choices kept things clean and fast.

## Describe a key challenge you faced while solving this problem and how you arrived at the final solution?

The biggest challenge was handling misspelled city names reliably. I initially tried using Levenshtein distance, but it always returned a 100% match with *some* city from the list, even if that city wasn’t actually what the user meant. That wasn’t ideal because the CSV file I had didn’t contain all Indian cities—so the “closest match” could end up being completely wrong.

Finding a good enough city database was also a pain. I finally found a solid base on [simplemaps.com](https://simplemaps.com/data/world-cities), filtered it down to Indian cities, and then manually (and with AI help) added more lesser-known or underrepresented cities to the dataset to improve accuracy. Once that was done, I switched from Levenshtein to `pyspellchecker`, trained on this expanded list, which worked much better because it only corrected to cities I knew were relevant.

## If you had more time, what improvements or alternative approaches would you explore, and why do you think they might be valuable?

If I had more time, I’d first add caching for geocoding results to avoid hitting the API repeatedly for the same city names—that would speed things up and reduce unnecessary calls. I’d also clean up the city data a bit more to remove any duplicates or inconsistent entries. Maybe even add a few tests and simple logging to help track what's happening in the background. These small changes would just make the tool more reliable and easier to maintain.