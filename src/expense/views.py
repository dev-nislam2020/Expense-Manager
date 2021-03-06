from datetime import date, timedelta

from django.core.paginator import Paginator
from django.db.models import Count, Sum
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.dates import (DayArchiveView, MonthArchiveView,
                                        WeekArchiveView)
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from expense.forms import (BudgetForm, CategoryForm, ExpenseForm,
                           ExpensePreviousForm)
from expense.models import Budget, Category, Expense


# Create your views here.
def report(expense_list):
    data = {}
    amount = expense_list.all().aggregate(Sum('amount'))['amount__sum']
    if amount is None:
        data['total_amount'] = 0
    else:
        data['total_amount'] = expense_list.all().aggregate(Sum('amount'))['amount__sum']
    data['trax'] = expense_list.count()
    return data

def get_day_expense(obj, today):
    expense_list = obj.filter(create_at__day=today.day)
    return report(expense_list)

def get_week_expense(obj, today):
    current_week = today.isocalendar()[1]
    expense_list = obj.filter(create_at__week=current_week)
    return report(expense_list)

def get_month_expense(obj, today):
    expense_list = obj.filter(create_at__month=today.month)
    return report(expense_list)
    
def get_expense_data(expense, today):
    data = {}
    data['day'] = get_day_expense(expense, today)
    data['week'] = get_week_expense(expense, today)
    data['month'] = get_month_expense(expense, today)
    return data


class HomeView(TemplateView):
    template_name = 'expense/home.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(HomeView, self).get_context_data(**kwargs)
        expense = Expense.objects.all()
        today = date.today()

        context['today'] = today
        context['reports'] = get_expense_data(expense, today)
        return context

class ExpenseCreateView(CreateView):
    form_class = ExpenseForm
    template_name = 'expense/create.html'
    success_url = reverse_lazy('expense-create')
    

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ExpenseCreateView, self).get_context_data(**kwargs)
        expense_list = Expense.objects.filter(create_at=date.today())
        paginator = Paginator(expense_list, 9)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        # Add in a QuerySet of all the books
        context['page_obj'] = page_obj
        context['page_name'] = "Add Expense"
        context['is_previose'] = True
        context['report'] = report(expense_list)
        context['is_expense'] = True
        return context
    
    def form_valid(self, form):
        if self.request.GET.get('pk'):
            self.category = get_object_or_404(Category, id=self.kwargs['pk'])
            form.instance.category = self.category

        form.instance.create_at = date.today()
        return super(ExpenseCreateView, self).form_valid(form)


class ExpensePreviousCreateView(CreateView):
    form_class = ExpensePreviousForm
    template_name = 'expense/create.html'
    success_url = reverse_lazy('expense-create')
    

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ExpensePreviousCreateView, self).get_context_data(**kwargs)
        expense_list = Expense.objects.filter(create_at=date.today())
        paginator = Paginator(expense_list, 9)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        # Add in a QuerySet of all the books
        context['page_obj'] = page_obj
        context['page_name'] = "Add Previouse Expense"
        context['report'] = report(expense_list)
        context['is_expense'] = True
        
        return context

    def form_valid(self, form):
        if self.request.GET.get('pk'):
            self.category = get_object_or_404(Category, id=self.kwargs['pk'])
            form.instance.category = self.category

        return super(ExpensePreviousCreateView, self).form_valid(form)


class ExpenseUpdateView(UpdateView):
    form_class = ExpenseForm
    template_name = 'expense/create.html'
    success_url = reverse_lazy('expense-create')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ExpenseUpdateView, self).get_context_data(**kwargs)
        expense_list = Expense.objects.filter(create_at=date.today())
        paginator = Paginator(expense_list, 9)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        # Add in a QuerySet of all the books
        context['page_obj'] = page_obj
        context['page_name'] = "Update Expense"
        context['report'] = report(expense_list)
        return context
    
    def get_queryset(self):
        return Expense.objects.all()
    
class ExpenseDeleteView(DeleteView):
    form_class = ExpenseForm
    template_name = 'expense/delete.html'
    success_url = reverse_lazy('expense-create')
    
    def get_queryset(self):
        return Expense.objects.all()

class CategoryCreateView(CreateView):
    form_class = CategoryForm
    template_name = 'expense/create.html'
    success_url = reverse_lazy('category-create')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CategoryCreateView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        category_list = Category.objects.all()
        paginator = Paginator(category_list, 9)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        # Add in a QuerySet of all the books
        context['page_obj'] = page_obj
        context['page_name'] = "Add Expense Category"
        context['is_category_expense'] = True
        return context

class CategoryUpdateView(UpdateView):
    form_class = CategoryForm
    template_name = 'expense/create.html'
    success_url = reverse_lazy('category-create')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CategoryUpdateView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        category_list = Category.objects.all()
        paginator = Paginator(category_list, 9)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        # Add in a QuerySet of all the books
        context['page_obj'] = page_obj
        context['page_name'] = "Update Expense Category"
        context['is_category_expense'] = True
        return context

    def get_queryset(self):
        return Category.objects.all()
    
class BudgetCreateView(CreateView):
    form_class = BudgetForm
    template_name = 'expense/create.html'
    success_url = reverse_lazy('budget-create')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(BudgetCreateView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        budget_list = Budget.objects.all()
        paginator = Paginator(budget_list, 9)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        # Add in a QuerySet of all the books
        context['page_obj'] = page_obj
        context['page_name'] = "Add Budget Expense"
        context['is_budget_expense'] = True
        return context

    def form_valid(self, form):
        day = form.cleaned_data['budget_for']
        form.instance.deadline = date.today() + timedelta(int(day))
        return super(BudgetCreateView, self).form_valid(form)


class BudgetUpdateView(UpdateView):
    form_class = BudgetForm
    template_name = 'expense/create.html'
    success_url = reverse_lazy('budget-create')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(BudgetUpdateView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        budget_list = Budget.objects.all()
        paginator = Paginator(budget_list, 9)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        # Add in a QuerySet of all the books
        context['page_obj'] = page_obj
        context['page_name'] = "Update Budget Expense"
        context['is_budget_expense'] = True
        return context

    def get_queryset(self):
        return Budget.objects.all()

class TodayView(DayArchiveView):
    queryset = Expense.objects.all()
    date_field = "create_at"
    allow_future = True
    template_name = 'expense/report.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(TodayView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        expense = context['object_list']
        context['report'] = report(expense)
        context['page_name'] = "Today Expense"
        context['is_day'] = True
        return context

class WeekView(WeekArchiveView):
    queryset = Expense.objects.all()
    date_field = "create_at"
    template_name = 'expense/report.html'
    week_format = "%W"
    allow_future = True

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(WeekView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        expense = context['object_list']
        context['report'] = report(expense)
        context['page_name'] = "Week Expense"
        context['is_week'] = True
        return context

class MonthView(MonthArchiveView):
    queryset = Expense.objects.all()
    date_field = "create_at"
    template_name = 'expense/report.html'
    allow_future = True

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(MonthView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        expense = context['object_list']
        context['report'] = report(expense)
        context['page_name'] = "Month Expense"
        context['is_month'] = True
        return context
