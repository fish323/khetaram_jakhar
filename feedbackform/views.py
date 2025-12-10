from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from .forms import Feedform
from .models import Feedback

def contactusview(request):
    # Logic to handle Form Submission
    if request.method == "POST":
        form = Feedform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contactview') # Redirect to same page to prevent re-submission
    else:
        form = Feedform()

    # Logic to fetch last 5 feedback entries (New Code)
    # We order by '-id' to get the most recent ones first
    recent_feedback = Feedback.objects.all().order_by('-id')[:5]

    context = {
        'form' : form,
        'recent_feedback': recent_feedback, # Pass data to template
    }            
    return render(request, 'contact.html', context)