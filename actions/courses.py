from flask_wizard import response
from urllib.parse import quote

import json
import math
import operator


def find_course(session):
    response.send(session,"Finding the courses")
    response.sendTyping(session)
    if session['entities'][0]['value']:
        query = session['entities'][0]['value']
    else:
        response.send("What do you want to learn about?")
        return 1
    with open('./data/mod_courses.json','r') as data:
        courses = json.loads(data.read())
        
    with open('./data/inv_index.json','r') as data:
        inv_index= json.loads(data.read())

    final_res_set = []
    res_set = {}
    words = query.split(" ")

    for word in words:
            if not word in inv_index:
                continue
            else:
                responses = inv_index[word][:10]

                for resp in responses:
                    file,score = resp

                    if file in res_set:
                        res_set[file] += score
                    else:
                        res_set[file] = score


    sorted_results = sorted(res_set.items(), key=operator.itemgetter(1), reverse=True)
    final_courses = sorted_results[:5]
    res_courses = []
    for course_key in final_courses:
        course_name = course_key[0]
        search_url = courses[course_name]['marketing_url'].split("?")[0] + '?search_query=' + quote(courses[course_name]['title'])
        if courses[course_name]['image']['src'] and courses[course_name]['image']['src']!='None':
            img_url = courses[course_name]['image']['src']
        else:
            img_url = "https://www.edx.org/sites/default/files/mediakit/image/thumb/edx_logo_200x200.png"
        course_obj = response.template_element(
                                                    title=courses[course_name]['title'],
                                                    image_url=img_url,
                                                    subtitle=courses[course_name]['short_description'],
                                                    action=response.actions(type="web_url",url=search_url),
                                                    buttons=[response.button(type="web_url",url=search_url,title="Open Course")]
                                                )
        res_courses.append(course_obj)

    template = response.template(type="generic",elements=res_courses)
    response.send(session,template)
