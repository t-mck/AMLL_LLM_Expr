##### required to pip install sseclient-py
##### required to pip install claude-api-py

from claude import claude_client, claude_wrapper
from pprint import pprint
import json
import time
import yaml


class Claude:
    def __init__(self, SESSION_KEY):
        self.client = claude_client.ClaudeClient(SESSION_KEY)
        self.organization_uuid = self.client.get_organizations()[0]['uuid']
        self.claude_obj = claude_wrapper.ClaudeWrapper(self.client, self.organization_uuid)
        self.response_dict = None


    def run_new_query(self, QUERY, MODEL="claude-3-opus-20240229"):

        new_conversation_data = self.claude_obj.start_new_conversation("New Conversation", QUERY, model=MODEL)
        print(new_conversation_data)
        if new_conversation_data is None:
            return {'response':'None'}
        else:
            time.sleep(1)  # to prevent rate limiting
            conversation_uuid = new_conversation_data['uuid']
            # You can get the response from the initial message you sent with:
            initial_response = new_conversation_data['response']
            initial_response['conversation_uuid'] = conversation_uuid

            return initial_response
        


    def run_bulk_queries(self, QUERY_DICT):

        response_dict = {}
        for QUERY_IDX, QUERY in QUERY_DICT.items():
            response = self.run_new_query(QUERY)
            response['query'] = QUERY
            response_dict[f'QID_{QUERY_IDX}'] = response
        
        self.response_dict = response_dict

        return response_dict

    def write_bulk_output_to_json(self, OUTPUT_FNAME):
        assert self.response_dict is not None, 'Response Dictionary is empty'
        with open(OUTPUT_FNAME, "w") as outfile: 
            json.dump(self.response_dict, outfile)


if __name__ == "__main__":

    with open('claude_session_api.yaml') as rf:
        SESSION_KEY = yaml.safe_load(rf)['session_id']

    ##### placeholder for query input
    QUERY_DICT = {
        1: 'Use the chain rule to find the indicated partial derivatives dw/dr and dw/dtheta, where w=xy+yz+zx, x=r* cos(theta), y = r*sin(theta), z = r*theta, when r=2, theta = pi/2'
    }

    claude = Claude(SESSION_KEY)
    
    response_dict = claude.run_bulk_queries(QUERY_DICT)

    pprint(response_dict)
    claude.write_bulk_output_to_json('TEST_JSON_OUTPUT.json')
