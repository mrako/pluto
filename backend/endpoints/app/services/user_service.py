from ariadne import convert_kwargs_to_snake_case

from dao import organisation_dao
from utils.common import build_result_from_dict


@convert_kwargs_to_snake_case
def get_user_organisational_info(obj, info):
    pluto_user_uuid = info.context['pluto_user'].uuid
    orgs = organisation_dao.find_by_user_account(pluto_user_uuid)
    users = organisation_dao.find_organisational_users(pluto_user_uuid)

    return build_result_from_dict({
        'organisations': orgs,
        'personal_project_users': users
    })
