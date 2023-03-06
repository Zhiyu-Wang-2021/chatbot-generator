template = {
    "intents": [
        {
            "intent": "appointment",
            "examples": [
                {
                    "text": "appointment"
                },
                {
                    "text": "book appointment"
                },
                {
                    "text": "Can I book an appointment?"
                },
                {
                    "text": "do you know how to make an appointment"
                },
                {
                    "text": "How do I book an appointment"
                },
                {
                    "text": "How to cancel an appointment?"
                },
                {
                    "text": "how to get an appointment"
                },
                {
                    "text": "how to see a doctor"
                },
                {
                    "text": "I want to book an appointment"
                },
                {
                    "text": "I want to cancel my appointment"
                },
                {
                    "text": "I want to schedule an appointment"
                },
                {
                    "text": "I want to see a doctor"
                },
                {
                    "text": "make an appointment"
                },
                {
                    "text": "tell me how to make an appointment"
                }
            ],
            "description": ""
        },
        {
            "intent": "ask_more_info",
            "examples": [
                {
                    "text": "are there any more things to share"
                },
                {
                    "text": "can you describe more"
                },
                {
                    "text": "can you direct me to some links on your website?"
                },
                {
                    "text": "I need more information"
                },
                {
                    "text": "please give me more info"
                }
            ],
            "description": ""
        },
        {
            "intent": "greetings",
            "examples": [
                {
                    "text": "can you assist me?"
                },
                {
                    "text": "greetings"
                },
                {
                    "text": "hello"
                },
                {
                    "text": "hi"
                },
                {
                    "text": "Hi! I'm Bob."
                },
                {
                    "text": "how's it going"
                },
                {
                    "text": "How you can help me"
                },
                {
                    "text": "nice to meet you"
                },
                {
                    "text": "what service do you provide"
                },
                {
                    "text": "what's up"
                }
            ],
            "description": ""
        },
        {
            "intent": "hours_info",
            "examples": [
                {
                    "text": "Are you open on Christmas' Day?"
                },
                {
                    "text": "Are you open on Saturdays?"
                },
                {
                    "text": "Are you open on Sundays?"
                },
                {
                    "text": "hours of operation"
                },
                {
                    "text": "opening hour"
                },
                {
                    "text": "What are your hours?"
                },
                {
                    "text": "What are your hours of operation?"
                },
                {
                    "text": "What days are you closed on?"
                },
                {
                    "text": "what is the opening hour of this practice"
                },
                {
                    "text": "What time are you open until?"
                },
                {
                    "text": "When are you open"
                },
                {
                    "text": "When does this trust open"
                },
                {
                    "text": "When do you close"
                },
                {
                    "text": "When do you open"
                },
                {
                    "text": "When will this hospital open"
                }
            ],
            "description": "-"
        },
        {
            "intent": "location_info",
            "examples": [
                {
                    "text": "address"
                },
                {
                    "text": "can you tell me where are you loacted"
                },
                {
                    "text": "can you tell me your address"
                },
                {
                    "text": "Give me a list of locations"
                },
                {
                    "text": "I wonder what is the location of this GP"
                },
                {
                    "text": "List of location"
                },
                {
                    "text": "list of your locations"
                },
                {
                    "text": "location"
                },
                {
                    "text": "tell me where is this place"
                },
                {
                    "text": "the location of this hospital"
                },
                {
                    "text": "What are your locations?"
                },
                {
                    "text": "what is the location of this trust"
                },
                {
                    "text": "what is your address"
                },
                {
                    "text": "Where are you physically located?"
                },
                {
                    "text": "Where are your trusts?"
                },
                {
                    "text": "Where is the hospital"
                },
                {
                    "text": "Where is this GP located?"
                },
                {
                    "text": "Where is this hospital?"
                },
                {
                    "text": "Where is this hospital located?"
                },
                {
                    "text": "where is this place"
                },
                {
                    "text": "Where is this trust located?"
                },
                {
                    "text": "Where is your trust"
                }
            ],
            "description": "-"
        },
        {
            "intent": "phone_number",
            "examples": [
                {
                    "text": "can you tell me your contact information"
                },
                {
                    "text": "contact info"
                },
                {
                    "text": "how to call you"
                },
                {
                    "text": "how to contact this hospital"
                },
                {
                    "text": "I want to call this trust"
                },
                {
                    "text": "list your numbers"
                },
                {
                    "text": "phone number"
                },
                {
                    "text": "tell me your phone number"
                },
                {
                    "text": "this GP's contact information"
                },
                {
                    "text": "this hospital's number"
                },
                {
                    "text": "what is your number"
                },
                {
                    "text": "what is your telephone number"
                },
                {
                    "text": "what's the number of this trust"
                },
                {
                    "text": "which number should I call"
                }
            ],
            "description": ""
        }
    ],
    "entities": [
        {
            "entity": "specific_location",
            "values": [
                {
                    "type": "synonyms",
                    "value": "center",
                    "synonyms": []
                },
                {
                    "type": "synonyms",
                    "value": "department",
                    "synonyms": []
                },
                {
                    "type": "synonyms",
                    "value": "floor",
                    "synonyms": []
                },
                {
                    "type": "synonyms",
                    "value": "unit",
                    "synonyms": []
                },
                {
                    "type": "synonyms",
                    "value": "wing",
                    "synonyms": []
                }
            ],
            "fuzzy_match": True
        }
    ],
    "metadata": {
        "api_version": {
            "major_version": "v2",
            "minor_version": "2018-11-08"
        }
    },
    "webhooks": [
        {
            "url": "https://bingaccessforwatson.azurewebsites.net/api/useQnA2ImproveAnswer?code=41mEZaj2kjJphYWmK6eHPFzQwQHLiVyW61QpEvrpGUcbAzFuAwDC3w==",
            "name": "main_webhook",
            "headers": [
                {
                    "name": "Ocp-Apim-Subscription-Key",
                    "value": "ef99b91a0209431cb66dd4d32a0b20c6"
                },
                {
                    "name": "Content-Type",
                    "value": "application/json"
                }
            ]
        }
    ],
    "dialog_nodes": [
        {
            "type": "standard",
            "title": "Anything else",
            "actions": [
                {
                    "name": "main_webhook",
                    "type": "webhook",
                    "parameters": {
                        "q": "<? input.text ?>",
                        "site": "https://www.gosh.nhs.uk"
                    },
                    "result_variable": "search_result"
                }
            ],
            "metadata": {
                "_customization": {
                    "mcr": True
                }
            },
            "conditions": "anything_else",
            "dialog_node": "Anything else",
            "previous_sibling": "node_10_1677578129201",
            "disambiguation_opt_out": True
        },
        {
            "type": "standard",
            "title": "Hours Info",
            "output": {
                "generic": [
                    {
                        "values": [
                            {
                                "text": "Our trusts opens on:\n\nMonday\n08:00-18:30\n\nTuesday\n08:00-18:30\n\nWednesday\n08:00-18:30\n\nThursday\n08:00-18:30\n\nFriday\n08:00-18:30"
                            }
                        ],
                        "response_type": "text",
                        "selection_policy": "sequential"
                    }
                ]
            },
            "conditions": "#hours_info && !@specific_location",
            "dialog_node": "Hours Info",
            "previous_sibling": "Location Info"
        },
        {
            "type": "standard",
            "title": "Location Info",
            "output": {
                "generic": [
                    {
                        "values": [
                            {
                                "text": "We are at this address: Great Ormond Street Hospital Great Ormond Street London WC1N 3JH"
                            }
                        ],
                        "response_type": "text",
                        "selection_policy": "sequential"
                    }
                ]
            },
            "metadata": {
                "_customization": {
                    "mcr": False
                }
            },
            "conditions": "#location_info && !@specific_location",
            "dialog_node": "Location Info",
            "previous_sibling": "node_3_1677777872422"
        },
        {
            "type": "standard",
            "output": {
                "generic": [
                    {
                        "values": [
                            {
                                "text": "The following links may be helpful:"
                            },
                            {
                                "text": "<a href=\"<? $search_result.bingResults[0].url ?>\"><? $search_result.bingResults[0].name ?></a>"
                            },
                            {
                                "text": "<a href=\"<? $search_result.bingResults[1].url ?>\"><? $search_result.bingResults[1].name ?></a>"
                            },
                            {
                                "text": "<a href=\"<? $search_result.bingResults[2].url ?>\"><? $search_result.bingResults[2].name ?></a>"
                            }
                        ],
                        "response_type": "text",
                        "selection_policy": "multiline"
                    }
                ]
            },
            "parent": "Anything else",
            "context": {},
            "conditions": "#ask_more_info",
            "dialog_node": "node_10_1677157030611"
        },
        {
            "type": "standard",
            "title": "Appointment Info",
            "output": {
                "generic": [
                    {
                        "values": [
                            {
                                "text": "APPOINTMENT"
                            }
                        ],
                        "response_type": "text",
                        "selection_policy": "sequential"
                    }
                ]
            },
            "conditions": "#appointment && !@specific_location",
            "dialog_node": "node_10_1677578129201",
            "previous_sibling": "node_5_1677172471791"
        },
        {
            "type": "standard",
            "title": "greetings",
            "output": {
                "generic": [
                    {
                        "values": [
                            {
                                "text": "Hello! I can answer you questions based on the information provided on this website. How can I help you?"
                            }
                        ],
                        "response_type": "text",
                        "selection_policy": "sequential"
                    }
                ]
            },
            "conditions": "#greetings",
            "dialog_node": "node_3_1677777872422",
            "previous_sibling": "Welcome"
        },
        {
            "type": "standard",
            "title": "Phone Info",
            "output": {
                "generic": [
                    {
                        "values": [
                            {
                                "text": "Please call us with this number: 020 7405 9200"
                            }
                        ],
                        "response_type": "text",
                        "selection_policy": "sequential"
                    }
                ]
            },
            "conditions": "#phone_number && !@specific_location",
            "dialog_node": "node_5_1677172471791",
            "previous_sibling": "Hours Info"
        },
        {
            "type": "response_condition",
            "output": {
                "generic": [
                    {
                        "values": [
                            {
                                "text": "<? $search_result.answer ?>"
                            }
                        ],
                        "response_type": "text",
                        "selection_policy": "multiline"
                    }
                ]
            },
            "parent": "Anything else",
            "conditions": "$search_result.confidenceScore > 0.43",
            "dialog_node": "response_1_1676646061220",
            "previous_sibling": "node_10_1677157030611"
        },
        {
            "type": "response_condition",
            "output": {
                "generic": [
                    {
                        "values": [
                            {
                                "text": "Sorry, I am not sure about this question based on the information on our website."
                            }
                        ],
                        "response_type": "text",
                        "selection_policy": "sequential"
                    }
                ]
            },
            "parent": "Anything else",
            "conditions": "anything_else",
            "dialog_node": "response_1_1676646061565",
            "previous_sibling": "response_8_1677157989078"
        },
        {
            "type": "response_condition",
            "output": {
                "generic": [
                    {
                        "values": [
                            {
                                "text": "I'm not very sure about this. But this link can be helpful: "
                            },
                            {
                                "text": "<a href=\"<? $search_result.bingResults[0].url ?>\"><? $search_result.bingResults[0].name ?></a>"
                            },
                            {
                                "text": "<? $search_result.bingResults[0].snippet ?>"
                            }
                        ],
                        "response_type": "text",
                        "selection_policy": "multiline"
                    }
                ]
            },
            "parent": "Anything else",
            "conditions": "$search_result.confidenceScore > 0.2",
            "dialog_node": "response_8_1677157989078",
            "previous_sibling": "response_1_1676646061220"
        },
        {
            "type": "response_condition",
            "title": "response_Location Info0",
            "output": {
                "generic": [
                    {
                        "values": [
                            {
                                "text": "We are at this address: Great Ormond Street Hospital Great Ormond Street London WC1N 3JH"
                            }
                        ],
                        "response_type": "text",
                        "selection_policy": "sequential"
                    }
                ]
            },
            "parent": "Location Info",
            "disabled": True,
            "conditions": "True",
            "dialog_node": "response_Location Info0"
        },
        {
            "type": "standard",
            "title": "Welcome",
            "output": {
                "generic": [
                    {
                        "values": [
                            {
                                "text": "Hello! I can answer you questions based on the information provided on this website. How can I help you?"
                            }
                        ],
                        "response_type": "text",
                        "selection_policy": "sequential"
                    }
                ]
            },
            "conditions": "welcome",
            "dialog_node": "Welcome"
        }
    ],
    "counterexamples": [],
    "system_settings": {
        "nlp": {
            "model": "latest"
        },
        "off_topic": {
            "enabled": True
        },
        "disambiguation": {
            "prompt": "Didyoumean:",
            "enabled": False,
            "randomize": True,
            "max_suggestions": 5,
            "suggestion_text_policy": "title",
            "none_of_the_above_prompt": "Noneoftheabove"
        },
        "system_entities": {
            "enabled": True
        },
        "human_agent_assist": {
            "prompt": "Didyoumean:"
        },
        "spelling_auto_correct": True
    },
    "learning_opt_out": False,
    "name": "GeneratedSkill",
    "language": "en",
    "description": ""
}