from django.shortcuts import render

from payments.models import EnrollmentDetail, Fee
from constans.paymentStates import StateEnum
from students.models import Course, Student
from django.db.models import Count

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
            enrollment.enrollment_amount for enrollment in studentEnrollments if enrollment.state.name == StateEnum.Vencido.value
        )
        
        studentFees = Fee.objects.filter(student=student)
                
        studentOverdueFees = sum(
            fee.fee_amount for fee in studentFees if fee.state.name == StateEnum.Vencido.value
        )

        print(studentOverdueFees)
        
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


def coursesRanking(request):

    courses_with_enrollment_counts = Course.objects.annotate(num_enrollment_details=Count('enrollment__enrollmentdetail')).order_by('-num_enrollment_details')

    courses_list = []
    for course in courses_with_enrollment_counts:
        courses_list.append({
            'course_name': course.name,
            'num_enrollment_details': course.num_enrollment_details,
        })


    return render(request, 'coursesRanking.html', {'courses_list': courses_list})
