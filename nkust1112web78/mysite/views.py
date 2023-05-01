from django.shortcuts import render   # 渲染網頁
from django.http import HttpResponse   # Django用來回應給瀏覽器特定資料的函式
import requests   # 匯入擷取網頁所需要的模組
import json       # 匯入操作JSON格式所需要的模組
from mysite import models  # 從 mysite 的資料夾中的 models.py 匯入所有的類別（資料表）
import random     # 匯入隨機模組

def index(request):
    mynames = ["高雄張景嵐", "楠梓張景嵐", "南台灣陶淵明", "高科張景嵐"]
    myname = random.choice(mynames)
    return render(request, "index.html", locals())

def all_data(request):
    url = "https://opendata.hccg.gov.tw/OpenDataFileHit.ashx?ID=48DEDBDAC3A31FC6&u=77DFE16E459DFCE3F5CEA2F931E333F7E23D5729EF83D5F20744125E844FB27044F9892E6F09372518441B3BB84260426ADE242A57DFB9E8C9A50C50134F4F47"
    r = requests.get(url)
    data = json.loads(r.text)
    msg = ""
    msg = "<h2>" + data["updated_at"] + "</h2><br>"
    bicycle_data = data["retVal"]
    msg = msg + "<table><tr><td>站名</td><td>自行車數量</td></tr>"
    for item in bicycle_data:
        msg = msg + "<tr bgcolor=#ccffcc><td>{}</td><td>{}/{}</td></tr>".format(
            item['sna'].split("_")[1], 
            item['sbi'], 
            item['tot'])
    msg = msg + "</table>"
    return HttpResponse(msg)

def filtered_data(request):
    # 先刪除所有的舊資料
    models.HBicycleData.objects.all().delete()
    # 先把所有的資料放到資料庫中，比照all_data()中的程式碼
    url = "https://opendata.hccg.gov.tw/OpenDataFileHit.ashx?ID=48DEDBDAC3A31FC6&u=77DFE16E459DFCE3F5CEA2F931E333F7E23D5729EF83D5F20744125E844FB27044F9892E6F09372518441B3BB84260426ADE242A57DFB9E8C9A50C50134F4F47"
    r = requests.get(url)
    data = json.loads(r.text)
    bicycle_data = data["retVal"]
    for item in bicycle_data:
        new_record = models.HBicycleData(
            sna = item['sna'].split("_")[1],
            sbi = int(item['sbi']),
            tot = int(item['tot']))
        new_record.save()
    # 從資料表裡面過濾出我們想要的資料
    data = models.HBicycleData.objects.filter(sbi__gte=10)
    return render(request, "filter.html", locals())

def nkustnews(request):
    data = models.NKUSTnews.objects.all()
    return render(request, "nkustnews.html", locals())

def phonelist(request, id=-1):
    if id==-1:
        data = models.PhoneModel.objects.all()
    else:
        maker = models.PhoneMaker.objects.get(id=id)         #找一個用get
        data = models.PhoneModel.objects.filter(maker=maker) #找好多個，用filter
    return render(request, "phonelist.html", locals())

def chart(request):
    data = models.PhoneModel.objects.all()
    return render(request, "chart.html", locals())