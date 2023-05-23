import os


text = "Ich suche einen Anfängerkurs am 21. Hat jemand eine Ahnung? :)"

# get search strings from env
os.environ["search_strings"] = "20.;21."
search_strings_from_env = os.environ.get("search_strings")
print(search_strings_from_env.split(";"))


def does_include_search_string(text: str, search_strings: list) -> bool:
    for search_string in search_strings:
        if text.find(search_string) != -1:
            return True
        else:
            return False


print(does_include_search_string(text, search_strings_from_env))
