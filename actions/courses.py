from flask_wizard import response
from urllib.parse import quote

import json
import math
import operator
import os


def maybe_find_course(session):
    response.send(session,"Do you want me to find courses?")

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


def find_profession(session):
    response.sendTyping(session)
    redis = session['cache']
    mongo = session['mongo']
    if mongo:
        user_data = mongo.db.user_data.find_one({'user_id':session['user']['id']})
    else:
        user_data = None
    
    if user_data:
        topics_known = user_data['topics']
    else:
        topics_known = []
    if len(session['entities']) > 0:
        profession = session['entities'][0]['value']
        if 'android' in profession.lower():
            profession = 'android'
        elif 'frontend' in profession.lower() or 'front end' in profession.lower() or 'front-end' in profession.lower():
            profession = 'frontend'
        else:
            response.send(session,"Unfortunately I don't have a report ready for that job role."+ "\n\n" +"But your request has been recieved and I will get back with the results :)")
            insert = mongo.db.requests.insert_one({"user_id":session['user']['id'],"request":profession})
            response.send(session,"Here are some professions that I can help with currently")
            choices = [
                response.template_element(
                                            title='Android Developer',
                                            image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Android_robot.svg/872px-Android_robot.svg.png",
                                            buttons=[response.button(type="postback",title="Select",payload="I want to be an android developer")]
                                        ),
                response.template_element(
                                            title='Frontend Developer',
                                            image_url="https://image.ibb.co/ntCt1Q/web_1935737_640.png",
                                            buttons=[response.button(type="postback",title="Select",payload="I want to be a frontend developer")]
                                        )
            ]
            template = response.template(type="generic",elements=choices)
            response.send(session,template)
            return 1
        
        response.sendTyping(session)
        with open('./data/professions.json','r') as data:
            professions = json.loads(data.read())
            prof = professions[profession]
            
            for obj in prof:
                topic = obj['topic']
                is_final = obj['is_final']

                if is_final == "true":
                    with open('./data/mod_courses.json','r') as data:
                        courses_data = json.loads(data.read())

                    courses = obj['courses']
                    reply_text = obj['reply_text']

                    res_courses = []
                    for course in courses:
                        if course in courses_data:
                            search_url = courses_data[course]['marketing_url'].split("?")[0] + '?search_query=' + quote(courses_data[course]['title'])
                            if courses_data[course]['image']['src'] and courses_data[course]['image']['src']!='None':
                                img_url = courses_data[course]['image']['src']
                            else:
                                img_url = "https://www.edx.org/sites/default/files/mediakit/image/thumb/edx_logo_200x200.png"
                            course_obj = response.template_element(
                                                                        title=courses_data[course]['title'],
                                                                        image_url=img_url,
                                                                        subtitle=courses_data[course]['short_description'],
                                                                        action=response.actions(type="web_url",url=search_url),
                                                                        buttons=[response.button(type="web_url",url=search_url,title="Open Course")]
                                                                    )
                            res_courses.append(course_obj)

                    template = response.template(type="generic",elements=res_courses)
                    response.send(session,reply_text)
                    response.send(session,template)
                    break
                
                if topic in topics_known:
                    continue
                
                else:
                    quick_reply_obj = response.quick_reply(
                                                            text=obj['question'],
                                                            replies = [
                                                                response.replies(
                                                                    title="Yes",
                                                                    payload="Yes"
                                                                ),
                                                                response.replies(
                                                                    title="No",
                                                                    payload="No"
                                                                )
                                                            ]
                                                            )
                    response.send(session,quick_reply_obj)

                    key = session['user']['id']
                    event = {
                        "question":"topic",
                        "topic":topic,
                        "profession":profession,
                        "courses":obj['courses'],
                        "reply_text": obj['reply_text']
                    }
                    redis.hmset(key, event)
                    redis.expire(key, 259200)
                    break
    else:
        response.send(session,"Please choose a profession")
        choices = [
            response.template_element(
                                        title='Android Developer',
                                        image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Android_robot.svg/872px-Android_robot.svg.png",
                                        buttons=[response.button(type="postback",title="Select",payload="I want to be an android developer")]
                                    ),
            response.template_element(
                                        title='Frontend Developer',
                                        image_url="https://image.ibb.co/ntCt1Q/web_1935737_640.png",
                                        buttons=[response.button(type="postback",title="Select",payload="I want to be a frontend developer")]
                                    )
        ]
        template = response.template(type="generic",elements=choices)
        response.send(session,template)
