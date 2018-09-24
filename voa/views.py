from django.shortcuts import render


from .tools import mykindle

# Create your views here.

def index(request):
    try:
        result = mykindle.main()
    except:
        result = 'fail'

    return render(request, 'voa/index.html', {
        'result': result,
    })
