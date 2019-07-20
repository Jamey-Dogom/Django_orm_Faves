import inspect

def copy_dict_partial(source_dict, keys_to_remove = []):

    copy = source_dict.copy()

    if 'csrfmiddlewaretoken' in source_dict:
        keys_to_remove.append('csrfmiddlewaretoken')
    
    for key in keys_to_remove:
        del copy[key]

    return copy

def key_formatter(key):
    key = key.replace("_", " ")
    return key.title()

def stringify_obj(obj, excluded_keys=["created_at", "updated_at", "password"], title_case=False):
    s = "***"
    items = []

    if type(obj) is dict:
        items = obj.items()
    elif inspect.isclass(type(obj)):
        items = vars(obj).items()

    for key, val in items:
        if key not in excluded_keys:
            s += f" | {key_formatter(key) if title_case else key}: {val}"
            
    return s + " ***"

def print_items_new_line(lst):
    for item in lst:
        print(item)