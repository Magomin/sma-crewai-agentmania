from pydantic import BaseModel,Field
from typing import List




#CV Classes
class CVProfile(BaseModel):
    name: str = Field(..., description="The name of the CV owner")
    cv_experience: str = Field(..., description="The work experience of the CV owner")
    cv_skills: str = Field(..., description="The skills of the CV owner")
    cv_education: str = Field(..., description="The education of the CV owner")
    cv_languages: str = Field(..., description="The languages that the CV owner speaks")

class CommentedCV(CVProfile):
    commented_cv_experience: str = Field(..., description="The work experience commented")
    commented_cv_education: str = Field(..., description="The education commented")
    commented_cv_skills: str = Field(..., description="Commented skills")
    commented_cv_languages: str = Field(..., description="Commented languages")

# Linkedin classes
class LinkedinProfile(CommentedCV):
    linkedin_experience: str = Field(..., description="The experience found on the LinkedIn profile")
    linkedin_education: str = Field(..., description="The education found on the LinkedIn profile")
    linkedin_skills: str = Field(..., description="The skills found on the LinkedIn profile")
    linkedin_languages: str = Field(..., description="The languages found on the LinkedIn profile")
    linkedin_recommendations: str = Field(..., description="The recommendations found on the LinkedIn profile")
    linkedin_certifications: str = Field(..., description="The certifications found on the LinkedIn profile")
    linkedin_volunteering: str = Field(..., description="The volunteering experience found on the LinkedIn profile")
    linkedin_course: str = Field(..., description="The courses found on the LinkedIn profile")
    linkedin_activity: str = Field(..., description="The activity found on the LinkedIn profile")
    linkedin_comments: str = Field(..., description="Additional comments on the LinkedIn profile")

class CommentedLinkedin(LinkedinProfile):
    commented_linkedin_experience: str = Field(..., description="Comments on the LinkedIn experience")
    commented_linkedin_education: str = Field(..., description="Comments on the LinkedIn education")
    commented_linkedin_skills: str = Field(..., description="Comments on the LinkedIn skills")
    commented_linkedin_languages: str = Field(..., description="Comments on the LinkedIn languages")
    commented_linkedin_recommendations: str = Field(..., description="Comments on the LinkedIn recommendations")
    commented_linkedin_certifications: str = Field(..., description="Comments on the LinkedIn certifications")
    commented_linkedin_volunteering: str = Field(..., description="Comments on the LinkedIn volunteering experience")
    commented_linkedin_course: str = Field(..., description="Comments on the LinkedIn courses")
    commented_linkedin_activity: str = Field(..., description="Comments on the LinkedIn activity")
    commented_linkedin_comments: str = Field(..., description="Additional comments on the LinkedIn profile")

# Comparaison class
class Comparaison(CommentedLinkedin):
    experience_compared: str = Field(..., description="Comparison of the experience between CV and LinkedIn")
    education_compared: str = Field(..., description="Comparison of the education between CV and LinkedIn")
    skills_compared: str = Field(..., description="Comparison of the skills between CV and LinkedIn")
    languages_compared: str = Field(..., description="Comparison of the languages between CV and LinkedIn")

class SocialMediaAnalysis(Comparaison):
    extra: str = Field(...,description="Summary of the extra information provided by the linkedin profile, the recommendation, certification, volunteering, course") 
    behaviour: str = Field(...,description="an Analysis of the online behaviour, it's activity what the owner of the linkedin profile comments on")

#Enrichementc class
class CVEnrichement(Comparaison):
    cv_enrichement: str = Field(..., description="Enrichment information for the CV")


