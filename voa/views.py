from django.shortcuts import render


from .tools import mykindle
import traceback
# Create your views here.

def index(request):
    try:
        result = mykindle.main()
    except Exception, e:
        result = 'fail ,str(Exception):\t%s\n str(e):\t\t%s \nrepr(e):\t%s\ne.message:\t%s\ntraceback.print_exc():%s\ntraceback.format_exc():\n%s'%(str(Exception),str(e),repr(e),e.message,traceback.print_exc(),traceback.format_exc())
    return render(request, 'voa/index.html', {
        'result': result,
    })
