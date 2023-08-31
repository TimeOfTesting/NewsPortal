from django import template

register = template.Library()

@register.filter
def censor(value, change_word):
    try:
        if isinstance(value, str):
            value = value.split()
            new_value = ''
            for i in value:
                if change_word in i:
                    result = change_word[0]
                    for j in i[1:]:
                        if j.isalpha():
                            result += '*'
                        else:
                            result += j
                    new_value += result + ' '
                if change_word not in i:
                    new_value += i + ' '
            return new_value
    except TypeError:
        return 'Неверный тип данных'