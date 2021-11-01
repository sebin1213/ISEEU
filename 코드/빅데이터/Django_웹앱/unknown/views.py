from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Max, F
from .models import record
from django.utils import timezone
from .forms import UnknownForm, NicknameForm
from django.core.paginator import Paginator
from django.contrib import messages

from .models import record
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.generic import View
from django.shortcuts import render
from django.db.models import Count, Max, DateTimeField, ExpressionWrapper, F, TimeField, IntegerField, Case, When, Q
from django.db.models.functions import TruncHour, ExtractHour, Trunc

from time import mktime, strptime
from datetime import datetime, timezone
import datetime
from django.db.models.functions import TruncDay

from datetime import timedelta
# Create your views here.


# dt = datetime.datetime.now()
# # date_format = "%Y-%m-%d"
# date_format = "%H"
#
# months_ago = dt - datetime.timedelta(days=30)
# now_date = dt + datetime.timedelta(days=1)
# str_date_list = []
# while months_ago.strftime(date_format) != now_date.strftime(date_format):
#     tt = str(months_ago)[:13]
#     time_tuple = strptime(tt, date_format)
#     utc_now = mktime(time_tuple) * 1000
#     str_date_list.append([utc_now, 0])
#     months_ago += datetime.timedelta(days=1)
#
# # stocks = record.objects.all().filter(name="unknown").filter(id=1).annotate(month=TruncDay('time')).values(
# #     'month').annotate(c=Count('id')).order_by('month')
# stocks = record.objects.all().filter(name="unknown").filter(id=1).annotate(hour=ExtractHour('time')).values(
#     'hour').annotate(c=Count('id')).order_by('hour')
#
# close_list=[]
# for stock in stocks:
#     tt = str(stock['hour'])[:13]
#     time_tuple = strptime(tt, date_format)
#     utc_now = mktime(time_tuple) * 1000
#     close_list.append([utc_now, stock['c']])
#     if [utc_now, 0] in str_date_list:
#         str_date_list[str_date_list.index([utc_now, 0])][1] = stock['c']
#         str_date_list[str_date_list.index([utc_now, stock['c']])][0] = utc_now
#
# data = {
#             'close': str_date_list
#         }
# print(data)












import datetime

def index1(request):
    """     combot 목록 출력
    """
    date_format = "%Y-%m-%d"
    dt = datetime.datetime.now()
    months_ago = (dt - datetime.timedelta(days=30)).strftime(date_format)
    now_date = (dt + datetime.timedelta(days=1)).strftime(date_format)

    # 입력 파라미터 설정
    page = request.GET.get('page','1') # http://서버주소/combot 으로 접근시 출력할 페이지를 1번 페이지로 설정
    record_list = record.objects.filter(name="unknown").filter(nickname="default")
    Unknown_list = record_list.filter(time__range=[months_ago, now_date]).values("id").annotate(unknown_count=Count("id")).annotate(unknown_max=Max("time")).order_by('-unknown_count').annotate(url=Max("url"))

    # 페이징 처리
    paginator = Paginator(Unknown_list,7) # 한 페이지의 출력 개수 설정
    page_obj = paginator.get_page(page)
    # context = {'question_list':question_list} # 모든 질문 전부 출력
    context = {'Unknown_list': page_obj} # 7개의 질문만 출력
    return render(request, 'unknown/unknown_list.html', context)

def index2(request):
    """     combot 목록 출력
    """
    date_format = "%Y-%m-%d"
    dt = datetime.datetime.now()
    week_ago = (dt - datetime.timedelta(days=7)).strftime(date_format)
    now_date = (dt + datetime.timedelta(days=1)).strftime(date_format)

    page = request.GET.get('page','1') # http://서버주소/combot 으로 접근시 출력할 페이지를 1번 페이지로 설정

    Unknown_week_list = record.objects.filter(name="unknown").filter(nickname="default").filter(time__range=[week_ago, now_date]).values("id").annotate(unknown_count=Count("id")).annotate(unknown_max=Max("time")).annotate(url=Max("url")).order_by('-unknown_count')

    # 페이징 처리
    paginator = Paginator(Unknown_week_list,7) # 한 페이지의 출력 개수 설정
    page_obj = paginator.get_page(page)
    context = {'Unknown_list': page_obj} # 7개의 질문만 출력
    return render(request, 'unknown/unknown_week_list.html', context)

def index3(request):
    """     combot 목록 출력
    """
    date_format = "%Y-%m-%d"
    dt = datetime.datetime.now()
    now_date = (dt + datetime.timedelta(days=1)).strftime(date_format)
    today = dt.strftime(date_format)

    # 입력 파라미터 설정
    page = request.GET.get('page','1') # http://서버주소/combot 으로 접근시 출력할 페이지를 1번 페이지로 설정

    Unknown_day_list = record.objects.filter(name="unknown").filter(nickname="default").filter(time__range=[today, now_date]).values("id").annotate(unknown_count=Count("id")).annotate(unknown_max=Max("time")).annotate(url=Max("url")).order_by('-unknown_count')

    # 페이징 처리
    paginator = Paginator(Unknown_day_list,7) # 한 페이지의 출력 개수 설정
    page_obj = paginator.get_page(page)
    # context = {'question_list':question_list} # 모든 질문 전부 출력
    context = {'Unknown_list': page_obj} # 7개의 질문만 출력
    return render(request, 'unknown/unknown_day_list.html', context)

def Nickname(request,unknown_id):
    forms = record.objects.filter(name="unknown").filter(nickname="default").filter(id=unknown_id)

    for Unknown in forms:
        Unknown.nickname = request.POST['nickname']
        Unknown.save()
    return redirect('unknown:index1')


######################################################################################################


from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.generic import View
from django.shortcuts import render


class ResultAPIView(APIView,):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        data = request.session.get('result')
        return Response(data)





class monthlistAPIView(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request, unknown_id, *args, **kwargs):
        dt = datetime.datetime.now()
        date_format = "%Y-%m-%d"

        print(unknown_id)

        months_ago = dt - datetime.timedelta(days=30)
        now_date = dt + datetime.timedelta(days=1)
        str_date_list = []
        while months_ago.strftime(date_format) != now_date.strftime(date_format):
            tt = str(months_ago)[:10]
            time_tuple = strptime(tt, date_format)
            utc_now = mktime(time_tuple) * 1000
            str_date_list.append([utc_now, 0])
            months_ago += datetime.timedelta(days=1)

        stocks = record.objects.all().filter(name="unknown").filter(id=unknown_id).annotate(month=TruncDay('time')).values(
            'month').annotate(c=Count('id')).order_by('month')

        close_list = []
        for stock in stocks:
            tt = str(stock['month'])[:10]
            time_tuple = strptime(tt, date_format)
            utc_now = mktime(time_tuple) * 1000
            close_list.append([utc_now, stock['c']])
            if [utc_now, 0] in str_date_list:
                str_date_list[str_date_list.index([utc_now, 0])][1] = stock['c']
        data = {
            'close': str_date_list
        }
        return Response(data)



class weekAPIView(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request, unknown_id, *args, **kwargs):
        dt = datetime.datetime.now()
        date_format = "%Y-%m-%d"

        print(unknown_id)
        print('아이디 접근')

        months_ago = dt - datetime.timedelta(days=7)
        now_date = dt + datetime.timedelta(days=1)
        str_date_list = []
        while months_ago.strftime(date_format) != now_date.strftime(date_format):
            tt = str(months_ago)[:10]
            time_tuple = strptime(tt, date_format)
            utc_now = mktime(time_tuple) * 1000
            str_date_list.append([utc_now, 0])
            months_ago += datetime.timedelta(days=1)

        stocks = record.objects.all().filter(name="unknown").filter(id=unknown_id).annotate(month=TruncDay('time')).values(
            'month').annotate(c=Count('id')).order_by('month')

        close_list = []
        for stock in stocks:
            tt = str(stock['month'])[:10]
            time_tuple = strptime(tt, date_format)
            utc_now = mktime(time_tuple) * 1000
            close_list.append([utc_now, stock['c']])
            if [utc_now, 0] in str_date_list:
                str_date_list[str_date_list.index([utc_now, 0])][1] = stock['c']
        data = {
            'close': str_date_list
        }
        return Response(data)




class dayAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, unknown_id, *args, **kwargs):
        dt = datetime.datetime.now()
        date_format = "%Y-%m-%d"

        print(unknown_id)
        print('아이디 접근')

        months_ago = dt - datetime.timedelta(days=1)
        now_date = dt + datetime.timedelta(days=1)
        str_date_list = []
        while months_ago.strftime(date_format) != now_date.strftime(date_format):
            tt = str(months_ago)[:10]
            time_tuple = strptime(tt, date_format)
            utc_now = mktime(time_tuple) * 1000
            str_date_list.append([utc_now, 0])
            months_ago += datetime.timedelta(days=1)

        stocks = record.objects.all().filter(name="unknown").filter(id=unknown_id).annotate(month=TruncDay('time')).values(
            'month').annotate(c=Count('id')).order_by('month')

        close_list = []
        for stock in stocks:
            tt = str(stock['month'])[:10]
            time_tuple = strptime(tt, date_format)
            utc_now = mktime(time_tuple) * 1000
            close_list.append([utc_now, stock['c']])
            if [utc_now, 0] in str_date_list:
                str_date_list[str_date_list.index([utc_now, 0])][1] = stock['c']
        data = {
            'close': str_date_list
        }
        return Response(data)




    ############################################################################

class chartmonthAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, unknown_id, *args, **kwargs):
        date_format = "%Y-%m-%d"
        dt = datetime.datetime.now()
        today = dt.strftime(date_format)
        week_ago = (dt - timedelta(days=7)).strftime(date_format)
        months_ago = (dt - datetime.timedelta(days=30)).strftime(date_format)
        now_date = (dt + datetime.timedelta(days=1)).strftime(date_format)

        c = record.objects.filter(time__range=[months_ago, now_date]).filter(name="unknown", id=unknown_id).annotate(hour=ExtractHour('time')).values('hour').order_by('hour').annotate(month_count=Count('hour'))
        c_w = record.objects.filter(time__range=[week_ago, now_date]).filter(name="unknown", id=unknown_id).annotate(hour=ExtractHour('time')).values('hour').order_by('hour').annotate(month_count=Count('hour'))
        c_d = record.objects.filter(time__range=[today, now_date]).filter(name="unknown", id=unknown_id).annotate(hour=ExtractHour('time')).values('hour').order_by('hour').annotate(month_count=Count('hour'))

        time_all = [[1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0], [8, 0], [9, 0], [10, 0],[11, 0], [12, 0], [13, 0], [14, 0], [15, 0], [16, 0], [17, 0], [18, 0], [19, 0],[20, 0], [21, 0], [22, 0], [23, 0], [24, 0]]
        time_all_w = [[1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0], [8, 0], [9, 0], [10, 0], [11, 0], [12, 0],
                    [13, 0], [14, 0], [15, 0], [16, 0], [17, 0], [18, 0], [19, 0], [20, 0], [21, 0], [22, 0], [23, 0],
                    [24, 0]]
        time_all_d = [[1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0], [8, 0], [9, 0], [10, 0], [11, 0], [12, 0],
                    [13, 0], [14, 0], [15, 0], [16, 0], [17, 0], [18, 0], [19, 0], [20, 0], [21, 0], [22, 0], [23, 0],
                    [24, 0]]

        time_list = []
        time_list_w = []
        time_list_d = []
        for stock in c:
            tt = stock['hour']
            time_list.append([tt, stock['month_count']])
            if [tt, 0] in time_all:
                time_all[time_all.index([tt, 0])][1] = stock['month_count']

        for stock in c_w:
            tt = stock['hour']
            time_list_w.append([tt, stock['month_count']])
            if [tt, 0] in time_all_w:
                time_all_w[time_all_w.index([tt, 0])][1] = stock['month_count']

        for stock in c_d:
            tt = stock['hour']
            time_list_d.append([tt, stock['month_count']])
            if [tt, 0] in time_all_d:
                time_all_d[time_all_d.index([tt, 0])][1] = stock['month_count']

        data = {
            'count_month': time_all,
            'count_week': time_all_w,
            'count_day': time_all_d
        }
        return Response(data)
