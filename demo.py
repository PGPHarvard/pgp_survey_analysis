"""Demo code analyzing PGP Survey data.

Prints to stdout tab-separated data. The first row is a header.
Following lines each lists:
 - participant huID
 - profile URL
 - age (from Participant Survey, if available)
 - sex/gender (from Participant Survey, if available)
 - race/ethnicity (from Participant Survey, if available)
 - all possible traits (239 total as of 2013/02/23)

 Only participants who responded to all trait surveys are reported.
"""

import re
import pgp_survey

SURVEYS_DIRECTORY = 'surveys_20130329'

# Input trait surveys and list of traits.
trait_surveys, trait_survey_traits = pgp_survey.get_trait_surveys(SURVEYS_DIRECTORY)

# Input participant survey.
participant_survey = pgp_survey.get_participant_survey(SURVEYS_DIRECTORY)

# Use splat to get the intersection of sets returned by get_huIDs().
in_all_surveys = trait_surveys[0].get_huIDs().intersection(
    *[x.get_huIDs() for x in trait_surveys])
huID_list = list(in_all_surveys)
huID_list.sort()

# Create a single list of traits from all trait surveys.
traits_flat = []
[traits_flat.extend(x) for x in trait_survey_traits]

# Create and output header.
header = ['huID', 'Profile URL', 'Age', 'Sex/Gender', 
          'Race/Ethnicity'] + traits_flat
print '\t'.join(header)

# Output participant ID and 'Y' for every trait a participant has.
for huID in huID_list:
    url = 'https://my.personalgenomes.org/profile/' + huID
    age = 'Unknown'
    sex = 'Unknown'
    race = 'Unknown'
    if huID in participant_survey.by_huID:
        latest_general_survey = participant_survey.get_latest_responses(huID)
        age = latest_general_survey[1]
        sex = latest_general_survey[13]
        race = latest_general_survey[14]
    huID_traits_flat = []
    for surv_num in range(len(trait_surveys)):
        huID_latest_data = trait_surveys[surv_num].get_latest_responses(huID)
        traits = ['Y' if re.search(re.escape(x), huID_latest_data[1])
                  else '' for x in trait_survey_traits[surv_num]]
        [huID_traits_flat.append(x) for x in traits]
    print '\t'.join([huID, url, age, sex, race] + huID_traits_flat)
