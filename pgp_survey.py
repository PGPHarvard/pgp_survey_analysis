"""Code useful for interpreting Personal Genome Project surveys

Classes:
    SurveyData: contains survey data from PGP survey

Methods:
    get_trait_surveys: find and parse trait surveys
    get_participant_survey: parse participant survey file
"""

import csv
import os
import re


this_dir = os.path.dirname(os.path.abspath(__file__))
TRAITS_FILE = os.path.join(this_dir, 'PGP_trait_list.txt')


def _latest_matching_file(regex_string, directory='.'):
    """Find most recently edited filename matching regex in directory."""
    local_filenames = os.listdir(directory)
    all_matches = []
    for filename in local_filenames:
        if re.match(regex_string, filename):
            all_matches.append(os.path.join(directory, filename))
    if all_matches:
        return max(all_matches, key=lambda x: os.stat(x).st_mtime)
    else:
        return None


class SurveyData():
    """PGP Survey Data from Google Spreadsheets

    Data attributes:
    by_huID:       Key is huID (str), value is results (array of str).
                    Results exclude timestamp and participant indentifiers.
    header_titles: Header titles for results (array of str)
    sourcefile:    Path to file that was parsed to create this object.

    Methods:
    get_huIDs:            Return huIDs that completed survey (set of str)
    get_latest_responses: Return most recent set of survey responses.
    get_

    """
    by_huID = dict()
    header_titles = []
    sourcefile = ''

    def __init__(self, filepath):
        self.by_huID = dict()
        self.sourcefile = filepath
        file_input = open(filepath)
        file_data = csv.reader(file_input)
        header_data = file_data.next()
        self.header_titles = [header_data[1]] + header_data[3:]
        for row in file_data:
            huID = row[0]
            # Assumes that the file is sorted chronologically.
            # Data for a given huID is stored with the most recent first.
            if huID in self.by_huID:
                self.by_huID[huID].insert(0, [row[1]] + row[3:])
            else:
                self.by_huID[huID] = [[row[1]] + row[3:]]

    def __repr__(self):
        return 'SurveyData from ' + self.sourcefile

    def get_huIDs(self):
        """Returns (set): all huIDs that have completed the survey."""
        hu_IDs = set(self.by_huID.keys())
        return hu_IDs

    def get_latest_responses(self, huID):
        """Returns (list): most recent survey response for an huID."""
        if huID in self.by_huID:
            return self.by_huID[huID][0]
        else:
            return None

    def get_responses(self, huID):
        """Returns (list of lists): all survey responses for an huID."""
        if huID in self.by_huID:
            return self.by_huID[huID]
        else:
            return None


def get_trait_surveys(directory='.'):
    """Returns tuple containing trait surveys list and possible traits lists.

    [0]: An array of SurveyData objects containing data from each of the 
         trait surveys.
    [1]: An array of arrays of str, one for each trait survey in [0].
         Each array lists the traits covered by that survey.
    """

    # Find the most recent survey files, which should match the regexps below.
    surveys_regexps = [
        r'^PGPTrait&DiseaseSurvey2012-Cancers-[0-9]{14}.csv$',
        r'^PGPTrait&DiseaseSurvey2012-Endocrine,Metabolic,Nutritional,And' +
         'Immunity-[0-9]{14}.csv$',
        r'^PGPTrait&DiseaseSurvey2012-Blood-[0-9]{14}.csv$',
        r'^PGPTrait&DiseaseSurvey2012-NervousSystem-[0-9]{14}.csv$',
        r'^PGPTrait&DiseaseSurvey2012-VisionAndHearing-[0-9]{14}.csv$',
        r'^PGPTrait&DiseaseSurvey2012-CirculatorySystem-[0-9]{14}.csv$',
        r'^PGPTrait&DiseaseSurvey2012-RespiratorySystem-[0-9]{14}.csv$',
        r'^PGPTrait&DiseaseSurvey2012-DigestiveSystem-[0-9]{14}.csv$',
        r'^PGPTrait&DiseaseSurvey2012-GenitourinarySystems-[0-9]{14}.csv$',
        r'^PGPTrait&DiseaseSurvey2012-SkinAndSubcutaneousTissue-[0-9]{14}.csv$',
        r'^PGPTrait&DiseaseSurvey2012-MusculoskeletalSystemAndConnective' + \
            'Tissue-[0-9]{14}.csv$',
        r'^PGPTrait&DiseaseSurvey2012-CongenitalTraitsAndAnomalies' + \
            '-[0-9]{14}.csv$',
        ]    
    survey_files = [_latest_matching_file(x, directory) for 
                    x in surveys_regexps]
    assert not [x for x in survey_files if not x], \
        "Can't find files for all trait surveys. Check that you have files " + \
        "matching all items in this regex list: \n" + '\n'.join(surveys_regexps)
    surveys = [SurveyData(x) for x in survey_files]

    # Read the list of all possible traits, available in another text file.
    survey_traits = [list() for x in range(len(surveys_regexps))]
    traits_file = open(TRAITS_FILE)
    # Find which traits are in each trait survey.
    for line in traits_file:
        data = line.strip().split('\t')
        index = [x for x in range(len(surveys_regexps)) if 
                 re.search(data[1], survey_files[x])][0]
        survey_traits[index].append(data[0])

    return (surveys, survey_traits)


def get_participant_survey(directory='.'):
    """Find and return the PGP participant survey (SurveyData)."""
    survey_regex = r'PGPParticipantSurvey-[0-9]{14}.csv'
    survey_file = _latest_matching_file(survey_regex, directory)
    survey = SurveyData(survey_file)
    return survey
