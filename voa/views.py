from django.shortcuts import render


from .tools import mykindle
import sys
# Create your views here.

def index(request):
    try:
        result = mykindle.main()
    except:
        result = sys.exc_info()
    return render(request, 'voa/index.html', {
        'result': result,
    })
