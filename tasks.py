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
            
                "name": "Jane Doe",
                "cv_experience": "Jane has over 10 years of experience in software development, having worked at various tech companies. At TechCorp, she led a team of developers to create innovative software solutions, contributing to a 20% increase in productivity. Previously, she worked at Web Solutions Inc. where she played a key role in developing a major e-commerce platform.",
                "cv_skills": "Jane is skilled in Python, Java, and JavaScript. She has strong problem-solving abilities and is experienced with Agile methodologies. Jane is also proficient in database management with SQL and has a good understanding of cloud services like AWS and Azure.",
                "cv_education": "Jane holds a Bachelor of Science degree in Computer Science from MIT, where she graduated with honors. She also completed a Master's degree in Software Engineering from Stanford University.",
                "cv_languages": "Jane is fluent in English and Spanish, and has a basic understanding of French."
            
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
                    
                        "name": "Jane Doe",
                        "cv_experience": "Jane has over 10 years of experience in software development, having worked at various tech companies. At TechCorp, she led a team of developers to create innovative software solutions, contributing to a 20% increase in productivity. Previously, she worked at Web Solutions Inc. where she played a key role in developing a major e-commerce platform.",
                        "commented_cv_experience": "Jane's extensive experience in software development is highlighted by her leadership role at TechCorp and her contributions to productivity gains. Her experience in developing a major e-commerce platform demonstrates her technical expertise.",
                        "cv_skills": "Jane is skilled in Python, Java, and JavaScript. She has strong problem-solving abilities and is experienced with Agile methodologies. Jane is also proficient in database management with SQL and has a good understanding of cloud services like AWS and Azure.",
                        "commented_cv_skills": "Jane's skills in Python, Java, and JavaScript are complemented by her problem-solving abilities and experience with Agile methodologies. Her proficiency in database management and cloud services is an added advantage.",
                        "cv_education": "Jane holds a Bachelor of Science degree in Computer Science from MIT, where she graduated with honors. She also completed a Master's degree in Software Engineering from Stanford University.",
                        "commented_cv_education": "Jane's educational background from prestigious institutions like MIT and Stanford University adds significant value to her profile.",
                        "cv_languages": "Jane is fluent in English and Spanish, and has a basic understanding of French.",
                        "commented_cv_languages": "Jane's fluency in English and Spanish, along with her basic understanding of French, enhances her ability to work in diverse environments."
                    
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
                        
                            "name": "Alex Johnson",
                            "cv_experience": "Alex has worked as a Software Engineer at TechCorp since January 2020, where he developed innovative solutions and led a team of engineers to improve system efficiency by 30%. Previously, he worked as a Junior Developer at WebSolutions, enhancing website performance.",
                            "commented_cv_experience": "Alex's experience as a Software Engineer showcases his leadership and technical skills, particularly in improving system efficiency and implementing automated testing.",
                            "cv_skills": "Alex is skilled in Python, Java, C++, automated testing, system design, and Agile methodologies.",
                            "commented_cv_skills": "Alex's technical skills in multiple programming languages and his expertise in system design and Agile methodologies make him a valuable asset.",
                            "cv_education": "Details not provided in the JSON.",
                            "commented_cv_education": "Education details are missing; further information would be beneficial.",
                            "cv_languages": "Alex is fluent in English and has professional working proficiency in Spanish.",
                            "commented_cv_languages": "Alex's bilingual proficiency in English and Spanish enhances his ability to work in diverse environments.",
                            "linkedin_experience": "Software Development at TechCorp (Jan 2020 - Present): Developed innovative solutions using Python, Java, and C++. Led a team to improve system efficiency by 30%. Implemented automated testing, reducing bugs by 40%.\nJunior Developer at WebSolutions (Jun 2017 - Dec 2019): Worked on front-end and back-end development for e-commerce platforms, enhancing website performance and increasing user satisfaction by 20%.",
                            "linkedin_education": "Details not provided in the JSON.",
                            "linkedin_skills": "Python, Java, C++, Automated Testing, System Design, Agile Methodologies",
                            "linkedin_languages": "English (Native or bilingual proficiency), Spanish (Professional working proficiency)",
                            "linkedin_recommendations": "Alex is a highly skilled engineer with a knack for solving complex problems. - John Doe, Manager at TechCorp",
                            "linkedin_certifications": "Certified Java Developer, Oracle, Jan 2019",
                            "linkedin_volunteering": "Code for Good, Volunteer (2019 to Present): Organized coding workshops for underprivileged students.",
                            "linkedin_course": "Advanced Python Programming, Coursera, Completed in 2020",
                            "linkedin_activity": "GitHub: https://github.com/alexjohnson, Tech Blog: https://alextechblog.com",
                            "linkedin_comments": "Alex's contributions to our open-source projects have been invaluable. - Tech Community Member"
                        
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
                        
                            "name": "Alex Johnson",
                            "cv_experience": "Alex has worked as a Software Engineer at TechCorp since January 2020, where he developed innovative solutions and led a team of engineers to improve system efficiency by 30%. Previously, he worked as a Junior Developer at WebSolutions, enhancing website performance.",
                            "commented_cv_experience": "Alex's experience as a Software Engineer showcases his leadership and technical skills, particularly in improving system efficiency and implementing automated testing.",
                            "cv_skills": "Alex is skilled in Python, Java, C++, automated testing, system design, and Agile methodologies.",
                            "commented_cv_skills": "Alex's technical skills in multiple programming languages and his expertise in system design and Agile methodologies make him a valuable asset.",
                            "cv_education": "B.Sc. in Computer Science from Stanford University, M.Sc. in Software Engineering from MIT.",
                            "commented_cv_education": "Alex's educational background from top-tier institutions like Stanford and MIT highlights his strong academic foundation and technical prowess.",
                            "cv_languages": "Alex is fluent in English and has professional working proficiency in Spanish.",
                            "commented_cv_languages": "Alex's bilingual proficiency in English and Spanish enhances his ability to work in diverse environments.",
                            "linkedin_experience": "Software Development at TechCorp (Jan 2020 - Present): Developed innovative solutions using Python, Java, and C++. Led a team to improve system efficiency by 30%. Implemented automated testing, reducing bugs by 40%.\nJunior Developer at WebSolutions (Jun 2017 - Dec 2019): Worked on front-end and back-end development for e-commerce platforms, enhancing website performance and increasing user satisfaction by 20%.",
                            "commented_linkedin_experience": "Alex's LinkedIn experience is robust, showing consistent career growth and significant contributions to his teams and projects. His ability to lead a team and implement solutions that enhance efficiency highlights his value.",
                            "linkedin_education": "B.Sc. in Computer Science from Stanford University, M.Sc. in Software Engineering from MIT.",
                            "commented_linkedin_education": "Alex's educational achievements from prestigious institutions like Stanford and MIT underscore his academic excellence and technical expertise.",
                            "linkedin_skills": "Python, Java, C++, Automated Testing, System Design, Agile Methodologies",
                            "commented_linkedin_skills": "Alex's LinkedIn profile confirms his strong technical skills, particularly in Python and Java, which are highly valuable in software development. His expertise in system design and Agile methodologies is also noteworthy.",
                            "linkedin_languages": "English (Native or bilingual proficiency), Spanish (Professional working proficiency)",
                            "commented_linkedin_languages": "Alex's proficiency in both English and Spanish is a strong asset, enabling him to communicate effectively in bilingual environments.",
                            "linkedin_recommendations": "Alex is a highly skilled engineer with a knack for solving complex problems. - John Doe, Manager at TechCorp",
                            "commented_linkedin_recommendations": "The recommendation from John Doe highlights Alex's problem-solving abilities and technical expertise, reinforcing his suitability for advanced engineering roles.",
                            "linkedin_certifications": "Certified Java Developer, Oracle, Jan 2019",
                            "commented_linkedin_certifications": "Alex's certification as a Java Developer from Oracle validates his technical skills and commitment to professional development.",
                            "linkedin_volunteering": "Code for Good, Volunteer (2019 to Present): Organized coding workshops for underprivileged students.",
                            "commented_linkedin_volunteering": "Alex's volunteer work with Code for Good demonstrates his dedication to community service and his passion for teaching coding to underprivileged students.",
                            "linkedin_course": "Advanced Python Programming, Coursera, Completed in 2020",
                            "commented_linkedin_course": "Completing an Advanced Python Programming course on Coursera shows Alex's commitment to continuous learning and skill enhancement.",
                            "linkedin_activity": "GitHub: https://github.com/alexjohnson, Tech Blog: https://alextechblog.com",
                            "commented_linkedin_activity": "Alex's activity on GitHub and his tech blog indicates his active engagement in the tech community and his willingness to share knowledge.",
                            "linkedin_comments": "Alex's contributions to our open-source projects have been invaluable. - Tech Community Member",
                            "commented_linkedin_comments": "The comment from a tech community member highlights Alex's valuable contributions to open-source projects, showcasing his collaborative spirit and technical acumen."
                        
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
                    
                        "experience_compared": "Both the CV and LinkedIn profiles highlight Alex's significant contributions and leadership in software development. While the CV focuses on his technical skills and improvements in system efficiency, LinkedIn emphasizes his consistent career growth and team leadership.",
                        "education_compared": "Both profiles highlight Alex's educational background from Stanford and MIT. The LinkedIn profile underscores his academic excellence, while the CV emphasizes his strong academic foundation.",
                        "skills_compared": "Both profiles confirm Alex's strong technical skills in Python, Java, and system design. The CV provides a broader range of skills, including automated testing, while LinkedIn highlights his expertise in Agile methodologies.",
                        "languages_compared": "Both profiles mention Alex's proficiency in English and Spanish, enhancing his ability to work in diverse environments. There are no discrepancies between the two profiles in terms of language proficiency."
                    
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
                    
                "extra": "Alex has received a recommendation from his manager at TechCorp, highlighting his problem-solving skills. He is a Certified Java Developer (Oracle, Jan 2019) and has volunteered with Code for Good since 2019, organizing coding workshops for underprivileged students. Additionally, he completed an Advanced Python Programming course on Coursera in 2020.",
                "behaviour": "Alex is highly active on GitHub and maintains a tech blog, indicating his engagement in the tech community. His contributions to open-source projects and insightful comments demonstrate his collaborative and knowledgeable online presence. On LinkedIn, he shares professional articles and participates in discussions related to software development and technology."
                    
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
            "cv_enrichement": "Alex Johnson's LinkedIn profile strongly confirms the information presented in his CV. His extensive experience in software development, 
            particularly his leadership role at TechCorp, is consistently highlighted across both platforms. His academic credentials from Stanford and MIT are validated, 
            emphasizing his strong technical foundation. Alex's proficiency in multiple programming languages and methodologies is evident in both profiles. 
            Furthermore, his active online presence, demonstrated through his GitHub contributions and tech blog, showcases his engagement and influence in the tech community.
             His volunteer work and additional certifications further enhance his profile, indicating a commitment to continuous learning and community involvement."


                """
            ),
            agent=agent,
            context=context,
            async_exectution=True
        )