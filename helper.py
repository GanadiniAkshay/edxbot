import json

with open('./data/mod_courses.json','r') as data:
    courses = json.loads(data.read())

# with open('./data/titles.txt','w') as outFile:
#     for course in courses:
#         outFile.write(course + '\n')
#         print(course)
#     outFile.close()


with open('./data/missing_url.txt','w') as outFile:
    for course in courses:
        marketing_url = courses[course]['marketing_url']
        if marketing_url == "https://www.edx.org/course/?utm_source=ozzai&utm_medium=affiliate_partner":
            outFile.write(course + '\n')
            print(course)
    outFile.close()

