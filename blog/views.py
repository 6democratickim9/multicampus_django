from django.shortcuts import render
from django.http import HttpResponse
# Post 목록
def post_list(request):
    name = 'Django'
    response = HttpResponse(content_type ="text/html")
    response.write(f'<h2>Hello {name}</h2>',)
    response.write(f'<p>HTTP Method : {request.method}</p>')
    response.write(f'<p>HTTP ConentType : {request.content_type}</p>')
    # return HttpResponse(f'''<h2>Hello{name}</h2><p>HTTP METHOD : {request.method}</p>''')

    return response