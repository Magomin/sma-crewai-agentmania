import os
from crewai import Crew,Process
from textwrap import dedent
from langchain_anthropic import ChatAnthropic
from agents import InformationAnalystAgents,InformationRetrieverAgents
from tasks import CvTasks,LinkedinTasks,EnrichementTasks,ComparaisonTasks
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
        

class MyCrew:
    def __init__(self,cv,json,output_filename):
        self.cv =cv
        self.json = json
        self.output_filename= output_filename
    def run(self):

        

        agents = (InformationRetrieverAgents(),InformationAnalystAgents())
        tasks =  (CvTasks(),LinkedinTasks(),ComparaisonTasks(),EnrichementTasks())

        """
        Agents
        """
        #information retriever agents
        cv_info_retriever_agent = agents[0].cv_info_retriever_agent(self.cv)
        linkedin_info_retriever_agent=agents[0].linkedin_info_retriever_agent(self.json)

        #Information analyst agents
        cv_information_analyst_agent=agents[1].cv_information_analyst_agent()
        linkedin_information_analyst_agent=agents[1].linkedin_information_analyst_agent()
        information_comparaison_agent=agents[1].information_comparaison_agent()
        enrichement_agent=agents[1].enrichement_agent()
       

        """
        Tasks
        """

        #CV Tasks
        get_cvprofile_task=tasks[0].get_cvprofile_task(cv_info_retriever_agent,self.cv)
        comment_cv_task=tasks[0].comment_cv_task(cv_info_retriever_agent,[get_cvprofile_task])

        #Linkedin Tasks
        get_linkedin_profile_task=tasks[1].get_linkedin_profile_task(linkedin_info_retriever_agent,self.json,[comment_cv_task])
        comment_linkedin_profile_task=tasks[1].comment_linkedin_profile_task(linkedin_information_analyst_agent,[get_linkedin_profile_task])

        #Comparaison Tasks
        compare_cv_linkedin_comments_task=tasks[2].compare_cv_linkedin_comments_task(information_comparaison_agent,[comment_cv_task,comment_linkedin_profile_task])
        social_media_analysis_task=tasks[2].social_media_analysis_task(information_comparaison_agent,[comment_linkedin_profile_task,compare_cv_linkedin_comments_task])

        #Enrichement Tasks
        enrichement_task=tasks[3].enrichement_task(enrichement_agent,[compare_cv_linkedin_comments_task,social_media_analysis_task],self.output_filename)
        




        #Define your custom Crew here
        crew = Crew(
            agents=[

               cv_info_retriever_agent,
               linkedin_info_retriever_agent,
               cv_information_analyst_agent,
               linkedin_information_analyst_agent,
               information_comparaison_agent,
               enrichement_agent
                
            ],
            tasks=[

                get_cvprofile_task,
                comment_cv_task,
                get_linkedin_profile_task,
                comment_linkedin_profile_task,
                compare_cv_linkedin_comments_task,
                social_media_analysis_task,
                enrichement_task,
           
            ],
            verbose=True,
            process=Process.sequential,
            manager_llm= claude_3_haiku
        )

        result = crew.kickoff()
        return result
    





# if __name__ == "__main__":

    
#     cv= r"C:\Users\domin\Desktop\sma-crewai-agentmania\Cv Matthieu Dominguez Business developer.pdf"
    

#     mycrew = MyCrew(cv)
#     result = mycrew.run()
#     print(result)


  

        