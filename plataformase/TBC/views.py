from django.shortcuts import render
# Create your views here.
def resultadosTBC(request):

	return render(request,'resultadosTBC.html')

def homePage(request):
	return render(request, 'homePage.html')




