import requests
import datetime
import logging
import re
import uuid
import json
from api_address import *
from http_responces import *

# domain, username, password, bearer = None
token = { "Authorization": None }
credentials = { "domain": None, "username": None, "password": None, "bearer": None }


log = logging.getLogger()
console = logging.StreamHandler()
console.setFormatter(logging.Formatter("%(asctime)s\t%(levelname)s -- %(message)s"))
log.addHandler(console)
log.setLevel(20)

def connect(domain: str, username: str, password: str, bearer: str) -> None:
    global token
    global credentials


    if bearer:
        headers = { 'Authorization' : f'Bearer {bearer}' }
        method = 'token'
    else:
        headers = { f'{username}':f'{password}' }
        method = f'user auth {username}'
    
    response = requests.get(f"https://{domain}{db_api}{get_warehouses}", headers = headers)
    
    if response.status_code == HTTP_OK:
        set_credentials(domain, username, password, bearer)
        set_token(bearer)
        log.info("Connected to the Power BI REST API with {}".format(method))
    else:
        set_credentials(None, None, None, None)
        set_token(None)
        log.error("Error {} -- Something went wrong when trying to retrieve the token from the REST API".format(response.status_code))

def set_credentials(domain: str, username: str, password: str, bearer: str) -> None:
    global credentials
    credentials["domain"] = domain
    credentials["username"] = username
    credentials["password"] = password
    credentials["bearer"] = bearer

def set_token(bearer: str) -> None:
    global token
    token["Authorization"] = "Bearer {}".format(bearer)

def verify_token() -> bool:
    global token
    if token["Authorization"] == None:
        log.error("Error 401 -- Please connect to the Power BI REST API with the connect() function before")
        return False
    else:
        connect(credentials["domain"], credentials["username"], credentials["password"], credentials["bearer"])
        return True

def get_token() -> dict:
    global token
    return

def get_credentials() -> dict:
    global credentials
    return

def request_get(api_query: str , body: dict =None) -> dict:
    global token
    if(not verify_token()): return None
    if body is None:
        response = requests.get(f"https://{domain}{db_api}{api_query}", headers = token)
    else:
        response = requests.get(f"https://{domain}{db_api}{api_query}", headers = token,  data = body)
        
    if response.status_code == HTTP_OK:
        set_credentials(domain, username, password, bearer)
        set_token(bearer)
        log.info("Connected to the databricks REST API")
        return response.text
    else:
        # set_credentials(domain, username, password, bearer)
        # set_token(bearer)
        set_credentials(None, None, None, None)
        set_token(None)
        log.error("Error -- Something went wrong when trying to retrieve the token from the REST")
        return {}
    
def request_post(api_query: str , body: dict =None) -> dict:
    global token
    if(not verify_token()): return None
    if body is None:
        response = requests.post(f"https://{domain}{db_api}{api_query}", headers = token)
    else:
        response = requests.post(f"https://{domain}{db_api}{api_query}", headers = token,  data = json.dumps(body))
        
    if response.status_code == HTTP_OK:
        set_credentials(domain, username, password, bearer)
        set_token(bearer)
        log.info("Connected to the databricks REST API")
        return response.text
    else:
        # set_credentials(domain, username, password, bearer)
        # set_token(bearer)
        set_credentials(None, None, None, None)
        set_token(None)
        log.error(f"Error -- Something went wrong when trying to retrieve the token from the REST {response.status_code}")
        return {}


def request_delete(api_query: str , body: dict =None) -> dict:
    global token
    if(not verify_token()): return None
    if body is None:
        response = requests.post(f"https://{domain}{db_api}{api_query}", headers = token)
    else:
        print(f"https://{domain}{db_api}{api_query}")
        print(f"{token}")
        print(json.dumps(body))
        response = requests.delete(f"https://{domain}{db_api}{api_query}", headers = token,  data = json.dumps(body))
        
    if response.status_code == HTTP_OK:
        set_credentials(domain, username, password, bearer)
        set_token(bearer)
        log.info("Connected to the databricks REST API")
        return response.text
    else:
        # set_credentials(domain, username, password, bearer)
        # set_token(bearer)
        set_credentials(None, None, None, None)
        set_token(None)
        log.error(f"Error -- Something went wrong when trying to retrieve the token from the REST {response.status_code}")
        return {} 

def retrieve_a_list_of_queries(page_size:int =50,
                              page: int =1,
                              order:str ='-executed_at',
                              q:str =None) -> dict:
    data = {
        "page_size": page_size,
        "page": page,
        "order": order,
        "q": q
    }
    return request_get(api_get_retrieve_a_list_of_queries,data)

def create_a_new_query_definition (
    data_source_id:str =None,
    description:str =None,
    name:str =None,
    options:dict =None,
    parent:str ='/Users/dummy.name@dummy.com/dummy',
    query:str =None,
    schedule:dict =None) -> dict:
    u_id = str(uuid.uuid1())
    if data_source_id is None: data_source_id = u_id
    if description is None: description = "This is SQL Query created by the API."
    if name is None: name = "API Created SQL"
    if options is None: options  = {
        "parameters": [
            {
                "name": "cob_date_id",
                "title": "cob_date_id",
                "type": "text",
                "value": "2022012"
            }
        ]
        }
    if query is None: query =  "SELECT field FROM dummy WHERE cob_date_id = {{ cob_date_id }}"
    if schedule is None: schedule = {
            "day_of_week": "Wednesday",
            "interval": 86400,
            "time": "06:15",
            "until": "1991-08-03"
        }
    data = {
            "data_source_id": data_source_id,
            "description": description,
            "name": name,
            "options": options,
            "parent": parent,
            "query": query,
            "schedule": schedule
        }
    return request_post(api_post_create_a_new_query_definition,data)

# Token managment 

def create_token(comment:str ='This is an example token created from API',
                lifetime_seconds:int =7776000) -> dict:
    data  = { 
        "comment": comment,
        "lifetime_seconds": lifetime_seconds
    }
    return request_post(api_post_create_token,data)

def delete_token(token_id:str) -> dict:
    data = {
        token_id: token_id
    }
    return request_post(api_post_delete_token,data)

def list_token() -> dict:
    return request_get(api_get_list_token)

# User Groups managment 

def get_groups() ->dict:
    return request_get(api_get_groups)


def get_groups(group_name:str) ->dict:
    return request_get(f"{api_get_group_by_id}{group_name}")


def create_group(group_name:str, user_id:str) ->dict:
    data = {
        "schemas": [ "urn:ietf:params:scim:schemas:core:2.0:Group" ],
        "displayName": group_name,
        "members": [
            {
                "value": user_id
                }
            ]
        }
    return request_post(api_post_create_group,data)


def update_group(user_id:str) -> dict:
    # Azure Databricks does not support updating group names. this is a placeholder 
    data = {
        "schemas": [ "urn:ietf:params:scim:api:messages:2.0:PatchOp" ],
        "Operations": [
            {
                "op":"add",
                "value":
                {
                    "members": 
                    [
                        {
                            "value": user_id
                            }
                        ]
                    }
                }
            ]
    }
    return request_post(f"{api_post_update_group}{user_id}",data)


def add_group(user_id:str) -> dict:
    data = {
        "schemas": [ "urn:ietf:params:scim:api:messages:2.0:PatchOp" ],
        "Operations": [
            {
                "op":"add",
                "value":
                {
                    "members": 
                    [
                        {
                            "value": user_id
                            }
                        ]
                    }
                }
            ]
    }
    return request_post(f"{api_post_add_group}{user_id}",data)


def remove_from_group(user_id:str) -> dict:
    data = {
        "schemas": [ "urn:ietf:params:scim:api:messages:2.0:PatchOp" ],
        "Operations": [
            {
                "op": "remove",
                "path": f"members[value eq \"{user_id}\"]"
            }
        ]
    }
    return request_post(f"{api_post_remove_from_group}{user_id}",data)


def delete_group(user_id:str) -> dict:
    return request_delete (f"{api_post_remove_from_group}{user_id}")


# Cluster managment
def cluster_info_get() -> dict:
    return  request_get(api_get_cluster_info_get)


def cluster_list() -> dict:
    return  request_get(api_get_cluster_list)


def cluster_response_structure() -> dict:
    return  request_get(api_get_cluster_response_structure)


def cluster_run_time_versions() -> dict:
    return  request_get(api_get_cluster_run_time_versions)


def cluster_create(cluster_name:str, spark_version:str,node_type_id:str,num_workers:int) -> dict:
    data = {
        "cluster_name": cluster_name,
        "spark_version": spark_version,
        "node_type_id": node_type_id,
        "spark_conf": {
            "spark.speculation": True
            },
        "num_workers": num_workers
    }
    return request_post(api_post_cluster_create, data)


def cluster_start(cluster_id:str) -> dict:
    data = { "cluster_id": cluster_id }
    return request_post(api_post_cluster_start, data)


def cluster_restart(cluster_id:str) -> dict:
    data = { "cluster_id": cluster_id }
    return request_post(api_post_cluster_restart, data)


def cluster_request_structure(cluster_id:str) -> dict:
    data = { "cluster_id": cluster_id }
    return request_post(api_post_cluster_request_structure, data)


def cluster_terminate(cluster_id:str) -> dict:
    data = { "cluster_id": cluster_id }
    return request_post(api_post_cluster_terminate, data)


def cluster_permanent_delete(cluster_id:str) -> dict:
    data = { "cluster_id": cluster_id }
    return request_post(api_post_cluster_permanent_delete, data)


def cluster_events(
    cluster_id:str,
    start_time:int,
    end_time:int, 
    order:str ='DESC', 
    offset:int =10, 
    limit:int =5,
    event_type:str = 'RUNNING' ) -> dict:
    data = {
        "cluster_id": cluster_id,
        "start_time": start_time,
        "end_time": end_time,
        "order": order,
        "offset": offset,
        "limit": limit,
        "event_type": event_type
    }
    return request_post(api_post_cluster_events, data)