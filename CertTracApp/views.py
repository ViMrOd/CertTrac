from django.shortcuts import render, get_object_or_404, redirect
from django.forms import modelformset_factory
from .models import Tutor, Takes, Subtopic, Session
from .forms import TutorForm, TutorLevelForm, TakesForm, SessionForm, \
    AddSessionForm, AddTutorForm, SearchTutors, AddLoggedHours

from datetime import datetime

from utils import get_tutor_id, get_course_id, count_courses
from update_hours import add_hours


def render_team_meetings(request):
    form = AddSessionForm()

    SessionFormSet = modelformset_factory(
        Session, SessionForm, 
        extra = 0, 
        can_delete = True
    )
    queryset = Session.objects.all().order_by('-id')
    initial = [{'subtopic': session.subtopic.name} for session in queryset]
    formset = SessionFormSet(queryset = queryset, initial = initial)

    context = {'formset': formset, 'form' : form}
    return render(request, 'session.html', context)


def add_subtopic_session(request):
    if request.method == 'POST':
        form = AddSessionForm(request.POST)
        if form.is_valid():
            subtopic = form.cleaned_data['subtopic']
            semester = form.cleaned_data['semester']
            in_person_hours = form.cleaned_data['in_person_hours']
            async_hours = form.cleaned_data['async_hours']

            Session.objects.create(
                subtopic = subtopic,
                semester = semester,
                in_person_hours = in_person_hours,
                async_hours = async_hours
            )
        else:
            print(form.errors)
    
    return redirect('team_meetings')


def edit_subtopic_session(request):
    if request.method == 'POST':
        SessionFormSet = modelformset_factory(
            Session, 
            SessionForm, 
            extra = 0, 
            can_delete = True
        )
        formset = SessionFormSet(
            request.POST, 
            Session.objects.all().order_by('-id')
        )
        if formset.is_valid():
            formset.save()
        else:
            print(formset.errors)
            print(formset.non_form_errors())

    # Recalculate Possibly Changed Information #
    count_courses()
    #add_hours()

    return redirect('team_meetings')


def index(request):
    return render(request, 'help.html')


def add_tutor_session(request):
    if request.method == 'POST':
        names = request.POST.get('names')
        id = request.POST.get('ID')
        date = request.POST.get('date')

        names = names.splitlines(keepends = False)

        request.session['names'] = names

        #subtopic = Subtopic.objects.get(name = course)
        session = Session.objects.get(id = id)

        for name in names:
            tid = get_tutor_id(name)

            tutor = get_object_or_404(Tutor, id = tid)

            Takes.objects.create(
                tutor = tutor, 
                session = session, 
                date = date
            )

            if session.subtopic.name == 'Review of Level 1':
                tutor = Tutor.objects.filter(id = tid)
                tutor.update(review_level_1_completed = date)

            #add_hours(name, course, date, session.in_person_hours, session.async_hours)

        count_courses()

        return update_level_logic(request)

    return render(request, 'index.html')


def add_25_logged_hours(request):
    if request.method == 'POST':
        form = AddLoggedHours(request.POST)
        if form.is_valid:
            name = form.cleaned_data['name']
            date = form.changed_data['date']
        
            tid = get_tutor_id(name)
            tutor = get_object_or_404(Tutor, id = tid)


            request.session['names'] = [name]

            date = datetime.strptime(date, '%Y-%m-%d').date()

            if tutor.logged_25_hours_level_1 is None:
                Tutor.objects.filter(id = tid).update(logged_25_hours_level_1 = date)

            elif tutor.logged_25_hours_level_2 is None:
                Tutor.objects.filter(id  = tid).update(logged_25_hours_level_2 = date)

            else:
                #Print error
                pass
            
        return update_level_logic(request)

    form = AddLoggedHours()
    return render(request, '25.html', {'form' : form})
   

def addTutor(request):
    form_ = AddTutorForm()
    if request.method == 'POST':
        form = AddTutorForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            date_hired = form.cleaned_data['date_hired']
            email = form.cleaned_data['email']

            Tutor.objects.create(
                first_name = first_name,
                last_name = last_name,
                date_hired = date_hired,
                email = email
            )

    return render(request, 'addTutor.html', {'form' : form_})


def help(request):
    return render(request, 'help.html')


def search(request):
    query = request.GET.get('q', '')
    TakesFormSet = modelformset_factory(
        Takes, TakesForm, 
        extra = 0, 
        can_delete = True
    )
    if query:
        TakesFormSet = modelformset_factory(
            Takes, TakesForm, 
            extra = 0, 
            can_delete = True
        )
        tid = get_tutor_id(query)
        request.session['tid'] = tid

        tutor = Tutor.objects.get(id = tid)
        tutor_form = TutorForm(instance = tutor)
        formset = TakesFormSet(queryset = Takes.objects.filter(tutor_id = tid))
    else:
        tid = request.session['tid']
        tutor = Tutor.objects.get(id = tid)
        tutor_form = TutorForm(instance = tutor)
        formset = TakesFormSet(queryset = Takes.objects.filter(tutor_id = tid))

    return render(
        request, 'results.html', 
        {'tutor': tutor, 'tutor_form' : tutor_form, 'formset' : formset}
    )


def edit_tutor(request):
    tid = request.session['tid']
    # Retrieve the Tutor instance from the database
    tutor = get_object_or_404(Tutor, id = tid)

    # Check if the request method is POST (form submission)
    if request.method == 'POST':
        # Create a form instance with the submitted data and the instance of the Tutor
        form = TutorForm(request.POST, instance = tutor)
        if form.is_valid():
            # Save the form data to the database
            form.save()
        else:
            # Print form errors for debugging
            print(form.errors)
            print(form.non_field_errors())
    else:
        # If the request method is GET, create a form instance with the Tutor instance
        form = TutorForm(instance = tutor)

    # Render the template with the form
    count_courses()
    return redirect('search')


def edit_takes(request):
    tid = request.session['tid']
    takes = Takes.objects.filter(tutor_id = tid)
    TakesFormSet = modelformset_factory(Takes, TakesForm, extra = 0, can_delete = True)

    if request.method == 'POST':
        formset = TakesFormSet(request.POST, queryset = takes)
        if formset.is_valid():
            formset.save()
        else:
            # Print form errors for debugging
            print(formset.errors)
            print(formset.non_form_errors())
            pass
    else:
        return redirect('search')

    count_courses()
    #add_hours()

    return redirect('search')


def update_level_logic(request):
    conditions_met = False 

    names = request.session.get('names')
    request.session.pop('names')
    level_up = []
    shared = []
    for name in names:
        tid = get_tutor_id(name)
        tutor = get_object_or_404(Tutor, id = tid)

        if tutor.level == 0:
            conditions_met = (
                ((tutor.number_basic_courses_completed_level_1) +
                (tutor.number_communication_courses_completed_level_1) +
                (tutor.number_learningstudytechinque_courses_completed_level_1) +
                (tutor.number_ethicsequality_courses_completed_level_1) +
                (tutor.number_elective_courses_completed_level_1)) >= 10
                and (tutor.number_basic_courses_completed_level_1) >= 4
                and (tutor.number_communication_courses_completed_level_1) >= 2
                and (tutor.number_learningstudytechinque_courses_completed_level_1) >= 2
                and (tutor.number_ethicsequality_courses_completed_level_1) >= 1
                and (tutor.number_elective_courses_completed_level_1) >= 1
                and (tutor.level_1_hours_in_person) >= 5
                and (tutor.level_1_hours) >= 10
                and (tutor.logged_25_hours_level_1)
            )
        if tutor.level == 1:
            conditions_met = (
                (tutor.number_basic_courses_completed_level_2 +
                tutor.number_communication_courses_completed_level_2 +
                tutor.number_learningstudytechinque_courses_completed_level_2 +
                tutor.number_ethicsequality_courses_completed_level_2 +
                tutor.number_elective_courses_completed_level_2) >= 10
                and tutor.number_basic_courses_completed_level_2 >= 3
                and tutor.number_communication_courses_completed_level_2 >= 2
                and tutor.number_learningstudytechinque_courses_completed_level_2 >= 3
                and tutor.number_ethicsequality_courses_completed_level_2 >= 1
                and tutor.number_elective_courses_completed_level_2 >= 1
                and tutor.level_2_hours_in_person >= 5
                and tutor.level_2_hours >= 10
                and tutor.logged_25_hours_level_2
                and tutor.review_level_1_completed
            )

        if conditions_met:
            level_up.append(tutor)
            shared.append(tutor.id)

    if level_up:
        TutorLevelFormSet = modelformset_factory(Tutor, TutorLevelForm, extra = 0)
        tutors = Tutor.objects.filter(id__in = shared)
        formset = TutorLevelFormSet(queryset = tutors)
        request.session['id'] = shared
        #info = zip(level_up, formset)
        return render(request, 'update_level.html', {'formset' : formset})
    else:
        return render(request, 'index.html')


def update_level(request):
    TutorLevelFormSet = modelformset_factory(Tutor, TutorLevelForm, extra = 0)
    if request.method == 'POST':
        shared = request.session.get('id')
        tutors = Tutor.objects.filter(id__in = shared)
        request.session.pop('id')
        formset = TutorLevelFormSet(request.POST, queryset = tutors)

        if formset.is_valid():
            formset.save()
            print("SAVED")
        else:
            print(formset.errors)
            print(formset.non_form_errors())

        return render(request, 'index.html')
    return render(request, 'help.html')
