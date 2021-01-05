VOWELS = set('aeiou')


def pluralize(word: str) -> dict:
    res = {'plural': '', 'status': ''}
    # capital to lower
    ori_word = word
    word = str.lower(word)
    # empty string, {'', 'empty_string'}
    if '' == word:
        res['status'] = 'empty_string'
        return res

    # proper noun, if in proper_nouns.txt, return {word, 'proper_noun'}
    # retain original capitalization
    if check_if_string_in_file('proper_nouns.txt', word):
        res['plural'] = ori_word
        res['status'] = 'proper_noun'
        return res
    # already plural, return {word, 'already_in_plural'}
    if word.endswith('s'):
        res['plural'] = ori_word
        res['status'] = 'already_in_plural'
        return res

    # not plural, not proper
    # ends with vowel, add -s
    if word[-1] in VOWELS:
        res['plural'] = ori_word + 's'
        res['status'] = 'success'
        return res
    # If it ends with 'y' and is preceded by a consonant, erase the last letter and add - ies.
    if word.endswith('y') and word[-2] not in VOWELS:
        res['plural'] = ori_word[:-1] + 'ies'
        res['status'] = 'success'
        return res
    if word.endswith('f'):
        res['plural'] = ori_word[:-1] + 'ves'
        res['status'] = 'success'
        return res
    if word[:-2] in ['sh', 'ch']:
        res['plural'] = ori_word[:-2] + 'es'
        res['status'] = 'success'
        return res
    if word[-1] == 'z':
        res['plural'] = ori_word[:-1] + 'es'
        res['status'] = 'success'
        return res
    res['plural'] = ori_word + 's'
    res['status'] = 'success'
    return res


def check_if_string_in_file(file_name, string_to_search):
    with open(file_name, 'r') as read_obj:
        for line in read_obj:
            if string_to_search == line.strip():
                return True
    return False


if __name__ == '__main__':
    print(pluralize("failure"))
    print(pluralize("Zulma"))
    print(pluralize("injury"))
    print(pluralize("elf"))
    print(pluralize("buzz"))
    print(pluralize("computers"))
    print(pluralize("PCs"))
    print(pluralize(""))
    print(pluralize("highway"))
    print(pluralize("presentation"))
    print(pluralize("pouch"))
    print(pluralize("COVID-19"))
    print(pluralize("adam"))
