PARSE_BY_GROUP_CODE = """
var result = [];
var ids = [];
var offset = {offset};
var count_id = 0;
var call = 22;
var fields = "bdate, can_post, about, can_see_audio, can_write_private_message, city, counters, country, has_photo, last_seen, online, personal, relation, sex, status";
var vk_params_get = {{"fields": fields}};
var vk_params = {vk_params};
vk_params.count = 1000;
vk_params.offset = offset;

var response = API.groups.getMembers(vk_params);
count_id = response.count;
ids = response.items;
vk_params_get.user_ids = ids;
result = API.users.get(vk_params_get);

if (offset >= count_id){{    
    return {{"offset": offset, "count_id": count_id, "result": result}};
}}

while (call >= 1){{
    offset = offset + 1000;
    vk_params.offset = offset;
    
    response = API.groups.getMembers(vk_params);
    
    ids = response.items;
    vk_params_get.user_ids = ids;
    
    result = result + API.users.get(vk_params_get);
    call = call - 2;
    
    if (offset >= count_id){{
        call = 0;
    }}
}}

return {{"result": result, "offset": offset, "count_id": count_id}};
"""

EASY_PARSE_BY_GROUP_CODE = """
var response = {{}};
var result = [];
var ids = [];
var count_id = 0;
var call = 25;

var offset = {offset};
var vk_params = {vk_params};
vk_params.offset = offset;
vk_params.count = 1000;

while (call > 0){{
    response = API.groups.getMembers(vk_params);
    count_id = response.count;
    result = result + response.items;

    if (offset >= count_id){{
        call = 0;
    }} else {{
        offset = offset + 1000;
        vk_params.offset = offset;
    }}

    call = call - 1;
}}

return {{"offset": offset, "count_id": count_id, "result": result}};
"""