from crewai import Task
from pydantic_models import CVProfile,CommentedCV,LinkedinProfile,CommentedLinkedin,Comparaison,CVEnrichement,SocialMediaAnalysis
from textwrap import dedent


class CvTasks:

    def __tip_section(self):
        return "if you do your BEST WORK, I'll give you a $10 000 commission!"

    def get_cvprofile_task(self, agent, cv):
        return Task(
            description=dedent(
            f"""
        **Task**: extract the text of {cv}, and provide clasify the education, experience, skills, languages in a pydanticfile called {CVProfile}

        **Description**: get the text that is stored inside the{cv}, then clasify the different section of the {cv} education, experience, skills and languages in the 
        {CVProfile}
        
        
        **Parameters**:
        - Cv: {cv}
        - pydanticfile: {CVProfile}

        **Note**:{self.__tip_section()}
    """

        ),
        expected_output=(
            f"""
        The {cv} text extracted and formatted into the {CVProfile} format. The Pydantic model should look something like this:

        Example:

        [
            
                        "name": "Sample Name",
                        "cv_experience": "Sample experience description.",
                        "cv_skills": "Sample skills description.",
                        "cv_education": "Sample education details.",
                        "cv_languages": "Sample languages description."
            
        ]

        
        """
        ),
        
        agent=agent,
        async_exectution=True
        

        )
    
    def comment_cv_task(self, agent, context):
        return Task(

            description=dedent(
                f"""
                **Task**: Comment on the fields of the {CVProfile} outputted by the previous task {context} and output your comments in a new Pydantic model called {CommentedCV}.

                **Description**: Your comments must be observations of the experience, education, skills, and languages found in the {CVProfile}. Analyze the details and provide insightful feedback or notes that would be useful from an HR specialist's perspective.

                **Parameters**:
                - CVProfile: {CVProfile}
                - CommentedCV: {CommentedCV}

                **Note**: {self.__tip_section()}
                """
            ),
            expected_output=(
                f"""
                The Pydantic object {CommentedCV} should look like this:

                Example:


                CommentedCV:
                [
                
                    "name": "Sample Name",
                    "cv_experience": "Sample experience description.",
                    "commented_cv_experience": "Sample commented experience.",
                    "cv_skills": "Sample skills description.",
                    "commented_cv_skills": "Sample commented skills.",
                    "cv_education": "Sample education details.",
                    "commented_cv_education": "Sample commented education.",
                    "cv_languages": "Sample languages description.",
                    "commented_cv_languages": "Sample commented languages."
                    
                ]
                """
            ),
            agent=agent,
            context=context,
            async_exectution=True,
    )
    
class LinkedinTasks:

    def __tip_section(self):
        return "if you do your BEST WORK, I'll give you a $10 000 commission!"


    def get_linkedin_profile_task(self, agent, linkedin_json,context):
        return Task(
            description=dedent(
                f"""
                **Task**: Extract the information from the LinkedIn profile stored as JSON ({linkedin_json}) and parse it into a Pydantic model called {LinkedinProfile}.

                **Description**: Retrieve the JSON data representing a LinkedIn profile and map the relevant fields to the {LinkedinProfile} Pydantic model. Ensure that the extracted information is accurately reflected in the corresponding fields of the model.

                **Parameters**:
                - linkedin_json: The JSON data containing the LinkedIn profile information.
                - LinkedinProfile: {LinkedinProfile}

                **Note**: {self.__tip_section()}
                """
            ),
            expected_output=(
                f"""
                The Pydantic object {LinkedinProfile} should look like this:

                    Example:

                    LinkedinProfile:
                    [
                        
                        "name": "Sample Name",
                        "cv_experience": "Sample experience description.",
                        "commented_cv_experience": "Sample commented experience.",
                        "cv_skills": "Sample skills.",
                        "commented_cv_skills": "Sample commented skills.",
                        "cv_education": "Sample education details.",
                        "commented_cv_education": "Sample commented education details.",
                        "cv_languages": "Sample languages.",
                        "commented_cv_languages": "Sample commented languages.",
                        "linkedin_experience": "Sample LinkedIn experience.",
                        "linkedin_education": "Sample LinkedIn education details.",
                        "linkedin_skills": "Sample LinkedIn skills.",
                        "linkedin_languages": "Sample LinkedIn languages.",
                        "linkedin_recommendations": "Sample LinkedIn recommendations.",
                        "linkedin_certifications": "Sample LinkedIn certifications.",
                        "linkedin_volunteering": "Sample LinkedIn volunteering details.",
                        "linkedin_course": "Sample LinkedIn course details.",
                        "linkedin_activity": "Sample LinkedIn activity.",
                        "linkedin_comments": "Sample LinkedIn comments."
                        
                    ]
                    """
                ),
                agent=agent,
                context=context,
                async_exectution=True
                
            )

    def comment_linkedin_profile_task(self, agent,context):
            
            return Task(
                description=dedent(
                    f"""
                    **Task**: Comment on the fields of the {LinkedinProfile} created in the previous task ({context}) and output your comments in a new Pydantic model called {CommentedLinkedin}.

                    **Description**: Analyze the details from the {LinkedinProfile} and provide insightful feedback or notes for each section. Your comments should reflect observations that would be useful from an HR specialist's perspective.

                    **Parameters**:
                    - linkedin_profile: {LinkedinProfile}
                    - CommentedLinkedin: {CommentedLinkedin}

                    **Note**: {self.__tip_section()}
                    """
                ),
                expected_output=(
                    f"""
                    the expected output is the pydantic object fullfield, 
                    The Pydantic object {CommentedLinkedin} should look like this:

                    Example:


                    CommentedLinkedin:
                    [
                        
                        "name": "Sample Name",
                        "cv_experience": "Sample experience description.",
                        "commented_cv_experience": "Sample commented experience.",
                        "cv_skills": "Sample skills.",
                        "commented_cv_skills": "Sample commented skills.",
                        "cv_education": "Sample education details.",
                        "commented_cv_education": "Sample commented education details.",
                        "cv_languages": "Sample languages.",
                        "commented_cv_languages": "Sample commented languages.",
                        "linkedin_experience": "Sample LinkedIn experience.",
                        "commented_linkedin_experience": "Sample commented LinkedIn experience.",
                        "linkedin_education": "Sample LinkedIn education details.",
                        "commented_linkedin_education": "Sample commented LinkedIn education details.",
                        "linkedin_skills": "Sample LinkedIn skills.",
                        "commented_linkedin_skills": "Sample commented LinkedIn skills.",
                        "linkedin_languages": "Sample LinkedIn languages.",
                        "commented_linkedin_languages": "Sample commented LinkedIn languages.",
                        "linkedin_recommendations": "Sample LinkedIn recommendations.",
                        "commented_linkedin_recommendations": "Sample commented LinkedIn recommendations.",
                        "linkedin_certifications": "Sample LinkedIn certifications.",
                        "commented_linkedin_certifications": "Sample commented LinkedIn certifications.",
                        "linkedin_volunteering": "Sample LinkedIn volunteering details.",
                        "commented_linkedin_volunteering": "Sample commented LinkedIn volunteering details.",
                        "linkedin_course": "Sample LinkedIn course details.",
                        "commented_linkedin_course": "Sample commented LinkedIn course details.",
                        "linkedin_activity": "Sample LinkedIn activity.",
                        "commented_linkedin_activity": "Sample commented LinkedIn activity.",
                        "linkedin_comments": "Sample LinkedIn comments.",
                        "commented_linkedin_comments": "Sample commented LinkedIn comments."

                    ]
                    """
                ),
                agent=agent,
                context=context,
                async_exectution=True

            )



class ComparaisonTasks:

    def __tip_section(self):
        return "if you do your BEST WORK, I'll give you a $10 000 commission!"

    def compare_cv_linkedin_comments_task(self, agent, context):
        return Task(
            description=dedent(
                f"""
                **Task**: Compare the comments from the {CommentedCV} and {CommentedLinkedin} profiles from the previous tasks ({context}) and output the comparison in a new Pydantic model called {Comparaison}.

                **Description**: Analyze and compare the comments on the experience, education, skills, and languages from both the CV and LinkedIn profiles. Provide a detailed comparison highlighting similarities, differences, and any notable observations.

                **Parameters**:
                - commented_cv: {CommentedCV}
                - commented_linkedin: {CommentedLinkedin}
                - comparaison: {Comparaison}

                **Note**: {self.__tip_section()}
                """
            ),
            expected_output=(
                f"""
                The Pydantic object {Comparaison} should look like this:

                Example:


                Comparaison:
                [
                    
                        "name": "Sample Name",
                        "cv_experience": "Sample experience description.",
                        "commented_cv_experience": "Sample commented experience.",
                        "cv_skills": "Sample skills.",
                        "commented_cv_skills": "Sample commented skills.",
                        "cv_education": "Sample education details.",
                        "commented_cv_education": "Sample commented education details.",
                        "cv_languages": "Sample languages.",
                        "commented_cv_languages": "Sample commented languages.",
                        "linkedin_experience": "Sample LinkedIn experience.",
                        "commented_linkedin_experience": "Sample commented LinkedIn experience.",
                        "linkedin_education": "Sample LinkedIn education details.",
                        "commented_linkedin_education": "Sample commented LinkedIn education details.",
                        "linkedin_skills": "Sample LinkedIn skills.",
                        "commented_linkedin_skills": "Sample commented LinkedIn skills.",
                        "linkedin_languages": "Sample LinkedIn languages.",
                        "commented_linkedin_languages": "Sample commented LinkedIn languages.",
                        "linkedin_recommendations": "Sample LinkedIn recommendations.",
                        "commented_linkedin_recommendations": "Sample commented LinkedIn recommendations.",
                        "linkedin_certifications": "Sample LinkedIn certifications.",
                        "commented_linkedin_certifications": "Sample commented LinkedIn certifications.",
                        "linkedin_volunteering": "Sample LinkedIn volunteering details.",
                        "commented_linkedin_volunteering": "Sample commented LinkedIn volunteering details.",
                        "linkedin_course": "Sample LinkedIn course details.",
                        "commented_linkedin_course": "Sample commented LinkedIn course details.",
                        "linkedin_activity": "Sample LinkedIn activity.",
                        "commented_linkedin_activity": "Sample commented LinkedIn activity.",
                        "linkedin_comments": "Sample LinkedIn comments.",
                        "commented_linkedin_comments": "Sample commented LinkedIn comments."
                    
                ]
                """
            ),
            agent=agent,
            context=context,
            async_exectution=True

        )


    def social_media_analysis_task(self, agent, context):
        return Task(
            description=dedent(
                f"""
                **Task**: Analyze the LinkedIn profile for additional information and online behavior, then output the analysis in a new Pydantic model called {SocialMediaAnalysis}.

                **Description**: Extract and analyze extra information from the LinkedIn profile, such as recommendations, certifications, volunteering, and courses.
                Additionally, provide an analysis of the LinkedIn user's online behavior, including their activities and comments. Summarize this information in the {SocialMediaAnalysis} Pydantic model.

                **Parameters**:
                - comparaison: {Comparaison}

                **Note**: {self.__tip_section()}
                """
            ),
            expected_output=(
                f"""
                The Pydantic object {SocialMediaAnalysis} should look like this:

                Example:



                SocialMediaAnalysis:
                [
                    
                "extra": "Sample extra information from LinkedIn profile.",
                "behaviour": "Sample analysis of online behavior."
                    
                ]
                """
            ),
            agent=agent,
            context=context
        )




class EnrichementTasks:

    def __tip_section(self):
        return "if you do your BEST WORK, I'll give you a $10 000 commission!"

    def enrichement_task(self,agent,context):
        return Task(
            description=dedent(
                  f"""
            **Task**: Summarize how the information extracted from LinkedIn confirms the information in the CV, and add insights on online behavior. Output this summary in a new Pydantic model called {CVEnrichement}.

            **Description**: Using the data from the previous tasks ({context}), create a summary that highlights how the LinkedIn profile information supports and confirms the details in the CV. Include insights on the individual's online behavior, such as their activities, comments, and overall engagement. The summary should provide a comprehensive overview of the individual's qualifications, experience, skills, education, and online presence.

            **Parameters**:
            - CVEnrichement: {CVEnrichement}


            **Note**: {self.__tip_section()}
            """
            ),
            expected_output=dedent(
                f"""\
            a paragraph that highlights the extra information extracted that can be beneficial to add for the current cv

            Example:

            CVEnrichement:
           "cv_enrichement": "The LinkedIn profile corroborates the CV details, highlighting consistent themes in professional experience, education, and skills." 
           "Both sources confirm the individual's expertise and qualifications."
            "Additionally, the individual's active online presence and community engagement provide further evidence of their professional involvement and continuous learning."


                """
            ),
            agent=agent,
            context=context,
            async_exectution=True
        )