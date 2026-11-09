---
name: rental-scan
description: Scan apparment rental listings, apply a score to then and add aggregate them in a file.
---

Important file:
 - Criteria: `CRITERIA.md`
 - Prospects `output/prospects.csv`
 - Rejects `output/rejects.csv`

Scan all appartment rental listings from these sites:

- https://www.kijiji.ca/

Adapt the search to look for listings aligned with the user's criteria, but a bit broader, to make sure no potential prospect is missed.

Only treat criteria as deal breaker if the user explicitally says that is it deal-breaking.

Do not stop to asks questions, just refer to Criteria file.

Once done, do not write any output, simply let the user know hoe many Prospect listings have been added

From each listing found:

  1) Check if it has already been scored: has the listing been added to Prospects or Rejects ? If so, skip it
  2) Create a score from 0 to 100. 0 being worst and 100 being perfect. The score is determined based off of Criteria.
  4) Once a score it set
    - If the listing does not meet deal breaking requirements, add an entry to the Rejects file
    - If it does meet deal breaking requirement, add the an entry to the Prospects file.
  Entries should follow this format:
  ```
    SCORE,PRICE,LOCATION,LISTING LINK
  ```
