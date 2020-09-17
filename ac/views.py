from django.shortcuts import render
from .models import Ac,Rule
from . import forms
from .computePower import fuzzify_temperature,fuzzify_humidity,defuzzify

def index(request):
    ac_dict = {}

    form = forms.FormName(request.POST)

    # task_list = Tasks.objects.order_by("task_id")

    if form.is_valid():

        print("Form validation")
        print("Temperature : " , form.cleaned_data['temperature'])
        print("Humidity : " , form.cleaned_data['humidity'])

        # compute power
        temperature = form.cleaned_data['temperature']
        humidity = float(form.cleaned_data['humidity'])
        
        ft = fuzzify_temperature(temperature)
        fh = fuzzify_humidity(humidity)
        print("Fuzzy Temp : ",ft)
        print("Fuzzy Humidity : ",fh)
        fp = Rule.objects.filter(temperature = ft , humidity = fh)[0].power
        print("Fuzzy Power : ",fp)
        power = defuzzify(fp)

        ac_dict['power'] = power

        # put in database
        ac_instance = Ac()
        ac_instance.temperature = temperature
        ac_instance.humidity = humidity
        ac_instance.power = power
        ac_instance.save()
        print('Saved in db')

    return render(request,'index.html',context=ac_dict)

def stored(request):
    st_dict = {}

    st_list = Ac.objects.all()
    st_dict['fuzzy_outputs'] = st_list
    return render(request,'stored.html',context=st_dict)

def viewrules(request):
    vr_dict = {}
    rules = Rule.objects.all()
    vr_dict['rules'] = rules
    return render(request,'viewrules.html',context=vr_dict)

def feedrules(request):

    rl_dict = {}

    form = forms.FormRules(request.POST)

    temperature = None
    humidity = None
    power = None

    if form.is_valid():

        temperature = form.cleaned_data['temperature']
        humidity = form.cleaned_data['humidity']
        power = form.cleaned_data['power']

        print('temp : ' , temperature)
        print('humidity : ', humidity)
        print('power : ',power)

        if Rule.objects.filter(temperature = temperature , humidity = humidity):
            print('Alread Present')
            rl_dict['stored'] = 'Already Present'
        else:
            
            rl_instance = Rule()
            rl_instance.temperature = temperature
            rl_instance.humidity = humidity
            rl_instance.power = power
            rl_instance.save()

            print('Stored')

            rl_dict['stored'] = 'Rule Stored'
    else:
        print('form not valid')
        rl_dict['stored'] = 'Not Stored'

    return render(request,'feedrules.html',context=rl_dict)

def deleterule(request):
    dl_dict = {}

    form = forms.FormDel(request.POST)

    temperature = None
    humidity = None

    if form.is_valid():

        temperature = form.cleaned_data['temperature']
        humidity = form.cleaned_data['humidity']

        print('temp : ' , temperature)
        print('humidity : ', humidity)

        if not Rule.objects.filter(temperature = temperature , humidity = humidity):
            print('Rule not Present')
            dl_dict['deleted'] = 'Rule not Present'
        else:
            
            dl = Rule.objects.get(temperature = temperature , humidity = humidity)
            dl.delete()
            print('deleted')

            dl_dict['deleted'] = 'Rule Deleted'
    else:
        print('form not valid del rule')
        dl_dict['stored'] = 'Not Delete'

    return render(request,'deleterule.html',context=dl_dict)

def populate(request):
    pl_dict = {}

    pl_dict['done'] = False

    Rule.objects.all().delete()
    print('All rules flushed')

    rule_map = {
        ('VC', 'VD'): 'H',
        ('VC', 'D'): 'H',
        ('VC', 'N'): 'VH',
        ('VC', 'W'): 'VH',
        ('VC', 'VW'): 'VH',
        ('C', 'VD'): 'N',
        ('C', 'D'): 'H',
        ('C', 'N'): 'H',
        ('C', 'W'): 'VH',
        ('C', 'VW'): 'VH',
        ('W', 'VD'): 'VL',
        ('W', 'D'): 'VL',
        ('W', 'N'): 'VL',
        ('W', 'W'): 'L',
        ('W', 'VW'): 'N',
        ('H', 'VD'): 'N',
        ('H', 'D'): 'N',
        ('H', 'N'): 'H',
        ('H', 'W'): 'H',
        ('H', 'VW'): 'VH',
        ('VH', 'VD'): 'L',
        ('VH', 'D'): 'N',
        ('VH', 'N'): 'H',
        ('VH', 'W'): 'VH',
        ('VH', 'VW'): 'VH',
    }
    c = 0
    print("Keys")
    for k in rule_map.keys():
        c+=1
        t = k[0]
        h = k[1]
        p = rule_map.get(k)
        try:
            if not Rule.objects.filter(temperature = t , humidity = h):
                temp = Rule()
                temp.temperature = t
                temp.humidity = h   
                temp.power = p  
                temp.save()
            else:
                print('Already Present')
        except:
            print('Error')
            continue
    print("Num rules : " , c)
    pl_dict['done'] = True
    return render(request,'populate.html',context=pl_dict)