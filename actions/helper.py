from flask_wizard import response

def purpose(session):
    response.send(session,"I can help you find the right course based on your requirement. You can either tell me what you want to learn or type search by profession")
    response.send(session,"Here are some sample phrases")
    response.send(session,"'Find courses for becoming an android developer'\n\n'Find courses for learning ReactJS'\n\n'Find me a course on bootsrap'\n\n")

def certificates(session):
    message = session['message']
    
    if 'certificate' in message.lower() or 'certificates' in message.lower():
        response.send(session,"Here is what people think about it on Quora")
        choices = [
            response.template_element(
                                        title='Quora Answer',
                                        subtitle='Does certificates from websites like Coursera, Udacity or Edx help you get a job?',
                                        image_url="https://lh3.googleusercontent.com/i8knN1N9o-jPD1Eckv8sXMKMPx5-_u7mFJa00JkrP-CXeTr5o9H6NDAVK_E7Iyqi6Pup=w300",
                                        action=response.actions(type="web_url",url="https://www.quora.com/Does-certificates-from-websites-like-Coursera-Udacity-or-Edx-help-you-get-a-job"),
                                        buttons=[response.button(type="web_url",title="Open",url="https://www.quora.com/Does-certificates-from-websites-like-Coursera-Udacity-or-Edx-help-you-get-a-job")]
                                    ),
            response.template_element(
                                        title='Quora Answer',
                                        subtitle='Do employers find MOOCs certificates from Coursera or edX valuable?',
                                        image_url="https://lh3.googleusercontent.com/i8knN1N9o-jPD1Eckv8sXMKMPx5-_u7mFJa00JkrP-CXeTr5o9H6NDAVK_E7Iyqi6Pup=w300",
                                        action=response.actions(type="web_url",url="https://www.quora.com/Do-employers-find-MOOCs-certificates-from-Coursera-or-edX-valuable"),
                                        buttons=[response.button(type="web_url",title="Open",url="https://www.quora.com/Do-employers-find-MOOCs-certificates-from-Coursera-or-edX-valuable")]
                                    ),
            response.template_element(
                                        title='Quora Answer',
                                        subtitle='Should I apply for certification while doing MOOCs?',
                                        image_url="https://lh3.googleusercontent.com/i8knN1N9o-jPD1Eckv8sXMKMPx5-_u7mFJa00JkrP-CXeTr5o9H6NDAVK_E7Iyqi6Pup=w300",
                                        action=response.actions(type="web_url",url="https://www.quora.com/Should-I-apply-for-certification-while-doing-MOOCs"),
                                        buttons=[response.button(type="web_url",title="Open",url="https://www.quora.com/Should-I-apply-for-certification-while-doing-MOOCs")]
                                    )
        ]
        template = response.template(type="generic",elements=choices)
        response.send(session,template)
    else:
        response.send(session,"Can you please rephrase?")
