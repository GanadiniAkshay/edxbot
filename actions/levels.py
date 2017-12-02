from flask_wizard import response
from urllib.parse import quote

import json
import math
import operator
import os
import ast

def intro(session):
    redis = session['cache']
    key = session['user']['id'] + '_levels'

    with open('./data/newest_courses.json','r') as data:
        course_data = json.loads(data.read())

    if redis.exists(key):
        event = redis.hgetall(key)
        redis.delete(key) 
    else:
        event = None

    if event:
        courses = str(event[b'introductory'],'utf-8')
        courses = ast.literal_eval(courses)
        
        res_courses = []
        for course in courses:
            course_name = course[0]
            search_url = course_data[course_name]['marketing_url']
            img_url = course_data[course_name]['img_url']
            course_obj = response.template_element(
                                                title=course_name,
                                                image_url=img_url,
                                                action=response.actions(type="web_url",url=search_url),
                                                buttons=[response.button(type="web_url",url=search_url,title="Open Course")]
                                            )
            res_courses.append(course_obj)
        template = response.template(type="generic",elements=res_courses)
        response.send(session,template)

def inter(session):
    redis = session['cache']
    key = session['user']['id'] + '_levels'

    with open('./data/newest_courses.json','r') as data:
        course_data = json.loads(data.read())

    if redis.exists(key):
        event = redis.hgetall(key)
        redis.delete(key) 
    else:
        event = None
    
    if event:
        courses = str(event[b'intermediate'],'utf-8')
        courses = ast.literal_eval(courses)
        
        res_courses = []
        for course in courses:
            course_name = course[0]
            search_url = course_data[course_name]['marketing_url']
            img_url = course_data[course_name]['img_url']
            course_obj = response.template_element(
                                                title=course_name,
                                                image_url=img_url,
                                                action=response.actions(type="web_url",url=search_url),
                                                buttons=[response.button(type="web_url",url=search_url,title="Open Course")]
                                            )
            res_courses.append(course_obj)
        template = response.template(type="generic",elements=res_courses)
        response.send(session,template)

def advanced(session):
    redis = session['cache']
    key = session['user']['id'] + '_levels'

    with open('./data/newest_courses.json','r') as data:
        course_data = json.loads(data.read())

    if redis.exists(key):
        event = redis.hgetall(key)
        redis.delete(key) 
    else:
        event = None

    if event:
        courses = str(event[b'advanced'],'utf-8')
        courses = ast.literal_eval(courses)
        
        res_courses = []
        for course in courses:
            course_name = course[0]
            search_url = course_data[course_name]['marketing_url']
            img_url = course_data[course_name]['img_url']
            course_obj = response.template_element(
                                                title=course_name,
                                                image_url=img_url,
                                                action=response.actions(type="web_url",url=search_url),
                                                buttons=[response.button(type="web_url",url=search_url,title="Open Course")]
                                            )
            res_courses.append(course_obj)
        template = response.template(type="generic",elements=res_courses)
        response.send(session,template)