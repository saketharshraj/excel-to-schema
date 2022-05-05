def fix_key(s):
    s = s.split()[0]
    s = s[0].lower() + s[1:]
    return s


def fix_types(s):
    s = s.lower().strip()
    if s == 'string':
        return 'String'
    elif s == 'number':
        return 'Number'
    elif s == 'objectid':
        return 'ObjectId'
    elif s == 'date':
        return 'Date'
    elif s in ('array(strings)', '[strings]', '[string]', 'array[string]'):
        return '[String]'
    elif s in ('array(objectid)', '[objectid]'):
        return '[ObjectId]'


def fix_required(s):
    s = str(s).strip().lower()
    if s.lower() == 'true':
        return 1
    else:
        return 0


def fix_ref(s):
    s = s.strip()
    if s in ('-', '', 'null'):
        return ''
    else:
        return s


def fix_default(s, kt):
    if s in ('-', '', 'null'):
        return ''
    else:
        if kt == 'Number':
            return int(s)
        return s


def fix_enum(s):
    if s in ('-', '', 'null'):
        return ''
    s = s.split()
    final_enum = f"""
                enum: ["""
    for i in range(0, len(s), 2):
        final_enum += f"""
                    {s[i]}, // {s[i + 1]},"""
    final_enum += f"""
                ]"""

    return final_enum


def fix_model_name(s):
    s = s.replace(' ', '-')
    s = s.replace('--', '-')
    s = s.replace('---', '-')
    s = s.replace('\n', '-')
    s = s.split('-')
    new_name = s[0]
    for i in s[1:]:
        new_name += i[0].upper() + i[1:]
    return new_name
