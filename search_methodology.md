# Search Methodology

## Effective Queries

### General Queries (with name + company)
- `"{name}" "{company}" arrested` -
- `"{name}" "{company}" convicted fraud` -
- `"{name}" "{company}" sentenced prison` -
- `"{name}" "{company}" criminal charges` -

### Site-Specific Queries
- `site:justice.gov "{name}"` - DOJ press releases
- `site:sec.gov "{name}"` - SEC enforcement actions
- `site:reuters.com "{name}" "{company}" fraud` - Reuters news
- `site:nytimes.com "{name}" "{company}" arrested` - NY Times

## Source Reliability

| Source | Reliability | Notes |
|--------|-------------|-------|
| justice.gov | High | Official DOJ press releases |
| sec.gov | High | Official SEC enforcement actions |
| reuters.com | High | Factual reporting, verified info |
| nytimes.com | High | Major newspaper, fact-checked |
| wsj.com | High | Financial focus, verified |
| bloomberg.com | High | Financial/business news |

## Fraud Indicators

### High Confidence Keywords
- "sentenced"
- "convicted"
- "guilty"
- "prison"
- "pleaded guilty"
- "federal prison"

### Medium Confidence Keywords
- "indicted"
- "charged"
- "arrested"
- "SEC charges"
- "fraud allegations"
- "criminal charges"

## Search Notes by Person

### Charlie Javice (2019, Frank) - FOUND IN DATASET (Row 3364)
- **Best query**: `"Charlie Javice" "Frank" fraud convicted sentenced`
- **Source**: justice.gov, NBC News, ABC News, BBC
- **Result**: Convicted wire/bank/securities fraud. Sentenced 85 months prison (Sep 2025). JPMorgan Chase $175M fraud.
- **Notes**: DOJ press release was first result, AI Overview provided clear summary

### Sam Bankman-Fried (2021, FTX) - FOUND IN DATASET (Row 4752)
- **Best query**: `"Sam Bankman-Fried" "FTX" fraud convicted sentenced`
- **Source**: justice.gov, NPR, ABC News, Wikipedia
- **Result**: Convicted fraud/conspiracy. Sentenced 25 years prison (Mar 2024). FTX collapse, $8B+ customer losses.
- **Notes**: DOJ was first result, extensive video coverage also available

### Caroline Ellison (2022, Alameda Research) - NOT IN DATASET
- **Status**: Not found in Forbes 30 Under 30 dataset
- **Expected**: Cooperating witness, sentenced to 2 years prison

### Elizabeth Holmes (Theranos) - NOT IN DATASET
- **Status**: Not found in Forbes 30 Under 30 dataset
- **Notes**: Morning Brew confirms she never made the Forbes 30 Under 30 list

### Martin Shkreli (2013, MSMB Capital) - FOUND IN DATASET (Row 106)
- **Best query**: `"Martin Shkreli" fraud convicted sentenced prison`
- **Source**: justice.gov, NPR, PBS, Wikipedia
- **Result**: Convicted securities fraud/conspiracy. Sentenced 7 years prison (Mar 2018). Released May 2022.
- **Notes**: Also known as "Pharma Bro", banned from pharmaceutical industry for life

### Gökçe Güven (2025, Kalder) - FOUND IN DATASET (Row 7227)
- **Best query**: `Forbes "30 Under 30" fraud convicted sentenced prison` (discovered via news)
- **Source**: Inc., NewsNation, The Telegraph, Yahoo
- **Result**: CHARGED (NOT CONVICTED) with wire fraud, securities fraud, aggravated identity theft (Jan 2026). Faces up to 52 years if convicted.
- **Notes**: Trial pending - marked as uncertain case

### Nate Paul (2016, World Class Capital Group) - FOUND IN DATASET (Row 1382)
- **Best query**: `"Nate Paul" "World Class Capital" fraud charged convicted`
- **Source**: bizjournals.com, bisnow.com, wrenews.com, thestreet.com
- **Result**: Pleaded guilty to bank fraud (Jan 2025). Sentenced to 4 months home confinement, 5 years supervised release, $1M fine (Apr 2025).
- **Notes**: Connected to Ken Paxton scandal, FBI raid in 2019

### Cody R. Wilson (2014, Defense Distributed) - FOUND IN DATASET (Row 711)
- **Best query**: `"Cody Wilson" "Defense Distributed" convicted sentenced`
- **Source**: kut.org, everytown.org, spectrumnews.com, theverge.com
- **Result**: Sentenced 7 years probation for sexual assault of minor (Sep 2019). Registered sex offender.
- **Notes**: NOT a fraud case - sex crime. 3D-printed gun pioneer. Pleaded guilty to injury to a child.

### Joanna Smith-Griffin (2021, AllHere Education) - FOUND IN DATASET (Row 4623)
- **Best query**: `"Joanna Smith-Griffin" "AllHere" fraud arrested charged`
- **Source**: justice.gov, LA Times, Axios, WUNC
- **Result**: CHARGED (NOT CONVICTED) with securities/wire fraud, identity theft (Nov 2024). Alleged $10M investor fraud.
- **Notes**: Trial pending - marked as uncertain case. AI/EdTech startup.

---
## Comprehensive List of Confirmed Fraud Cases

| Name | Year | Company | Crime | Sentence |
|------|------|---------|-------|----------|
| Martin Shkreli | 2013 | MSMB Capital | Securities fraud, conspiracy | 7 years (released 2022) |
| Cody R. Wilson | 2014 | Defense Distributed | Sexual assault of minor* | 7 years probation |
| Nate Paul | 2016 | World Class Capital | Bank fraud | 4 months home confinement |
| Charlie Javice | 2019 | Frank | Wire/bank/securities fraud | 85 months |
| Sam Bankman-Fried | 2021 | FTX | Fraud (7 counts) | 25 years |

*Note: Cody R. Wilson was convicted of a sex crime, not fraud, but included for completeness.

## Pending Cases (Charged, Not Convicted)

| Name | Year | Company | Charges | Status |
|------|------|---------|---------|--------|
| Joanna Smith-Griffin | 2021 | AllHere Education | Securities/wire fraud, identity theft | Trial pending |
| Gökçe Güven | 2025 | Kalder | Wire fraud, securities fraud, identity theft | Trial pending |

---
## Processing Notes

- Always include name AND company to reduce false positives
- Verify Forbes 30 Under 30 connection in results
- Check criminal activity date is after their Forbes award year
- Wait 3-5 seconds between searches for rate limiting
