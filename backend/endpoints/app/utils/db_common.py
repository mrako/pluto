from utils.common import build_result, build_error_result, success_result


def query_db(result_field_name: str, dao_function, **kwargs):
    return execute_db(result_field_name, dao_function, operation='Retrieving', **kwargs)


def update_db(result_field_name: str, dao_function, **kwargs):
    return execute_db(result_field_name, dao_function, operation='Updating', **kwargs)


def execute_db(result_field_name: str, dao_function, operation: str = 'Querying', **kwargs):
    return build_result(result_field_name, dao_function(**kwargs))


def delete_from_db(object_name: str, dao_function, **kwargs):
    try:
        # Execute the dao method
        dao_function(**kwargs)

        # Return result
        return success_result()
    except Exception as e:
        msg = f"Deleting {object_name} with args {kwargs} failed"
        return build_error_result(msg, 500, e)

