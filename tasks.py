from crewai import Task
from textwrap import dedent






"""
Hey are you following me?
-------------------------

Okay here we define the tasks that the cvcrew and linkedincrew will perform.
you can only assign one agent per task

the task need a description, an expected output, an agent

you can also specify if the task is async or not
async can give you a lot of errors so be careful with that

you can create an output file to store the output, it will output it in the directory
i haven't find a way to specify the path of the output file, maybe by asking it in the task it self?

you can see that i put a tip section,"if you do your BEST WORK, you will get a $10 000 commission!"

apparently, it helps get better results it's complicated to verify but if it helps even a little it will be worth it.



"""

class CvCrewTasks:

    def __tip_section(self):
        return "if you do your BEST WORK, I'll give you a $10 000 commission!"

    
    def cv_analysis_task(self, cv, agent):
        return Task(
            description=dedent(
                f"""
                **Task**: extract the text of {cv}, and analyze the experience, education, skills, and languages.

                **Description**: Get the text that is stored inside the CV, then analyze the sections of the {cv} including experience, education, skills, and languages.

                **Parameters**:
                - Cv: {cv}

                **Note**: {self.__tip_section()}
                """
            ),
            expected_output=dedent(
                f"""
                The {cv} text extracted and analyzed.

                """
            ),
            agent=agent,
            async_execution=False,
        )
    

    def cv_verification_task(self, cv, agent):
        return Task(
            description=dedent(
               f"""
                **Task**:verify that the text of {cv} was correclty extracted and commented by the previous task,
                correct mistake, and improve the overall quality of the previous task

                **Description**: verify and correct the previous task, check if the information of the was completely extracted
                and improve the comments made

                **Parameters**:
                - Cv: {cv}

                **Note**:{self.__tip_section()}
                """
            ),
            expected_output=dedent(
                f"""
                Your expected to improve the previous task output,
              

                """
            ),
            output_file="commented_cv.txt",
            agent=agent,
            async_execution=False,

        )
    

 
    
class LinkedinCrewTasks:

    def __tip_section(self):
        return "if you do your BEST WORK, I'll give you a $10 000 commission!"


    def linkedin_experience_analysis_task(self, agent, linkedin_experience,commented_cv_path,name):
            return Task(
                description=dedent(
                    f"""
                    **Task**: compare {linkedin_experience},  with the experience of the {commented_cv_path}, note the differences.

                    **Description**: provide an comment, on the professional experience of this LinkedIn profile.
                    Ensure that the comment reflects the professional background and career progression of the profile.

                    
                    **Parameters**:
                    -CV: {commented_cv_path}
                    -name: {name} 

                    **Note**: {self.__tip_section()}
                    """
                ),
                expected_output=(
                    f"""
                    Your expected task output is a paragraph that compare the experience section  of the LinkedIn profile. with  {commented_cv_path}

                    Example:
                        [
                        the experience of {name} present on linkedin showcase interesting experience that where not present on the cv such as an internship in Xyz which 
                        could enrich the cv by demonstrating knowledge in areas that he saw during that internship

                        ]
                        or
                        [
                            The experience present on {name}'s linkedin is the same as the cv, nothing to enrich here
                        ]



                    the examples above are just  examples, be sure to replace it with the actual info 

                    """
                ),
                agent=agent,
                async_execution=True,
            )






 
    def linkedin_education_analysis_task(self, agent,linkedin_education,commented_cv_path,name):
         

            return Task(
                  description=dedent(
            
                         f"""
                    **Task**: compare {linkedin_education},  with the education of the {commented_cv_path}, note the differences.

                    **Description**: comment the education of this LinkedIn profile.
                    

                    
                    **Parameters**:
                    -CV: {commented_cv_path}
                    -name:{name} 

                    **Note**: {self.__tip_section()}
                    """
                ),
                expected_output=(
                    f"""
                    Your expected task output is a paragraph that compare the education  section of the LinkedIn profile. with  {commented_cv_path}

                        Example
                        [
                        the education of {name} present on linkedin showcase interesting education that where not present on the cv such as a degree in Xyz which 
                        could enrich the cv

                        ]

                        or

                        [
                        The education present on {name} linkedin is the same as the cv, nothing to enrich here

                        ]

                    the examples above are just  examples, be sure to replace it with the actual info 
                    
                    """
                ),
                agent=agent,
                async_execution=True,
            )
            

    def linkedin_skills_analysis_task(self, agent, linkedin_skills,commented_cv_path,name):
        return Task(
            description=dedent(
                          f"""
                    **Task**: compare {linkedin_skills},  with the skills of the {commented_cv_path}, note the differences.

                    **Description**: comment the skills of this LinkedIn profile.
                    

                    
                    **Parameters**:
                    -name:{name}
                    -CV: {commented_cv_path} 

                    **Note**: {self.__tip_section()}
                    """
                ),
                expected_output=(
                    f"""
                    Your expected task output is a paragraph that compare the skills section of the LinkedIn profile. with  {commented_cv_path}

                    Example:
                        [
                        the skills of {name} present on linkedin showcase interesting skills that where not present on the cv such as 
                        skills in () which could enrich the cv
                        ]

                            or
                        [
                        The skills present on linkedin is the same sas the cv, nothing to enrich here
                        ]

                    the examples above are just  examples, be sure to replace it with the actual info 

                    """
                ),
                agent=agent,
                async_execution=True,
        )


    def linkedin_languages_analysis_task(self, agent, linkedin_languages, commented_cv_path,name):
         return Task(
            description=dedent(
                          f"""
                    **Task**: compare {linkedin_languages},  with the languages of the {commented_cv_path}, note the differences.

                    **Description**: comment the languages of this LinkedIn profile.
                    

                    
                    **Parameters**:
                    -name:{name}
                    -CV: {commented_cv_path} 

                    **Note**: {self.__tip_section()}

                    """
                ),
                expected_output=(
                    f"""
                    Your expected task output is a paragraph that compare the experience section of the LinkedIn profile. with  {commented_cv_path}

                    Example:
                        [
                        {name} linkedin comfirms that he speak the same languages as on its cv
                        ]

                            or
                        [
                        he did not add is language -> leave blank
                        ]

                    the examples above are just  examples, be sure to replace it

                    """
                ),
                agent=agent,
                async_execution=True,

        )
    
    def linkedin_certification_analysis_task(self, agent, linkedin_certification,commented_cv_path,name):
        return Task(
            description=dedent(
                f"""
               **Task**: comment the {linkedin_certification}, and see how they can value to the {commented_cv_path}

              
                    
                **Parameters**:
                -CV: {commented_cv_path} 
                -Name:{name}


                **Note**: {self.__tip_section()}
                """
            ),
            expected_output=(
                f"""
                Your expected task output is a paragraph that comment the certifications section of the LinkedIn profile. And see how they can value to the {commented_cv_path}

                Example:

                    [
                    {name} certifications on linkedin confirms his expertise in the domains mentioned in {commented_cv_path}
                    ]
                    or
                    [
                    {name} doesn't have any certification on his linkedin ->leave blank
                    ]

                the examples above are just  examples, be sure to replace it with the actual info 

                """
            ),
            agent=agent,
            async_execution=True
        )
    

    def linkedin_recommendations_analysis_task(self, agent, linkedin_recommendations, commented_cv_path,name):
        return Task(
            description=dedent(
                f"""
               **Task**: comment the {linkedin_recommendations}, and see how they can value to the {commented_cv_path}

              
                    
                **Parameters**:
                -CV: {commented_cv_path} 
                -name{name}


                **Note**: {self.__tip_section()}
                """
            ),
            expected_output=(
                f"""
                Your expected task output is a paragraph that comment the recommendations section of the LinkedIn profile. And see how they can value to the {commented_cv_path}

                Example:

                    [
                     {name} got recommended in linkedin for his capacities in xyz, which confirms his expertise in the domains mentioned in {commented_cv_path}
                    ]

                    or

                    [
                    {name} doesn't have any recommentation on his linkedin -> leave blank
                    ]

                the examples above are just  examples, be sure to replace it with the actual info 

                """
            ),
            agent=agent,
            async_execution=True
        )
    


    def linkedin_courses_analysis_task(self, agent, linkedin_courses,commented_cv_path,name):
              
            return Task(
            description=dedent(
                f"""
               **Task**: comment the {linkedin_courses}, and see how they can value to the {commented_cv_path}

              
                    
                **Parameters**:
                -CV: {commented_cv_path} 
                -name{name}


                **Note**: {self.__tip_section()}
                """
            ),
            expected_output=(
                f"""
                Your expected task output is a paragraph that comment the courses section of the LinkedIn profile. And see how they can value to the {commented_cv_path}

                Example:

                    [
                     {name}'s linkedin  show that he took courses in xyz, which confirms his expertise in the domains mentioned in {commented_cv_path}
                    ]

                    or

                    [
                    {name} doesn't have any course on his linkedin -> leave blank
                    ]

                the examples above are just  examples, be sure to replace it with the actual info 

                """
            ),
            agent=agent,
            async_execution=True
        )
    



    def linkedin_organization_analysis_task(self, agent, linkedin_organisation,commented_cv_path,name):
            return Task(
            description=dedent(
                f"""
               **Task**: comment the {linkedin_organisation}, and see how they can value to the {commented_cv_path}

              
                    
                **Parameters**:
                -CV: {commented_cv_path} 
                -name{name}


                **Note**: {self.__tip_section()}
                """
            ),
            expected_output=(
                f"""
                Your expected task output is a paragraph that comment the organization section of the LinkedIn profile. And see how they can value to the {commented_cv_path}

                Example:

                    [
                     {name}'s linkedin  show that he was/is part of organisation, xyz, which confirms his expertise in the domains mentioned in {commented_cv_path}
                    ]

                    or

                    [
                    {name} doesn't have any course on his linkedin -> leave blank
                    ]

                the examples above are just  examples, be sure to replace it with the actual info 

                """
            ),
            agent=agent,
            async_execution=True
        )
    

    def linkedin_volunteering_analysis_task(self, agent, linkedin_volunteering,commented_cv_path,name): 
            return Task(
            description=dedent(
                f"""
               **Task**: comment the {linkedin_volunteering}, and see how they can value to the {commented_cv_path}

              
                    
                **Parameters**:
                -CV: {commented_cv_path} 
                -name{name}


                **Note**: {self.__tip_section()}
                """
            ),
            expected_output=(
                f"""
                Your expected task output is a paragraph that comment the volunteering section of the LinkedIn profile. And see how they can value to the {commented_cv_path}

                Example:

                    [
                     {name}'s linkedin  show that he was a volunteer in xyz, which confirms his expertise in the domains mentioned in {commented_cv_path}
                    ]

                    or

                    [
                    {name} doesn't have any volunteering section on his linkedin -> leave blank
                    ]

                the examples above are just  examples, be sure to replace it with the actual info 

                """
            ),
            agent=agent,
            async_execution=True
        )
    
 
    def linkedin_activity_analysis_task(self, agent, linkedin_activity,commented_cv_path,name):
            return Task(
            description=dedent(
                f"""
               **Task**: comment the {linkedin_activity}, and see how they can value to the {commented_cv_path}

                  
                **Parameters**:
                -CV: {commented_cv_path} 
                -name{name}


                **Note**: {self.__tip_section()}
                """
            ),
            expected_output=(
                f"""
                Your expected task output is a paragraph that comment the activity section of the LinkedIn profile. And see how they can value to the {commented_cv_path}

                Example:

                    [
                     {name}'s linkedin activity show that he he is sharing article that are related with his area of expertise mentioned in {commented_cv_path}
                    ]

                    or

                    [
                    {name} activity is empty on his linkedin -> leave blank
                    ]

                the examples above are just  examples, be sure to replace it with the actual info 

                """
            ),
            agent=agent,
            async_execution=True
        )
    
    def linkedin_comments_analysis_task(self, agent, linkedin_comments,commented_cv_path,name):          
           return Task(
           description=dedent(
                f"""
               **Task**: comment the {linkedin_comments}, and see how they can value to the {commented_cv_path}

              
                    
                **Parameters**:
                -CV: {commented_cv_path} 
                -name{name}


                **Note**: {self.__tip_section()}
                """
            ),
            expected_output=(
                f"""
                Your expected task output is a paragraph that comment the comment section of the LinkedIn profile. And see how they can value to the {commented_cv_path}

                Example:

                    [
                     {name}'s linkedin  show that he commented on xyz post, his comment where consise, clear, enthousiast, showing his caracter
                    ]

                    or

                    [
                    {name} didn't post any comment -> leave blank
                    ]

                the examples above are just  examples, be sure to replace it with the actual info 

                """
            ),
            agent=agent,
            async_execution=True
        )
    
    def linkedin_summary_task(self, agent,name,cv_commented_path):   
        return Task(
            description=dedent(
                f"""
                **Task**: summarize the comments made in the previous task of the different parts of the LinkedIn profile of {name} into one paragraph

                **Description**: Your goal is to summarize the analysis of the different parts of the LinkedIn profile that were made in the previous tasks.

                **Parameters**: 
                - Name:{name}
                - Cv: {cv_commented_path}

                **Note**: {self.__tip_section()}
                """
            ),
            expected_output=(
                f"""
                Your expected task output is a paragraph that summarizes the comments made in the previous tasks of the different parts of the LinkedIn profile. and see how it can enrich {cv_commented_path}

                Example:

                    [
                    {name}'s linkedin confirms overall information provided in the cv, at the same time thanks we can add that he took extra course in xyz, and had internship that wasn't mentioned in the cv
                    which is valuable extra info as it confirms his expertise in this area
                    ]

                the examples above are just  examples, be sure to replace it with the actual info 

                """
            ),
            agent=agent,           
            async_execution=False
        )
    

    def enrichment_verification_task(self,agent,cv_commented_path,name):
        return Task(
        description=dedent(
             f"""
            **Task**: verify that the information of the previous task is correct and that he hasn't made errors or invented part of his summary, 
            then provide a corrected, improved summary 

            **Description**: Your goal is to correct and improve the output of the previous one to provide a better one 


            **Parameters**:
            -Name:{name}
            -Cv: {cv_commented_path}

            **Note**: {self.__tip_section()}, 
             """
        ),
        expected_output=(
             f"""
            Your expected task output is a paragraph that is an improved version of the previous task, the info is the correct one, and the phrasing is better

            [
            {name}'s linkedin confirms overall information provided in the cv, at the same time thanks we can add that he took extra course in xyz, and had internship that wasn't mentioned in the cv
            which is valuable extra info as it confirms his expertise in this area

            ]


            the examples above are just  examples, be sure to replace it with the actual info 
            """
        ),
        agent=agent,
        async_execution=False

        )

    
    def cv_enrichment_task(self, agent):
        return Task(
        description=dedent(
            f"""
            **Task**: take the output from the enrichment verification task and output it as txt file

            **Note**: {self.__tip_section()}
            """
        ),
        expected_output="A text file named cv_enrichment.txt containing the enriched data.",
        output_file="cv_enrichment.txt",
        agent=agent,
        async_execution=False,
        
    )

    


