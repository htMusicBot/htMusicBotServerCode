import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hateCrime.settings")
import django
django.setup()
from main.models import Singer , MusicDirector , Lyricist , MovieName , Actor , Category , Year ,Song ,UserData

PAGE_ACCESS_TOKEN = 'EAACCN4djHpkBAN7pazyZCHYSv14UPPYdUPCjmmbIFonmOR5we3mDrMTqYLJaByMjnD4LVjU0ZCZBCHgzsoeIGBgeldj3xULWYvoVAXHtufHoQaq4v0hN3GOxl4kvwmDgbkl7yqZCyCj74ZCbEiYMrpTpJM0AiAm0jJhZCnRTuqLwZDZD'




def setMenu():
    post_message_url = 'https://graph.facebook.com/v2.6/me/thread_settings?access_token=%s'%PAGE_ACCESS_TOKEN

    response_object = {
                        "persistent_menu":[
                        {
                          "locale":"default",
                          # "composer_input_disabled":False,
                          "call_to_actions":[
                            {
                              "title":"EZYCV",
                              "type":"nested",
                              "call_to_actions":[
                                                {
                                                  "type":"postback",
                                                  "title":"Reset everything",
                                                  "payload":"RESET"
                                                },
                                                
                                                
                                                {
                                                  "type":"postback",
                                                  "title":"Personal Details ",
                                                  "payload":"DETAILS"
                                                },
                                                {
                                                  "type":"postback",
                                                  "title":"Work",
                                                  "payload":"WORK"
                                                },
                                                {
                                                  "type":"postback",
                                                  "title": "See Templates",
                                                  "payload":"TEMPLATES"
                                                },
                                                {
                                                  "type":"postback",
                                                  "title":"Feedback",
                                                  "payload":"FEEDBACK"
                                                },
                              ]
                            },
                            {
                              "type":"web_url",
                              "title":"Our Website",
                              "url":"http://ezycv.github.io",
                              "webview_height_ratio":"full"
                            }
                          ]
                        },
                        
                      ]
                    }                    

    

    menu_object = json.dumps(response_object)
    status = requests.post(post_message_url,
          headers = {"Content-Type": "application/json"},
          data = menu_object)


def greetingText():
    post_message_url = 'https://graph.facebook.com/v2.6/me/thread_settings?access_token=%s'%PAGE_ACCESS_TOKEN
   
    response_object =   {
         "setting_type":"greeting",
             "greeting":{
             "text":"Hi {{user_first_name}} Welcome to music bot "
                }
            }

    menu_object = json.dumps(response_object)
    status = requests.post(post_message_url,
          headers = {"Content-Type": "application/json"},
          data = menu_object)


def greetingButton():
    post_message_url = 'https://graph.facebook.com/v2.6/me/thread_settings?access_token=%s'%PAGE_ACCESS_TOKEN
    
    response_object =   {
        "setting_type":"call_to_actions",
        "thread_state":"new_thread",
        "call_to_actions":[
        {
            "payload":"STARTING123"
            }
        ]
        }

    menu_object = json.dumps(response_object)
    status = requests.post(post_message_url,
          headers = {"Content-Type": "application/json"},
          data = menu_object)