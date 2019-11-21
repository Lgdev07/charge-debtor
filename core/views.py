from django.shortcuts import render, get_object_or_404, redirect
from .models import Debtor
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from datetime import timezone
from .forms import DebtorUpdateForm

class DebtorsListView(LoginRequiredMixin, ListView):
    model = Debtor
    template_name = 'core/list.html'        # <app>/<model>_<viewtype>.html
    context_object_name = 'debtors'
    ordering = ['-due_date']
    paginate_by = 3

    def get_queryset(self):
        return Debtor.objects.filter(created_by=self.request.user.profile).order_by('-due_date')

class DebtorCreateView(CreateView):
    model = Debtor
    template_name = 'core/newdebtor.html' 
    fields = [
        'name',
        'email',
        'amount_owed',
        'due_date'
    ]

    def form_valid(self, form):
        form.instance.created_by = self.request.user.profile
        return super().form_valid(form)
   
class DebtorDetailView(DetailView):
    model = Debtor
    template_name = 'core/debtordetail.html' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["d_form"] = DebtorUpdateForm(instance=context['object'])
        return context
    
    # if request.method == 'POST':
    #     u_form = UserUpdateForm(request.POST, instance=request.user)
    #     p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
    #     if u_form.is_valid() and p_form.is_valid():
    #         u_form.save()
    #         p_form.save()
    #         messages.success(request, f'Account updated for {request.user.username}!')
    #         return redirect('profile')
    # else:
    #     u_form = UserUpdateForm(instance=request.user)
    #     p_form = ProfileUpdateForm(instance=request.user.profile)

    # context = {
    #     'u_form': u_form,
    #     'p_form': p_form,
    # }


def deletedebtor(request, id):
    debtor = get_object_or_404(Debtor, pk=id)
    messages.success(request, f'{debtor.name} Excluded with success.')
    debtor.delete()
    return redirect('/', {'messages': messages})
