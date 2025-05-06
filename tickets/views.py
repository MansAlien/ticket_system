# views.py
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

def register(request):
    if request.user.is_authenticated:
        return redirect('/admin/')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/admin')
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})
