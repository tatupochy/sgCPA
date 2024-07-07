from django.shortcuts import render

from payments.models import EnrollmentDetail, Fee
from constans.paymentStates import StateEnum
from students.models import Student

# Create your views here.

#Menu principal
def reports(request):
    return render(request, 'reports.html')


#Morosidad
def latePayments(request):
    students = Student.objects.all()
    studentsDebts = []
    for student in students:
        studentEnrollments = EnrollmentDetail.objects.filter(student=student)
        
        enrollmentsOverdueAmount = sum(
            enrollment.enrollment_amount for enrollment in studentEnrollments if enrollment.state.name == StateEnum.Vencido
        )
        
        studentFees = Fee.objects.filter(student=student)
        studentOverdueFees = sum(
            fee.fee_amount for fee in studentFees if fee.state.name == StateEnum.Vencido
        )
        
        totalDebt = enrollmentsOverdueAmount + studentOverdueFees

        studentDebts = {
            'totalDebt': totalDebt,
            'name': student.name,
            'ciNumber': student.ciNumber
        }

        if totalDebt > 0: 
            studentsDebts.append(studentDebts)
            
        studentsDebts_sorted = sorted(studentsDebts, key=lambda x: x['totalDebt'], reverse=True)
        
    return render(request, 'latePayments.html', {'studentsDebts': studentsDebts_sorted})