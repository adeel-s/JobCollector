jobDataExtractionPrompt = '''
The following text is an html formatted job description for a software developer role. I need specific pieces of information from this text:

Years of experience (categorized as 0-1, 2-4, 4+)
Work arrangement (categorized as On-site, Hybrid, Remote - default is on-site)
Experience level (caterogized as Intern, Entry Level, Junior, Mid-level, Senior)
Pay (extract the range, if non given, write "Pay not stated")

Please output only the result in JSON format without any extra newline characters (for example: result = {yoe:"2-4", arrangement:"Remote", experience:"Junior", pay:"$65,000-$80,000"} without any leading or trailing comments

'''

resumeGenerationPrompt = '''
Given a job description and some text of my work experience, write 4 bullet points for each work experience tailored to the job description. 
Write each bullet point to emphasize the result of the work and value realized to the role, include as many quantitative metrics as possible,
and phrase your response in such a way that could be included on a resume. User hard numbers, not placeholders for all metrics.
Include one additional bullet point mentioning the technologies, programming languages and development environment used for the stack. 
Use '*' as bullet points. Do not add any leading or trailing comments.


Here is an example of the exact format of the response I want:

"Experience 1

* Wrote and tested Python applications to map the surroundings of an autonomous vehicle for pathfinding and
obstacle avoidance, increasing environment visibility by 40%

* Ensured seamless deployment of complex robotics software systems by thoroughly debugging code before
on-vehicle testing, saving the team valuable hours during high-pressure synchronous collaboration

* Increased team efficiency and communication by maintaining industry-standard coding practices and
performing regular code reviews in an Agile framework

* Stack: Proprietary Autoware Universe build running on UNIX NVIDIA Drive Orin SOC"


Here is the work experience:

Here is the job description:
'''

coverLetterGenerationPrompt = '''
I've included my work experience and a job description below. 
Please write a cover letter for this job, addressing requirements and skills in the description using my work experience.
Write only the letter, without any header, personal information, contact information, or a name at the end.
As much as possible, write sentences in the format Action Verb + Quantifiable Result + Linking Phrase + Action Take, highlighting quantifiable results and value realized.
The format of the letter should be:
* A short introductory paragraph
* Another paragraph highlighting an accomplishment that aligns with the company's needs
* A list of 3 bullet points highlighting my own skills that are relevant to the position
* A paragraph about the company and why our missions align
* A concluding paragraph restating my interest and requesting the company reach out at their earliest convenience.
The letter should be around 265 words
Do not include any leading or trailing whitespace in the cover letter
Do not include any leading or trailing comments.

Here is an example of the format I need:

"Dear Hiring Manager,
I am excited to apply for the IT Engineer position at Lenovo in Chicago. With a solid foundation in software development, a background in Android mobile development, and a proven ability to communicate effectively with clients, I am eager to contribute to Lenovo's mission of delivering innovative and high-quality solutions for its clients.
In my previous role as Software Engineer Intern, I successfully led the development of a LiDAR data fusion pipeline that increased vehicle environment visibility by over 40%. This experience not only strengthened my proficiency in Python but also refined my ability to translate complex technical concepts into clear, actionable insights for clients and stakeholders.
Key highlights of my qualifications include:
* Android Mobile Development Expertise: Designed and developed feature-rich Android applications, ensuring scalability and performance optimization.
* Client Communication: Collaborated directly with clients to gather requirements, provide progress updates, and deliver tailored software solutions that exceeded expectations.
* Team Collaboration and Leadership: Worked alongside cross-functional teams to align project goals with business needs, contributing to code reviews and fostering best practices in software design.
Lenovo's reputation for innovation and its focus on building a smarter, more inclusive future strongly align with my own values. I am particularly excited about the opportunity to design and maintain software applications for corporate legal solutions, where my technical expertise and communication skills can ensure solutions that meet both technical and business objectives.
I am confident that my combination of technical skills, client-focused mindset, and experience in Android development positions me to make a meaningful impact as part of your team. I would welcome the opportunity to discuss how my background aligns with Lenovo's vision and the IT Engineer role.
Thank you for considering my application. I look forward to the possibility of contributing to your team's success."
'''