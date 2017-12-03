from flask_wizard import response
from urllib.parse import quote

import json
import math
import operator
import os

def ngrams(sentence, n):
  return zip(*[sentence.split()[i:] for i in range(n)])


def maybe_find_course(session):
    redis = session['cache']
    #load the stop words
    stopWords = ['d','find' ,'down', 'they', 'during', 'no', 'yourselves', 'most', 'needn', 'which', 'yours', 'you', 've', 'once', 'own', 'does', 'weren', 'myself', 'will', 'mustn', 'm', 'couldn', 'from', 'their', 'ain', 'off', 'isn', 'wasn', 'doesn', 'll', 'about', 'where', 'only', 'an', 'nor', 'shouldn', 'by', 'themselves', 'should', 'him', 'ours', 'to', 'hasn', 'for', 'why', 'until', 'y', 'when', 'her', 'aren', 'didn', 'that', 'there', 'at', 'same', 'herself', 'below', 'it', 'under', 'how', 'more', 'whom', 'not', 'both', 'don', 'against', 'further', 'hers', 'just', 'each', 'being', 'your', 'now', 'then', 'if', 'have', 'is', 'be', 'but', 'shan', 'the', 'before', 'over', 's', 'his', 'mightn', 'as', 'can', 'yourself', 'up', 'between', 'i', 'on', 'few', 'having', 'and', 'himself', 'this', 'again', 'he', 'am', 'theirs', 'who', 'these', 'has', 'or', 'with', 't', 'here', 'such', 'through', 'won', 'above', 'did', 'she', 'had', 'our', 'my', 'all', 'were', 'its', 'hadn', 'other', 'doing', 'are', 'them', 'wouldn', 'while', 'because', 'into', 'itself', 'too', 'haven', 're', 'so', 'out', 'been', 'very', 'any', 'those', 'o', 'in', 'do', 'after', 'a', 'ourselves', 'we', 'ma', 'me', 'of', 'some', 'what', 'was', 'than']

    
    message = session['message'].lower()
    message_words = message.split(' ')
    search_words = []

    for word in message_words:
        if word in stopWords or word in ["course","courses"]:
            continue
        else:
            search_words.append(word)



    search_query = ' '.join(search_words)
    print(search_query)
    question = "Do you want me to find courses related to '" + search_query + "'?"
    quick_reply_obj = response.quick_reply(
                                            text=question,
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
        "question":"courses",
        "topic":search_query
    }
    redis.hmset(key, event)
    redis.expire(key, 259200)

def find_course(session):
    redis = session['cache']
    response.send(session,"Finding the courses")
    message = session['message'].lower()
    response.sendTyping(session)
    if session['entities'][0]['value']:
        query = session['entities'][0]['value']
    else:
        response.send("What do you want to learn about?")
        return 1
    with open('./data/newest_courses.json','r') as data:
        course_data = json.loads(data.read())
    with open('./data/gram_courses_inverted.json','r') as data:
        inverted_index= json.loads(data.read())

    query = query.lower()
    #load the stop words
    stopWords = ['(',')',',','|','.','?','-','d','introduction','interested','pace','course','learn','best','popular','subjects','courses',':','next','&','guide','online','courses','step','study','thing','need','edx','certificate','however','earn','down', 'they', 'during', 'no', 'yourselves', 'most', 'needn', 'which', 'yours', 'you', 've', 'once', 'own', 'does', 'weren', 'myself', 'will', 'mustn', 'm', 'couldn', 'from', 'their', 'ain', 'off', 'isn', 'wasn', 'doesn', 'll', 'about', 'where', 'only', 'an', 'nor', 'shouldn', 'by', 'themselves', 'should', 'him', 'ours', 'to', 'hasn', 'for', 'why', 'until', 'y', 'when', 'her', 'aren', 'didn', 'that', 'there', 'at', 'same', 'herself', 'below', 'it', 'under', 'how', 'more', 'whom', 'not', 'both', 'don', 'against', 'further', 'hers', 'just', 'each', 'being', 'your', 'now', 'then', 'if', 'have', 'is', 'be', 'but', 'shan', 'the', 'before', 'over', 's', 'his', 'mightn', 'as', 'can', 'yourself', 'up', 'between', 'i', 'on', 'few', 'having', 'and', 'himself', 'this', 'again', 'he', 'am', 'theirs', 'who', 'these', 'has', 'or', 'with', 't', 'here', 'such', 'through', 'won', 'above', 'did', 'she', 'had', 'our', 'my', 'all', 'were', 'its', 'hadn', 'other', 'doing', 'are', 'them', 'wouldn', 'while', 'because', 'into', 'itself', 'too', 'haven', 're', 'so', 'out', 'been', 'very', 'any', 'those', 'o', 'in', 'do', 'after', 'a', 'ourselves', 'we', 'ma', 'me', 'of', 'some', 'what', 'was', 'than']

    possible_courses = {}

    advanced_words = [" advanced "," advance "," advn "," advnc "," tougher "," tough "," hard "," harder "]
    inter_words = [" intermediate "," intermedit "," inter "," medium "," mid "]
    intro_words = [" introductory "," intro "," introduction "," begginer "," starting "," start "]


    level_type = None
    #remove stop words
    query = ' ' + query + ' '
    for word in stopWords:
        query = query.replace(' ' + word + ' ',' ')

    print(level_type)
    for word in advanced_words:
        if word in message or word in query:
            level_type = 'advanced'

    for word in inter_words:
        if word in message or word in query:
            level_type = 'intermediate'
    
    for word in intro_words:
        if word in message or word in query:
            level_type = 'introductory'

    # print(query)

    #get 2 grams
    doubles = list(ngrams(query,2))
    for double in doubles:
        double = ' '.join(double)
        if double in inverted_index["2"]:
            scores = inverted_index["2"][double]
            sorted_scores = sorted(scores.items(),key=operator.itemgetter(1), reverse=True)
            possibles = sorted_scores[:50]
            
            for item in possibles:
                if item[0] in possible_courses:
                    possible_courses[item[0]] += item[1]
                else:
                    possible_courses[item[0]] = item[1]
                    
    #get 1 grams
    singles = query.split(' ')
    for single in singles:
        if single in inverted_index["1"]:
            scores = inverted_index["1"][single]
            sorted_scores = sorted(scores.items(),key=operator.itemgetter(1), reverse=True)
            possibles = sorted_scores[:50]
            
            for item in possibles:
                if item[0] in possible_courses:
                    possible_courses[item[0]] += item[1]
                else:
                    possible_courses[item[0]] = item[1]
                    
                    
    #seperate possible_courses into categories
    categorised_courses = {"introductory":{},"intermediate":{},"advanced":{}}
    for course in possible_courses:
        if not course in course_data:
            continue
        else:
            level = course_data[course]['level'].lower()
            categorised_courses[level][course] = possible_courses[course]

    intro = len(categorised_courses["introductory"].keys())
    inter = len(categorised_courses["intermediate"].keys())
    advanced = len(categorised_courses["advanced"].keys())

    print("Found " + str(intro) + " introductory courses")
    print("Found " + str(inter) + " intermediate courses")
    print("Found " + str(advanced) + " advanced courses")

    # Get top 5 in each category
    top_categorised_courses = {}

    intro_courses = categorised_courses["introductory"]
    sorted_intro_courses = sorted(categorised_courses["introductory"].items(),key=operator.itemgetter(1), reverse=True)
    top_categorised_courses["introductory"] = sorted_intro_courses[:5]

    inter_courses = categorised_courses["intermediate"]
    sorted_inter_courses = sorted(categorised_courses["intermediate"].items(),key=operator.itemgetter(1), reverse=True)
    top_categorised_courses["intermediate"] = sorted_inter_courses[:5]

    advanced_courses = categorised_courses["advanced"]
    sorted_advanced_courses = sorted(categorised_courses["advanced"].items(),key=operator.itemgetter(1), reverse=True)
    top_categorised_courses["advanced"] = sorted_intro_courses[:5]

    print(level_type)
    if level_type == None:
        # print(top_categorised_courses)
        question = "What level of courses are you looking for?"

        replies = []
        if intro > 0:
            replies.append(
                            response.replies(
                                            title="Introductory",
                                            payload="introductory"
                            )
                        )

        if inter > 0:
            replies.append(
                            response.replies(
                                            title="Intermediate",
                                            payload="intermediate"
                            )
                        )

        if intro > 0:
            replies.append(
                            response.replies(
                                            title="Advanced",
                                            payload="advanced"
                            )
                        )
        quick_reply_obj = response.quick_reply(
                                                text=question,
                                                replies = replies
                                            )
        response.send(session,quick_reply_obj)
        key = session['user']['id'] + '_levels'
        event = {
            "question":"levels",
            "introductory":top_categorised_courses["introductory"],
            "intermediate":top_categorised_courses["intermediate"],
            "advanced":top_categorised_courses["advanced"]
        }
        redis.hmset(key, event)
        redis.expire(key, 259200)
    elif level_type == 'advanced':
        courses = top_categorised_courses["advanced"]
        
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
    elif level_type == 'intermediate':
        courses = top_categorised_courses["intermediate"]
        
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
    elif level_type == 'introductory':
        courses = top_categorised_courses["introductory"]
        
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
