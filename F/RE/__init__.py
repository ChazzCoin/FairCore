import re

from F import LIST

SEARCH_TERM = lambda searchTerm: fr'.*{str(searchTerm)}.*'
SEARCH_TERM_TWO = lambda searchTerm: fr'\b{searchTerm}\b'
REMOVE_SPECIAL_CHARACTERS = r'[^a-zA-Z0-9]'

FINDALL = lambda regex, content: re.findall(regex, content)
SEARCH = lambda regex, content: re.search(regex, content)

def search(search_term, content):
    match = FINDALL(SEARCH_TERM(search_term), content)
    return match if len(match) >= 1 and match is not None else False

def contains(search_term, content):
    try:
        if type(content) in [list, tuple]:
            for itemContent in content:
                match = re.findall(fr'.*{str(search_term)}.*', itemContent)
                if len(match) >= 1 and match is not None:
                    return True
            return False
        else:
            match = re.findall(fr'.*{str(search_term)}.*', content)
            return True if len(match) >= 1 and match is not None else False
    except Exception as e:
        print(f"Failed to regex findall. {str(search_term)}, error=[ {e} ]")
        return False

def contains_strict(search_term, content):
    try:
        if type(content) in [list, tuple]:
            for itemContent in content:
                search_term = __remove_special_characters(search_term)
                match = re.findall(fr'\b{search_term}\b', itemContent)
                if len(match) >= 1 and match is not None:
                    return True
            return False
        else:
            search_term = __remove_special_characters(search_term)
            match = re.findall(fr'\b{search_term}\b', content)
            return True if len(match) >= 1 and match is not None else False
    except Exception as e:
        print(f"Failed to regex findall. {search_term}, error=[ {e} ]")
        return False

def contains_any(search_terms, content):
    search_terms = LIST.flatten(search_terms)
    for term in search_terms:
        temp = contains(term, content)
        if temp:
            return True
    return False

def locate_term_in_str(term, content):
    match = re.search(fr'\b{term}\b', content)
    if match:
        return match
    return False


def __remove_special_characters(text):
    """ DEPRECATED """
    newText = re.sub('[^a-zA-Z0-9]', ' ', text)
    return newText