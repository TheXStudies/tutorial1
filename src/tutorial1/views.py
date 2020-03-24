from django.shortcuts import render


def index(request):
    a = 20
    b = ['a']
    ctx = {
        'a': a,
        'b': b,
    }


    functions = {
        'a_plus_b': lambda x, y: x + y,
        'a_mul_b': lambda x, y: x * y,
        'b_mul_a': lambda x, y: y * x,
        'a_bitor_b': lambda x, y: x | y,
        'type_of_a': lambda x, y: str(type(x)),
        'type_of_b': lambda x, y: str(type(y)),
    }

    for key, fn in functions.items():
        try:
            ctx[key] = fn(a, b)
        except TypeError:
            ctx[key] = "*ERROR*"

    return render(request, "index.html", context=ctx)