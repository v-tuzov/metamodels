# -*- coding: utf-8 -*-


import os
import threading
from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from django import forms
import dynamic.models


def reload_self():
    os.system('touch %s/%s' % (settings.DIRNAME, 'manage.py'))


class DForm(forms.Form):
    
    file = forms.FileField(required=True)
    

def view_index(request):
    
    page2show = 'index.html'
    vars = {}
    
    form = DForm(request.POST, request.FILES)
    
    if request.method == "POST":
        form = DForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                dynamic.models.load_models(form.cleaned_data.get('file').name)
            except Exception, e:
                vars['syntax_error'] = e
            if not vars.get('syntax_error'):    
                inp = open(form.cleaned_data.get('file').name)
                out = open('/tmp/models.dump','w')
                out.write(inp.read())
                out.close()
                vars['created'] = True
                t = threading.Timer(2.0, reload_self)
                t.start()
        else:
            pass           
    vars['form'] = form
    return render_to_response(page2show, vars, context_instance=RequestContext(request))
