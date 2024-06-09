import os
from crewai import Crew,Process
from textwrap import dedent
from langchain_anthropic import ChatAnthropic
from agents import CvCrewAgents,LinkedinCrewAgents
from tasks import CvCrewTasks,LinkedinCrewTasks
from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import BedrockChat
from langchain_core.runnables import ConfigurableField

load_dotenv(find_dotenv(), override=True)

_model_kwargs = {
    "temperature": float(os.getenv("BEDROCK_CLAUDE_TEMPERATURE", "0.1")),
    "top_p": float(os.getenv("BEDROCK_CLAUDE_TOP_P", "1")),
    "top_k": int(os.getenv("BEDROCK_CLAUDE_TOP_K", "250")),
    "max_tokens": int(os.getenv("BEDROCK_CLAUDE_MAX_TOKENS_TO_SAMPLE", "300")),
}


#Models

chatgpt4= ChatOpenAI(
    model="gpt-4",
    api_key=os.getenv("OPENAI_API_KEY")
)

claude_3_opus = BedrockChat(
    model_id="anthropic.claude-3-opus-20240307-v1:0",
    region_name="us-east-1",
    model_kwargs=_model_kwargs
)

claude_3_haiku = BedrockChat(
    model_id="anthropic.claude-3-haiku-20240307-v1:0",
    region_name="us-east-1",
    model_kwargs=_model_kwargs
)

llama_3_8b = ChatOpenAI(
    model="crewai-llama3-8b",
    base_url="http://localhost:11434/v1",
    api_key="NA"
        )

        
"""
Okay so here is were we compose our crew,
This is where we assign the agents to the tasks we want them to perform on

in the crews parameter, you can specify the process, verbose, and manager_llm
process can be sequential or hierarchical
i haven't managed to make the hierarchical work,
so just use sequential


"""







class CvCrew:
    def __init__(self,cv):
        self.cv =cv

    def run(self):

        agents = CvCrewAgents()
        tasks = CvCrewTasks()

 

        #information retriever agents
        cv_analyzer_agent = agents.cv_analyzer_agent(self.cv)
        cv_verifier_agent = agents.cv_verifier_agent(self.cv)


        #CV Tasks
        cv_analysis_task=tasks.cv_analysis_task(self.cv,cv_analyzer_agent)
        cv_verification_task=tasks.cv_verification_task(self.cv,cv_verifier_agent)

        #CvCrew
        cv_crew = Crew(
            agents=[

               cv_analyzer_agent,
               cv_verifier_agent
           
         
            ],
            tasks=[

                cv_analysis_task,
                cv_verification_task

            ],
            verbose=True,
            process=Process.sequential,
            manager_llm= claude_3_haiku,
        )

        result_cv_crew = cv_crew.kickoff()
        return result_cv_crew

class LinkedinCrew:
    def __init__(self,name,linkedin_experience,linkedin_skills, linkedin_education,
                 linkedin_certifications,linkedin_languages,
                 linkedin_recommendations,linkedin_courses,
                 linkedin_organizations,linkedin_volunteering,linkedin_activity,linkedin_comments,commented_cv_path):
        
        self.name = name
        self.linkedin_experience = linkedin_experience
        self.linkedin_skills = linkedin_skills
        self.linkedin_education = linkedin_education
        self.linkedin_certifications =  linkedin_certifications
        self.linkedin_languages = linkedin_languages
        self.linkedin_recommendations = linkedin_recommendations
        self.linkedin_courses = linkedin_courses
        self.linkedin_organizations = linkedin_organizations
        self.linkedin_volunteering = linkedin_volunteering
        self.linkedin_activity = linkedin_activity
        self.linkedin_comments = linkedin_comments
        self.commented_cv_path = commented_cv_path
        
    def run(self):

        

        agents = LinkedinCrewAgents()
        tasks =  LinkedinCrewTasks()

        """
        Agents
        """
        #linkedin Analyst agents
        linkedin_experience_analyzer_agent=agents.linkedin_experience_analyzer_agent(self.linkedin_experience)
        linkedin_skills_analyzer_agent=agents.linkedin_skills_analyzer_agent(self.linkedin_activity)
        linkedin_education_analyzer_agent=agents.linkedin_education_analyzer_agent(self.linkedin_education)
        linkedin_languages_analyzer_agent=agents.linkedin_languages_analyzer_agent(self.linkedin_languages)
        linkedin_recommendations_analyzer_agent=agents.linkedin_recommendations_analyzer_agent(self.linkedin_recommendations)
        linkedin_courses_analyzer_agent=agents.linkedin_courses_analyzer_agent(self.linkedin_courses)
        linkedin_organizations_analyzer_agent=agents.linkedin_organizations_analyzer_agent(self.linkedin_organizations)
        linkedin_volunteering_analyzer_agent=agents.linkedin_volunteering_analyzer_agent(self.linkedin_volunteering)
        linkedin_activity_analyzer_agent=agents.linkedin_activity_analyzer_agent(self.linkedin_activity)
        linkedin_comments_analyzer_agent=agents.linkedin_comments_analyzer_agent(self.linkedin_comments)
        linkedin_certification_analyzer_agent=agents.linkedin_certification_analyzer_agent(self.linkedin_certifications)

        #Linkedin_summary_agent
        sumarizer_agent=agents.sumarizer_agent()
        
        #Enrichement_verifier_agent
        enrichment_verifier_agent=agents.enrichment_verifier_agent()

        

       

        """
        Tasks
        """


        #Linkedin Tasks

        #Analysis
        linkedin_experience_analysis_task=tasks.linkedin_experience_analysis_task(linkedin_experience_analyzer_agent,self.linkedin_experience,self.commented_cv_path,self.name)
        linkedin_skills_analysis_task=tasks.linkedin_skills_analysis_task(linkedin_skills_analyzer_agent,self.linkedin_skills,self.commented_cv_path,self.name)
        linkedin_education_analysis_task=tasks.linkedin_education_analysis_task(linkedin_education_analyzer_agent,self.linkedin_education,self.commented_cv_path,self.name)
        linkedin_certification_analysis_task=tasks.linkedin_certification_analysis_task(linkedin_certification_analyzer_agent,self.linkedin_certifications,self.commented_cv_path,self.name)
        linkedin_languages_analysis_task=tasks.linkedin_languages_analysis_task(linkedin_languages_analyzer_agent,self.linkedin_languages,self.commented_cv_path,self.name)
        linkedin_recommendations_analysis_task=tasks.linkedin_recommendations_analysis_task(linkedin_recommendations_analyzer_agent,self.linkedin_recommendations,self.commented_cv_path,self.name)
        linkedin_courses_analysis_task=tasks.linkedin_courses_analysis_task(linkedin_courses_analyzer_agent,self.linkedin_courses,self.commented_cv_path,self.name)
        linkedin_organizations_analysis_task=tasks.linkedin_organization_analysis_task(linkedin_organizations_analyzer_agent,self.linkedin_organizations,self.commented_cv_path,self.name)
        linkedin_volunteering_analysis_task=tasks.linkedin_volunteering_analysis_task(linkedin_volunteering_analyzer_agent,self.linkedin_volunteering,self.commented_cv_path,self.name)
        linkedin_activity_analysis_task=tasks.linkedin_activity_analysis_task(linkedin_activity_analyzer_agent,self.linkedin_activity,self.commented_cv_path,self.name)
        linkedin_comments_analysis_task=tasks.linkedin_comments_analysis_task(linkedin_comments_analyzer_agent,self.linkedin_comments,self.commented_cv_path,self.name)



        #commenting
        linkedin_summary_task=tasks.linkedin_summary_task(sumarizer_agent,self.name,self.commented_cv_path)  
        cv_enrichement_task=tasks.cv_enrichment_task(sumarizer_agent)                            
        enrichment_verification_task=tasks.enrichment_verification_task(enrichment_verifier_agent,self.commented_cv_path,self.name)



    



        #Define your custom Crew here
        linkedin_crew = Crew(
            agents=[


                linkedin_experience_analyzer_agent,
                linkedin_skills_analyzer_agent,
                linkedin_education_analyzer_agent,
                linkedin_languages_analyzer_agent,
                linkedin_recommendations_analyzer_agent,
                linkedin_courses_analyzer_agent,
                linkedin_organizations_analyzer_agent,
                linkedin_volunteering_analyzer_agent,
                linkedin_activity_analyzer_agent,
                linkedin_comments_analyzer_agent,
                linkedin_certification_analyzer_agent,

                sumarizer_agent,
                enrichment_verifier_agent
               

                
            ],
            tasks=[
           linkedin_experience_analysis_task,
           linkedin_skills_analysis_task,
           linkedin_education_analysis_task,
           linkedin_certification_analysis_task,
           linkedin_languages_analysis_task,
           linkedin_recommendations_analysis_task,
           linkedin_courses_analysis_task,
           linkedin_organizations_analysis_task,
           linkedin_volunteering_analysis_task,
           linkedin_activity_analysis_task,
           linkedin_comments_analysis_task,

           linkedin_summary_task,
           enrichment_verification_task,
           cv_enrichement_task,
           
         
            ],
            verbose=True,
            process=Process.sequential,
            manager_llm= claude_3_haiku
        )

        result = linkedin_crew.kickoff()
        return result
    