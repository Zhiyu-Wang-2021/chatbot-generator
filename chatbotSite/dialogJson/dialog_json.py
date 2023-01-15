import json

import dialogJson.data as data


class DialogJson:

    def __init__(self, answers):
        self.answers = answers

    # "intents":[
    #     {
    #         "intent": "business_address",
    #         "examples":
    #         [
    #             {
    #                 "text": "What is the address of your @business ?"
    #             }, ...
    #         ],
    #         "description": "Addresses for the business"
    #     }, ...
    # ],
    def _intents(self):
        result = [
            self._intent(
                "hours_info",
                data.IntentExamples.hour_info
            ),
            self._intent(
                "location_info",
                data.IntentExamples.location_info
            )
        ]
        return '"intents": ' + json.dumps(result) + ','

    def _intent(self, name, examples, description='-'):
        return {
            "intent": name,
            "examples": list(map(lambda s: {
                "text": s
            }, examples)),
            "description": description
        }

    # "entities": [
    #     {
    #         "entity": "business",
    #         "values": [
    #             {
    #                 "type": "synonyms",
    #                 "value": "business",
    #                 "synonyms":[
    #                     "agency",
    #                     "bureau",
    #                     "firm",
    #                     "office",
    #                     "shop"
    #                 ]
    #             }
    #         ],
    #         "fuzzy_match": true
    #     }
    # ],
    def _entities(self):
        result = [
            self._entity(
                "uk_location",
                data.EntityValues.location,
            )
        ]
        return '"entities": ' + json.dumps(result) + ','

    def _entity(self, name, values, fuzzy_match=True):
        return {
            "entity": name,
            "values": list(map(lambda location_tuple: {
                "type": "synonyms",
                "value": location_tuple[0],
                "synonyms": location_tuple[1]
            }, values)),
            "fuzzy_match": fuzzy_match
        }

    # "dialog_nodes": [{
    #     "type": "standard",
    #     "title": "Business address",
    #     "output": {
    #         "generic": [
    #             {
    #             "values": [
    #                 {
    #                     "text": "Our business is located in ‘Watson Square 5, NY 10040’ and ‘Discovery Avenue, AZ 85010′"
    #                 }
    #             ],
    #             "response_type": "text",
    #                 "selection_policy": "sequential"
    #             }
    #         ]
    #     },
    #     "conditions": "#business_address",
    #     "dialog_node": "Business_Address",
    #     "previous_sibling": "Welcome"
    # }, ...],
    def _dialog_nodes(self):
        loc_info = self.answers.location[0]["address"] + self.answers.location[0]["postcode"]
        hour_info = self.answers.operation_hour[0]["time"]
        result_raw = [
            self._welcome_node(),
            self._dialog_node_multi_condition(
                reference="Location Info",
                condition_dict={
                    "handler": "@uk_location",
                    "enter": "#location_info",
                    "output": [
                        ("true", "Our trust is at: \n" + loc_info),
                        ("$location", "Our $location trust is at: \n" + loc_info)
                    ]
                },
                slot_var="$location",
                previous_sibling="Welcome"
            ),
            self._dialog_node_standard(
                reference="Hours Info",
                output="Our trust opens at " + hour_info,
                condition="#hours_info",
                previous_sibling="Location Info"
            ),
            self._else_node(previous_sibling="Hours Info")
        ]
        result = []
        for r in result_raw:
            if isinstance(r, list):
                result.extend(r)
            else:
                result.append(r)
        return '"dialog_nodes": ' + json.dumps(result) + ','

    # multiple responds node
    # handler -> slot
    # frame
    # response_condition
    # {
    #     "type": "event_handler",
    #     "output": {},
    #     "parent": "slot_handler_parent",
    #     "event_name": "focus",
    #     "dialog_node": "handler_focus",
    #     "previous_sibling": "handler_uk_location"
    # },
    # {
    #     "type": "event_handler",
    #     "output": {},
    #     "parent": "slot_handler_parent",
    #     "context": {
    #         "location": "@uk_location"
    #     },
    #     "conditions": "@uk_location",
    #     "event_name": "input",
    #     "dialog_node": "handler_uk_location"
    # },
    # {
    #     "type": "slot",
    #     "parent": "Location Info",
    #     "variable": "$location",
    #     "dialog_node": "slot_handler_parent",
    #     "previous_sibling": "response_without_location"
    # },
    # {
    #     "type": "frame",
    #     "title": "Location Info",
    #     "metadata": {
    #         "_customization": {
    #             "mcr": true
    #         }
    #     },
    #     "conditions": "#location_info",
    #     "dialog_node": "Location Info",
    #     "previous_sibling": "Welcome"
    # },
    # {
    #     "type": "response_condition",
    #     "output": {
    #         "generic": [
    #             {
    #                 "values": [
    #                     {
    #                         "text": "Our store is at ..."
    #                     }
    #                 ],
    #                 "response_type": "text",
    #                 "selection_policy": "sequential"
    #             }
    #         ]
    #     },
    #     "parent": "Location Info",
    #     "conditions": "true",
    #     "dialog_node": "response_without_location",
    #     "previous_sibling": "response_with_location"
    # },
    # {
    #     "type": "response_condition",
    #     "output": {
    #         "generic": [
    #             {
    #                 "values": [
    #                     {
    #                         "text": "Our $location store is at ..."
    #                     }
    #                 ],
    #                 "response_type": "text",
    #                 "selection_policy": "sequential"
    #             }
    #         ]
    #     },
    #     "parent": "Location Info",
    #     "conditions": "$location",
    #     "dialog_node": "response_with_location"
    # }
    def _dialog_node_multi_condition(self, reference, condition_dict, slot_var, previous_sibling):
        handler_condition = condition_dict['handler']
        enter_condition = condition_dict['enter']
        outputs_and_conditions = condition_dict['output']

        def handler():
            return [
                {
                    "type": "event_handler",
                    "output": {},
                    "parent": "slot_handler_parent_" + reference,
                    "event_name": "focus",
                    "dialog_node": "handler_focus_" + reference,
                    "previous_sibling": "handler_" + reference
                },
                {
                    "type": "event_handler",
                    "output": {},
                    "parent": "slot_handler_parent_" + reference,
                    "context": {
                        "location": handler_condition
                    },
                    "conditions": handler_condition,
                    "event_name": "input",
                    "dialog_node": "handler_" + reference
                }
            ]

        def slot():
            return {
                "type": "slot",
                "parent": reference,
                "variable": slot_var,
                "dialog_node": "slot_handler_parent_" + reference,
                "previous_sibling": "response_" + reference + "0"
            }

        def frame():
            return {
                "type": "frame",
                "title": reference,
                "metadata": {
                    "_customization": {
                        "mcr": True
                    }
                },
                "conditions": enter_condition,
                "dialog_node": reference,
                "previous_sibling": previous_sibling
            }

        def responses():
            responses_list = []
            node_idx = 0
            for condition, output in outputs_and_conditions:
                responses_list.append({
                    "type": "response_condition",
                    "output": {
                        "generic": [
                            {
                                "values": [
                                    {
                                        "text": output
                                    }
                                ],
                                "response_type": "text",
                                "selection_policy": "sequential"
                            }
                        ]
                    },
                    "parent": reference,
                    "conditions": condition,
                    "dialog_node": "response_" + reference + str(node_idx)
                })
                if node_idx < len(outputs_and_conditions) - 1:
                    responses_list[node_idx]["previous_sibling"] = "response_" + reference + str(node_idx + 1)
                node_idx += 1
            return responses_list

        result_raw = [handler(), slot(), frame(), responses()]
        result = []
        for r in result_raw:
            if isinstance(r, list):
                result.extend(r)
            else:
                result.append(r)
        return result

    def _dialog_node_standard(self, reference, output, condition, previous_sibling):
        return {
            "type": 'standard',
            "title": reference,
            "output": {
                "generic": [
                    {
                        "values": [
                            {
                                "text": output
                            }
                        ],
                        "response_type": "text",
                        "selection_policy": "sequential"
                    }
                ]
            },
            "conditions": condition,
            "dialog_node": reference,
            "previous_sibling": previous_sibling
        }

    def _welcome_node(self, greeting="Hello, how can I help you?"):
        return {
            "type": "standard",
            "title": "Welcome",
            "output": {
                "generic": [
                    {
                        "values": [
                            {
                                "text": greeting
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

    def _else_node(self, previous_sibling, response="Can you reword your statement? I'm not understanding."):
        return {
            "type": "standard",
            "title": "Anything else",
            "output": {
                "generic": [
                    {
                        "values": [
                            {
                                "text": response
                            },
                        ],
                        "response_type": "text",
                        "selection_policy": "sequential"
                    }
                ]
            },
            "conditions": "anything_else",
            "dialog_node": "Anything else",
            "previous_sibling": previous_sibling,
            "disambiguation_opt_out": True
        }

    def _other(self):
        return """
                "metadata": {
                "api_version": {
                  "major_version": "v2",
                  "minor_version": "2021-11-27"
                }
                },
                "counterexamples": [],
                "system_settings": {
                "nlp": {
                  "model": "latest"
                },
                "off_topic": {
                  "enabled": true
                },
                "disambiguation": {
                  "prompt": "Did you mean:",
                  "enabled": false,
                  "randomize": true,
                  "max_suggestions": 5,
                  "suggestion_text_policy": "title",
                  "none_of_the_above_prompt": "None of the above"
                },
                "system_entities": {
                  "enabled": true
                },
                "human_agent_assist": {
                  "prompt": "Did you mean:"
                },
                "spelling_auto_correct": true
                },
                "learning_opt_out": false,
                "name": "Generated Skill",
                "language": "en",
                "description": ""
            """.replace("\n", '').replace(" ", "")

    def generate(self):
        with open("chatbot.json", "w") as f:
            f.write("{" + self._intents() + self._entities() + self._dialog_nodes() + self._other() + "}")
            print('json generated')
            return 'success'

    def get_json(self):
        print('json generated')
        return json.loads("{" + self._intents() + self._entities() + self._dialog_nodes() + self._other() + "}")
