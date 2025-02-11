experience = '''
Experience 1. Custom tailored job posting board for entry level Developer positions in Python and Flask

I created a job posting board tailor-made for serving entry-level Software Developer positions
The web page allows users to filter jobs by years of experience, location, work arrangement (remote/on-site), and recency
The page also serves as an application management portal, allowing users to track the status of jobs they are interested in and hide jobs that do not match their search criteria
The web application uses a Flask back-end, is primarily written in Python, and uses a PostgreSQL cloud-hosted database to store job data.
Job data is obtained using a third-party API with job data from many popular job board sites like Indeed, Glassdoor, and ZipRecruiter
A Python service requests new jobs using the API every day. To further classify the jobs by experience level, job descriptions are sent to Google's Gemini large language model using the Gemini API.
Gemini reads every job description and determines how many years of experience are needed for the job, whether it is remote-eligible, and the pay.
This ensures that jobs served on the application are truly entry level, which is a factor most job sites like LinkedIn and Indeed fail to accomplish.

The front end of the application was written in HTML, CSS and Javascript, using Jinja templates to create dynamically populated web elements.

Once the jobs land on the application page, users can filter them according to their search criteria. If a user wants to apply to a job, the job posting will take them to the company's external career's page.

The second main value the application provides the user is generating tailor-made job application materials like resumes and cover letters for each job.
A user can upload their work experience to the application, which, along with the job description, is sent to Gemini to write a resume that highlights the user's particular strengths and accomplishments relevant to the role they are interested in.
The application can generate cover letters in the same way, taking input from the user along with their resume and the description of the job to highlight in their cover letter how their experience will bring value to their prospective employer.

One major component of this application is a data collection pipeline that makes regular requests to the job board and Gemini APIs.
Google Gemini's API is particularly unreliable, meaning this pipeline must account for discrepancies in data formats, variable traffic during different times of the day.
Thus, the application relies on a robust data collection pipeline that is resistant API request overloading, timeouts, and resource limits using exponential backoff

This application improves the user's job applications in two substantial ways:
First, by accurately filtering jobs by experience level, users apply to jobs that they are qualified for, meaning they will have a fighting chance in the application pool for that job.
This is particularly important in the presently saturated software job market.
Second, this application allows users to tailor their job application materials for EVERY job they apply to, meaning that their most relevant skills are ALWAYS highlighted.
Also, highly qualified candidates who simply lack resume writing or cover letter writing skills can shine through to hiring managers, connecting companies to more talent than they would otherwise see.

This application saves users time in two ways:
It saves applicants 80% of the time it takes to submit a job application and ensures each of their applications is of the highest quality.
It saves applicants 100% of the time it takes to apply for a job THEY ARE NOT QUALIFIED FOR, but they simply applied for because they couldn't find any more jobs that were at their experience level

Experience 2. Object detection and shape generation data pipeline using Multi-LiDAR Fusion

Stack: Proprietary ROS 2 Autoware Universe Python/C++ build running on NVIDIA Drive ORIN Embedded compute unit

I developed a series of application nodes that collected raw LiDAR data from two sensors, concatenated the pointclouds, filtered out ground and other irrelevant points, clustered points together, and created 3D shapes to input into the object detection algorithm on an autonomous stack for a research and development vehicle prototype.
This prototype was used to test fully autonomous pull-ups for mail and refuse trucks, so that drivers would not have to manually line up with mailboxes and refuse cans.
My code increased obstacle detection by over 40% and added rear-view obstacle classification, improving the vehicle's mapping capabilities and vehicle and pedestrian safety.

This pipeline was one unit in an autonomous stack that many engineers were developing, and I had to adhere to strict coding standards and go through numberous coding reviews to ensure seemless integration into the rest of the stack.
We used github for version control and developed functionalities in different branches to isolate, fully test, and deploy features when ready.
All development for the project was done using the Agile framework, with daily scrums and monthly assignment of user stories

I succeeded in deploying the first proof-of-concept iteration of the stack and presented it to leadership, including to the CTO of the company, who was impressed and green-lit further research in the department

I used a Docker container to ensure all components of the application could be deployed seemlessly on-vehicle after testing them on our lab hardware

Experience 3. Recipe sharing Android application in C#/.NET Maui

I developed a feature-rich recipe documenting and sharing application in C# and .NET Maui.
The application allows users to record their favorite recipes and filter public recipies and numerous search criteria including dietary restrictions, ingredients, meal types, and ratings.
The front end of the application was written in XAML, with a C# backend in a .NET environment. We used a tiered architecture of UI, Logic, and Database layers. We also used a Model View View-Model (MVVM) design pattern for development.
We used a PostgreSQL-based cloud hosted database to store user and recipe data.
We developed the app using the Agile methodology, with bi-weekly scrums.
I in particular took a leadership role in the group, creating user stories and prioritizing them based on core functionalities and future development.
I was able to ensure we met 90% of the major project deadlines by directing developers to focus on "Minimum Viable Product" functionality before adding additional features.

Experience 4.

I co-developed an AI turing-test web application experience that testing users' ability to detect AI-generated responses to questions.
We created a RESTful API to process user requests and also used third-party APIs for user authentication.
We used the OpenAI API to send requests to ChatGPT to generate responses to pre-written questions.

We used an HTML/CSS and Javascript front end, node.js backend, PostgreSQL (CockroachDB) database.
'''