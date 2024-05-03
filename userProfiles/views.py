from django.shortcuts import render
from django.http import HttpResponse

# This is a single View. Sort of like a class. for now its called view1
def view1(request):
    #template = loader.get_template('myfirst.html')
    #return HttpResponse(template.render())

    return render(request, 'myfirst.html')
