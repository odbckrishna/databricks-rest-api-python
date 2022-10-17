db_api = '/api/2.0'
get_warehouses = '/sql/warehouses/'
queries_dashboards = '/api/2.0/preview/sql'
retrieve_a_list_of_queries = '/preview/sql/queries'
api_get_retrieve_a_list_of_queries = '/preview/sql/queries'
api_post_create_a_new_query_definition = '/preview/sql/queries'


#Token 
api_post_create_token = '/token/create' 
api_get_list_token = '/token/list' 
api_post_delete_token = '/token/delete' 

# groups
api_get_groups = '/preview/scim/v2/Groups'
api_get_group_by_id = '/preview/scim/v2/Groups/'
api_post_create_group = '/preview/scim/v2/Groups'
api_post_update_group = '/preview/scim/v2/Groups/'
api_post_add_group = '/preview/scim/v2/Groups/'
api_post_remove_from_group = '/preview/scim/v2/Groups/'

# Cluster
api_get_cluster_info_get = '/clusters/get'
api_get_cluster_list = '/clusters/list'
api_get_cluster_response_structure = '/clusters/list-node-types'
api_get_cluster_run_time_versions = '/clusters/spark-versions'
api_post_cluster_create = '/clusters/create'
api_post_cluster_start = '/clusters/start'
api_post_cluster_restart = '/clusters/restart'
api_post_cluster_request_structure = '/clusters/resize'
api_post_cluster_terminate = '/clusters/delete'
api_post_cluster_permanent_delete = '/clusters/permanent-delete'
api_post_cluster_events = '/clusters/events'