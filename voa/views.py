from django.shortcuts import render


from .tools import mykindle
import sys
# Create your views here.

def index(request):
    #try:
    result = mykindle.main()
    #except:
    #    result = str(sys.exc_info()[2].tb_lasti) +':' + str(sys.exc_info()[2].tb_lineno)
    #    print(dir(result[2]))  'tb_frame', 'tb_lasti', 'tb_lineno', 'tb_next']
    return render(request, 'voa/index.html', {
        'result': result,
    })
