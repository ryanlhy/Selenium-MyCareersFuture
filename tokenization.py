import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

qualification_list = ['diploma']
tech_stack = ['react','reactjs','react.js','javascript', 'nodejs','node.js','sql','mongodb','html', 'html5','css', 'css3','bootstrap','jquery','python', 'django',]
title_list = ['software engineer', 'software developer', 'software programmer', 'front-end devloper', 'front-end engineer', 'front-end programmer','frontend developer', 'frontend engineer', 'frontend programmer', 'fullstack developer', 'fullstack engineer', 'fullstack programmer', 'web developer', 'web engineer', 'web programmer']
junior_title_list = ['junior software engineer', 'junior software developer', 'junior software programmer', 'junior front-end devloper', 'junior front-end engineer', 'junior front-end programmer','junior frontend developer', 'junior frontend engineer', 'junior frontend programmer', 'junior fullstack developer', 'junior fullstack engineer', 'junior fullstack programmer', 'junior web developer', 'junior web engineer', 'junior web programmer']
general_keywords = ['web application', 'github']
work_arragements = ['hybrid','remote']
keyword_list = qualification_list + tech_stack + junior_title_list + title_list + general_keywords

negative_list = ['']
noted_keyword = ['mobile developer', 'mobile engineer', 'mobile programmer', 'ios developer', 'ios engineer', 'ios programmer', 'android developer', 'android engineer', 'android programmer']

def extract_keywords(job_listing):
    # Tokenize the job listing text into individual words
    words = word_tokenize(job_listing)

    # Remove stopwords (common words like 'and', 'the', 'in')
    stop_words = set(stopwords.words('english'))
    words = [word.lower() for word in words if word.lower() not in stop_words]

    # Perform any additional pre-processing if required (e.g., stemming, lemmatization)

    # Check for the presence of specific words
    keywords = [word for word in words if word in keyword_list]
    keywords = list(dict.fromkeys(keywords))
    return keywords

job_listing_text = """
Your job listing text goes here. react

"""
keywords = extract_keywords(job_listing_text)
# print(keywords)