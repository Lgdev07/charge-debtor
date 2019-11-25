import smtplib, ssl
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Debtor
from .forms import DebtorUpdateForm
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class DebtorsListView(LoginRequiredMixin, ListView):
    model = Debtor
    template_name = 'core/list.html'        # <app>/<model>_<viewtype>.html
    context_object_name = 'debtors'
    ordering = ['-due_date']
    paginate_by = 3

    def get_queryset(self):
        query = Debtor.objects.filter(created_by=self.request.user.profile)
        
        if self.request.GET.get('search'):
            return query.filter(name__icontains=self.request.GET.get('search'))
        elif self.request.GET.get('paid'):
            return Debtor.objects.filter(is_paid=True)

        return query.filter(is_paid=False)

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
   
class DebtorDetailView(UpdateView):
    model = Debtor
    template_name = 'core/debtordetail.html' 
    form_class = DebtorUpdateForm

def deletedebtor(request, id):
    """Function that deletes the selected object.
    
    Arguments:
        request {get} -- HTTP method GET
        id {int} -- Id of the object Debtor
    
    Returns:
        redirect -- Redirect to home page
    """
    debtor = get_object_or_404(Debtor, pk=id)
    messages.success(request, f'{debtor.name} Excluded with success.')
    debtor.delete()
    return redirect('/', {'messages': messages})

def action_sendmail(request, id):
    """Function responsible for filtering the request and
    calling the email sending.
    
    Arguments:
        request {get} -- HTTP method GET
        id {int} -- Id of the object Debtor
    
    Returns:
        func sendmail -- call the function with args
    """
    debtor = get_object_or_404(Debtor, pk=id)
    profile_mail = request.user.profile.email
    profile_password = request.user.profile.password
    return sendmail(request, profile_mail, debtor, profile_password)

def sendmail(request, sender_email, debtor, password):
    """Function responsible for send the email with the
    SMTP method only for gmail accounts.
    
    Arguments:
        request {get} -- HTTP method GET
        sender_email {str} -- Profile email
        debtor {obj} -- object Debtor
        password {str} -- Profile password
    
    Returns:
        redirect -- Redirect to home page
    """
    try:
        receiver_email = debtor.email
        message = MIMEMultipart("alternative")
        message["Subject"] = "Please read the message"
        message["From"] = sender_email
        message["To"] = receiver_email

        # Create the plain-text and HTML version of your message
        text = f"""\
        Dear {debtor.name},
        You owe me {debtor.amount_owed} reais,
        Due Date: {debtor.due_date} 
        I'm waiting,
        {request.user.username}
        """
        html = f"""\
        <html>
        <body>
            <p>Dear {debtor.name},<br>
            You owe me {debtor.amount_owed} reais,<br>
            Due Date: {debtor.due_date}<br>
            I'm waiting,<br>
            {request.user.username}
            </p>
        </body>
        </html>
        """

        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        message.attach(part1)
        message.attach(part2)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )
        debtor.last_email_sent = timezone.now()
        debtor.save()
        messages.success(request, f'Message send with success.')
        return redirect('/', {'messages': messages})

    except Exception as e:
        messages.error(request, f'Message failed, error: {e}.')
        return redirect('/', {'messages': messages})