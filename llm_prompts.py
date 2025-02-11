jobDataExtractionPrompt = '''
The following text is an html formatted job description for a software developer role. I need specific pieces of information from this text:

Years of experience (categorized as 0-1, 2-4, 4+)
Work arrangement (categorized as On-site, Hybrid, Remote - default is on-site)
Experience level (caterogized as Intern, Entry Level, Junior, Mid-level, Senior)
Pay (extract the range, if non given, write "Pay not stated")

Please output only the result in JSON format without any extra newline characters (for example: result = {yoe:"2-4", arrangement:"Remote", experience:"Junior", pay:"$65,000-$80,000"} without any leading or trailing comments

'''