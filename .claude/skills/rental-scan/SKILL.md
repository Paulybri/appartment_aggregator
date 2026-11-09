---
name: rental-scan
description: Scan apparment rental listings, apply a score to then and add aggregate them in a file.
---

Important file:
 - Criteria: `CRITERIA.md`
 - Prospects `output/prospects.csv`
 - Rejects `output/rejects.csv`

Scan all appartment rental listings from these sites:

- https://www.kijiji.ca/ (via curl)

Adapt the search to look for listings aligned with the user's criteria, but a bit broader, to make sure no potential prospect is missed.
Only look for listings that are available for rent, not for sale. Only look at listings that have been posted in the last 2 weeks. Skip older listings.

Only treat criteria as deal breaker if the user explicitally says that is it deal-breaking.

Do not stop to asks questions, just refer to Criteria file.

Once done, do not write any output, simply let the user know hoe many Prospect listings have been added

From each listing found:

  1) Check if it has already been scored: has the listing been added to Prospects or Rejects ? If so, skip it
  2) Create a score from 0 to 100. 0 being worst and 100 being perfect. The score is determined based off of Criteria. Do not make the price influence the score. Let the user decide if the price is acceptable or not.
  4) Once a score it set
    - If the listing does not meet deal breaking requirements, add an entry to the Rejects file
    - If it does meet deal breaking requirement, add the an entry to the Prospects file.
  Entries should follow this format:
  ```
    SCORE,PRICE,LOCATION,POSTED,LISTING LINK,HIDDEN
  ```
  POSTED is the date the listing was posted, as YYYY-MM-DD (the viewer shows how long ago that was). If the date is not available, leave it empty.
  HIDDEN is `false` for new entries. The user toggles it from the viewer; never change the HIDDEN value of an existing entry.
  4) Start the local webpage server to serve the Prospects file (it also saves the HIDDEN flag when the user hides a listing). The user will be able to open the Prospects file in a browser and click on the links to see the listings:
  ```
    python3 viewer/server.py
  ```
  http://localhost:8000/viewer/
