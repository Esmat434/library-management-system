from django.shortcuts import render,redirect
from django.views import View

from accounts.models import (
    CustomUser
)

from dashboard.mixins import (
    LoginRequiredMixin,RoleCheckMixin
)

from books.models import (
    Book,BookCopy,BorrowTransaction,Reservation
)

class DashboardView(LoginRequiredMixin,RoleCheckMixin,View):
    def get(self,request):
        books = Book.objects.count()
        copies = BookCopy.objects.count()
        total_books = books+copies
        total_borrows = BorrowTransaction.objects.count()
        total_reserve = Reservation.objects.count()
        borrows = BorrowTransaction.objects.all()
        total_users = CustomUser.objects.count()
        return render(request,'dashboard/dashboard.html',{'total_users':total_users,'total_books':total_books,'total_borrows':total_borrows,'total_reserve':total_reserve,'borrows':borrows})
    