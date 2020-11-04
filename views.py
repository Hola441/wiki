from django.shortcuts import render
# from django.http import HttpResponse

from . import util, views, urls

from django.shortcuts import redirect
import random
import markdown2
from django import forms


def index(request):
    entries = util.list_entries()
    return render(request, "encyclopedia/index.html", {   
        "entries": entries,
        "length": len(entries)      
    })
def newPage(request):
    return render(request, "encyclopedia/newPage.html", {
        "form": NewPageForm()
    })
def pages(request, page): 
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            ex = form.cleaned_data["mc"]
            page = form.cleaned_data["title"]
            util.save_entry(page, ex)
            return redirect('pages', page)
        return render(request, "encyclopedia/pages.html", {
            "page": page,
            "ex": form   
        })
    if page.lower() == 'random':
        page = random.choice(util.list_entries())
    page = page.capitalize()
    explanation = util.get_entry(page)
    if explanation == None:
        ex = "Error"
    else:
        ex = markdown2.markdown(explanation)
    return render(request, "encyclopedia/pages.html", {
        "page": page,
        "ex": ex   
    })
def icontains(fullStr, page):
    return fullStr.lower().find(page.lower()) > -1
def searchResults(request):
    page = request.GET.get('q')
    if util.get_entry(page) != None:
        ex = markdown2.markdown(util.get_entry(page))
        return render(request, "encyclopedia/pages.html", {
            "page": page,
            "ex": ex
        })
    hello = util.list_entries()
    entries = []
    for i in hello:
        if icontains(i, page):
            entries.append(i)
    return render(request, "encyclopedia/index.html", {
        "entries": entries,
        "length": len(entries)
    })
def editPage(request, page):
    return render(request, "encyclopedia/editPage.html", {
            "page": page,
            "ex": util.get_entry(page),
            "form": EditPageForm()
    })
def savePage(request, page):
    if request.method == "POST":
        form = EditPageForm(request.POST)
        if form.is_valid():
            ex = form.cleaned_data["mc"]
            util.save_entry(page, ex)
            return redirect('pages', page)
        return render(request, "encyclopedia/pages.html", {
            "page": page,
            "ex": "Error"   
        })
    return render(request, "encyclopedia/pages.html", {
        "page": page,
        "ex": 'error'   
    })
class NewPageForm(forms.Form):
    title = forms.CharField(label="Title")
    mc = forms.CharField(widget=forms.Textarea(attrs={'value': "hello"}), label="Markdown Contents")
class EditPageForm(forms.Form):
    mc = forms.CharField(widget=forms.Textarea(attrs={'value': "hello"}), label="Markdown Contents")
