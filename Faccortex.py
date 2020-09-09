import json
import ssl
import time
from itertools import cycle
from tkinter import *
import websocket

class Cortex():
    def __init__(self, url, user,debug_mode=False):
        self.ws = websocket.create_connection(url, sslopt={"cert_reqs": ssl.CERT_NONE})
        self.user = user
        self.packet_count = 0
        self.count = 0
        self.id_sequence = 0
        self.debug=debug_mode
        self.switch_on_off=None


    def query_headset(self):
        QUERY_HEADSET_ID = 2

        query_headset_request = {
            "jsonrpc": "2.0",
            "id": QUERY_HEADSET_ID,
            "method": "queryHeadsets",
            "params": {}
        }

        self.ws.send(json.dumps(query_headset_request))
        result = self.ws.recv()
        result_dic = json.loads(result)
        if result_dic['result'] == []:
            print("connect your device")
        # print('query headset result', json.dumps(result_dic, indent=4))
        self.headset_id = result_dic['result'][0]['id']
        print(self.headset_id)

    def connect_headset(self):
        CONNECT_HEADSET_ID = 111

        connect_headset_request = {
            "jsonrpc": "2.0",
            "id": CONNECT_HEADSET_ID,
            "method": "controlDevice",
            "params": {
                "command": "connect",
                "headset": self.headset_id
            }
        }

        self.ws.send(json.dumps(connect_headset_request))
        result = self.ws.recv()
        result_dic = json.loads(result)
        print('connect headset result', json.dumps(result_dic, indent=4))

    def request_access(self):
        REQUEST_ACCESS_ID = 1
        request_access_request = {
            "jsonrpc": "2.0",
            "method": "requestAccess",
            "params": {
                "clientId": self.user['client_id'],
                "clientSecret": self.user['client_secret']
            },
            "id": REQUEST_ACCESS_ID
        }
        self.ws.send(json.dumps(request_access_request))
        result = self.ws.recv()
        result_dic = json.loads(result)
        print(json.dumps(result_dic, indent=4))

    def authorize(self):
        AUTHORIZE_ID = 4
        authorize_request = {
            "jsonrpc": "2.0",
            "method": "authorize",
            "params": {
                "clientId": self.user['client_id'],
                "clientSecret": self.user['client_secret'],
                "license": self.user['license'],
                "debit": self.user['debit']
            },
            "id": AUTHORIZE_ID
        }
        print('json.dumps(authorize_request)', json.dumps(authorize_request))
        self.ws.send(json.dumps(authorize_request))
        result = self.ws.recv()
        result_dic = json.loads(result)
        print('auth_result', json.dumps(result_dic, indent=4))
        self.auth = result_dic['result']['cortexToken']
        print(self.auth)

    def create_session(self, auth, headset_id):
        CREATE_SESSION_ID = 5
        create_session_request = {
            "jsonrpc": "2.0",
            "id": CREATE_SESSION_ID,
            "method": "createSession",
            "params": {
                "cortexToken": self.auth,
                "headset": self.headset_id,
                "status": "active"
            }
        }
        self.ws.send(json.dumps(create_session_request))
        result = self.ws.recv()
        result_dic = json.loads(result)
        print('create session result ', json.dumps(result_dic, indent=4))
        self.session_id = result_dic['result']['id']
        # print(self.session_id)

    def close_session(self):
        CREATE_SESSION_ID = 117
        close_session_request = {
            "jsonrpc": "2.0",
            "id": CREATE_SESSION_ID,
            "method": "updateSession",
            "params": {
                "cortexToken": self.auth,
                "session": self.session_id,
                "status": "close"
            }
        }

        self.ws.send(json.dumps(close_session_request))
        result = self.ws.recv()
        result_dic = json.loads(result)
        print('close session result ', json.dumps(result_dic, indent=4))

    #def get_cortex_info(self):
     #   get_cortex_info_request = {
      #      "jsonrpc": "2.0",
       #     "method": "getCortexInfo",
        #    "id": 100
       # }
       # self.ws.send(json.dumps(get_cortex_info_request))
        #result = self.ws.recv()
        #print(json.dumps(json.loads(result), indent=4))

    def grant_access_and_session_info(self):
        self.query_headset()
        self.connect_headset()
        self.request_access()
        self.authorize()
        self.create_session(self.auth, self.headset_id)


    def sub_request(self, stream):
        print('subscribe request --------------------------------')
        SUB_REQUEST_ID = 6
        sub_request_json = {
            "jsonrpc": "2.0",
            "method": "subscribe",
            "params": {
                "cortexToken": self.auth,
                "session": self.session_id,
                "streams": stream
            },
            "id": SUB_REQUEST_ID
        }

        self.ws.send(json.dumps(sub_request_json))

        if 'sys' in stream:
            new_data = self.ws.recv()
            print(json.dumps(new_data, indent=4))
            print('\n')
        else:
            while True:
                new_data = self.ws.recv()
                print(new_data)

    def gen_request(self, method, auth, **kwargs):
        self.id_sequence += 1
        params = {key: value for (key, value) in kwargs.items()}
        if auth and self.auth:
            params['cortexToken'] = self.auth
        request = json.dumps(
            {'jsonrpc': "2.0",
             'method': method,
             'params': params,
             'id': self.id_sequence
             })
        print(f"Sending request:\n{request}")
        return request

    def send_command(self, method, auth=True, callback=None, **kwargs):
        if auth and not self.auth:
            self.authorize()
        msg = self.gen_request(method, auth, **kwargs)
        self.ws.send(msg)
        print("sent; awaiting response")
        resp = self.ws.recv()
        if 'error' in resp:
            print(f"Got error in {method} with params {kwargs}:\n{resp}")
            raise Exception(resp)
        resp = json.loads(resp)
        if callback:
            callback(resp)
        return resp

    def setup_profile(self, profile_name, status):
        SETUP_PROFILE_ID = 7
        print('setup profile --------------------------------')
        setup_profile_json = {
            "jsonrpc": "2.0",
            "method": "setupProfile",
            "params": {
                "cortexToken": self.auth,
                "headset": self.headset_id,
                "profile": profile_name,
                "status": status
            },
            "id": SETUP_PROFILE_ID
        }

        if self.debug:
            print('setup profile json:\n', json.dumps(setup_profile_json, indent=4))
            print('\n')

        self.ws.send(json.dumps(setup_profile_json))

        result = self.ws.recv()
        result_dic = json.loads(result)

        if self.debug:
            print('result \n', json.dumps(result_dic, indent=4))
            print('\n')

    def train_request(self, detection, action, status):
        # print('train request --------------------------------')
        TRAINING_ID = 9
        train_request_json = {
            "jsonrpc": "2.0",
            "method": "training",
            "params": {
                "cortexToken": self.auth,
                "detection": detection,
                "session": self.session_id,
                "action": action,
                "status": status
            },
            "id": TRAINING_ID
        }

        # print('training request:\n', json.dumps(train_request_json, indent=4))
        # print('\n')

        self.ws.send(json.dumps(train_request_json))

        if detection == 'mentalCommand':
            start_wanted_result = 'MC_Succeeded'
            accept_wanted_result = 'MC_Completed'

        if detection == 'facialExpression':
            start_wanted_result = 'FE_Succeeded'
            accept_wanted_result = 'FE_Completed'

        if status == 'start':
            wanted_result = start_wanted_result
            print('\n YOU HAVE 8 SECONDS FOR TRAIN ACTION {} \n'.format(action.upper()))

        if status == 'accept':
            wanted_result = accept_wanted_result

        # wait until success
        while True:
            result = self.ws.recv()
            result_dic = json.loads(result)

            print(json.dumps(result_dic, indent=4))

            if 'sys' in result_dic:
                # success or complete, break the wait
                if result_dic['sys'][1] == wanted_result:
                    break

    def disconnect_headset(self):
        DISCONNECT_HEADSET_ID = 112

        disconnect_headset_request = {
            "jsonrpc": "2.0",
            "id": DISCONNECT_HEADSET_ID,
            "method": "controlDevice",
            "params": {
                "command": "disconnect",
                "headset": self.headset_id
            }
        }

        self.ws.send(json.dumps(disconnect_headset_request))

        # wait until disconnect completed
        while True:
            time.sleep(1)
            result = self.ws.recv()
            result_dic = json.loads(result)

            print('disconnect headset result', json.dumps(result_dic, indent=4))

            if 'warning' in result_dic:
                if result_dic['warning']['code'] == 1:
                    break

    def subscribe(self, stream_list):
        params = {'cortexToken': self.auth,
                  'session': self.session_id,
                  'streams': stream_list}
        resp = self.send_command('subscribe', **params)
        print(f"{__name__} resp:\n{resp}")

    def get_data(self):
        while True:
            resp = self.ws.recv()
            res = json.loads(resp)
            val = res['fac']
            eyeact = val[0]
            alternator = cycle(("on", "off"))
            if eyeact == 'blink':
                self.count += 1
                if self.count == 14:
                    self.switch_on_off=next(alternator)
                    print(self.switch_on_off)
                    #time.sleep(0.5)
                if self.count == 24:
                    self.switch_on_off="off"
                    print(self.switch_on_off)
                    self.count = 0
                    #time.sleep(0.5)
            self.packet_count += 1


    def queryProfile(self):
        QUERY_PROFILE_ID = 15
        queryProfileRequest = {
            "jsonrpc": "2.0",
            "method": "queryProfile",
            "params": {
                "cortexToken": self.auth,
            },
            "id": QUERY_PROFILE_ID
        }
        print('query profile:\n', json.dumps(queryProfileRequest))
        print('\n')
        self.ws.send(json.dumps(queryProfileRequest))

        result = self.ws.recv()
        result_dic = json.loads(result)
        self.queryProfile = result_dic
        print('result queryProfile\n', result_dic)
        print('\n')

    def delete(self, detection, action, status):
        TRAINING_ID = 9
        train_request_json = {
            "jsonrpc": "2.0",
            "method": "training",
            "params": {
                "cortexToken": self.auth,
                "detection": detection,
                "session": self.session_id,
                "action": action,
                "status": status
            },
            "id": TRAINING_ID
        }
        print('command erase initiated\n')
        self.ws.send(json.dumps(train_request_json))
        result = self.ws.recv()
        result_dic = json.loads(result)
        print('command erase done\n',result_dic)