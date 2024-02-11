from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import generic
from django.views.generic.edit import DeleteView

from .forms import NewQuestionForm, QuestionForm, ChoiceForm
from .models import Question, Choice
from django.template import loader
from django.shortcuts import render, get_object_or_404

# Create your views here.
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"
    def get_queryset(self):
        return Question.objects.filter(productiondate__lte=timezone.now(),pk__in=[x.question.pk for x in Choice.objects.all()]).order_by("-productiondate")[:10]

class QuestionDetailView(generic.DetailView):
    model = Question
    template_name = "polls/details.html"
    def get_queryset(self):
        return Question.objects.filter(productiondate__lte=timezone.now(),pk__in=[x.question.pk for x in Choice.objects.all()])
class QuestionDelete(DeleteView):
    model = Question
    success_url = reverse_lazy('polls:index')

def detail(request, question_id):
    q=get_object_or_404(Question, pk=question_id)

    if q.productiondate>timezone.now() :
        raise Http404("Question is not published")
    if q.choice_set.count() == 0:
        raise Http404("No choices for this question")
    context = {"question":q, "question_id":question_id}
    return render(request, "polls/details.html", context)
def results(request, question_id):
    q=get_object_or_404(Question, pk=question_id)
    if (q.productiondate > timezone.now()):
        raise Http404("Question is not published")
    if q.choice_set.count() == 0:
        raise Http404("No choices for this question")
    context={"question":q}
    return render(request, "polls/results.html", context)
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

@login_required()
@permission_required("polls.can_nullify")
def nullask(request, question_id):
    question=get_object_or_404(Question, pk = question_id)
    if request.method == "GET":
        return render(request, "polls/nullifyask.html", {"question":question})
    else:
        for i in question.choice_set.all():
            i.votes = 0
            i.save()
        return HttpResponseRedirect(reverse("polls:index"))
def create_new_question(request):
    if request.method == "POST":
        form = NewQuestionForm(request.POST)
        if form.is_valid():
           q = Question.objects.create(text=form.cleaned_data['question_text'], productiondate=form.cleaned_data['pub_date'])
           q.save()
           return HttpResponseRedirect(reverse("polls:index"))
    else:
        form= NewQuestionForm()
    context={
        'form':form
    }
    return render(request, 'polls/create_new_question.html', context)
def create_question_with_choices(request):
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)

        extra_choices = int(request.POST.get('extra_choices', 0))
        if question_form.is_valid():
            question = question_form.save()
            for i in range(1,extra_choices+1):
                choice_text = request.POST.get(f'choice_text_{i}')
                if choice_text:
                    choice = Choice(question=question, choice_text=choice_text)
                    choice.save()

            return HttpResponseRedirect(reverse('polls:index')) # Redirect to a success page
    else:
        question_form = QuestionForm()
    return render(request, 'polls/create_question_with_choices.html', {'question_form': question_form, 'list':[1,2,3]})
#here is vscode.....and here is github....branch Feature_C


#changes text commit 111