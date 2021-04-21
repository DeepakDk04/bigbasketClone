from django.shortcuts import render

# Create your views here.
def sampleView(request):
    context = {}
    return render(request, 'product.html', context)