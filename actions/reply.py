from flask_wizard import response
from urllib.parse import quote

import ast
import json 

from .courses import find_profession

def yes(session):
    response.sendTyping(session)
    redis = session['cache']
    mongo = session['mongo']
    key = session['user']['id']
    if mongo:
        user_data = mongo.db.user_data.find_one({'user_id':key})
    else:
        user_data = None

    if redis.exists(key):
        event = redis.hgetall(key)
        redis.delete(key) 
    else:
        event = None
    
    if event:
        question = str(event[b'question'],'utf-8')
        topic = str(event[b'topic'],'utf-8')
        profession = str(event[b'profession'],'utf-8')

        if question == 'topic':
            if user_data:
                topics = user_data['topics']

                if topic not in topics:
                    topics.append(topic)

                user_data['topics'] = topics
                update = mongo.db.user_data.update_one(
                            {'user_id':key},
                            {
                                "$set":{
                                    "topics":topics
                                }
                            }
                    )
            else:
                user_obj = {"user_id":key,"topics":[topic]}
                load = mongo.db.user_data.insert_one(user_obj)
            session['entities'] = [{"value":profession}]
            find_profession(session)
        else:
            response.send(session,":)")

def no(session):
    response.sendTyping(session)
    redis = session['cache']
    mongo = session['mongo']
    key = session['user']['id']

    with open('./data/mod_courses.json','r') as data:
        courses_data = json.loads(data.read())
    if mongo:
        user_data = mongo.db.user_data.find_one({'user_id':key})
    else:
        user_data = None

    if redis.exists(key):
        event = redis.hgetall(key)
        redis.delete(key) 
    else:
        event = None

    if event:
        question = str(event[b'question'],'utf-8')
        topic = str(event[b'topic'],'utf-8')
        courses = ast.literal_eval(str(event[b'courses'],'utf-8'))
        reply_text = str(event[b'reply_text'],'utf-8')
        if question == 'topic':
           
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
        else:
            response.send(session,":)")

