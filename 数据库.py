from django.shortcuts import render, redirect, HttpResponse
from webapi.models.car import car
from webapi.models.RegularUsers import regularuser
from webapi.models.userbuy import userbuy
from datetime import datetime
from collections import defaultdict
from webapi.models.price import price
from webapi.models.notice import notice
from webapi.models.things import things


def find(request):
    datas = car.objects.all()
    new_datas = defaultdict(set)
    for cho in datas:
        new_datas["types"].add(cho.types)
        new_datas["volume"].add(cho.volume)
        new_datas["car_road__begin"].add(cho.car_road.begin)
        new_datas["car_road__ends"].add(cho.car_road.ends)
        new_datas["car_road__begintime"].add(cho.car_road.begintime)
        new_datas["car_road__needtime"].add(cho.car_road.needtime)
        new_datas["car_price__money"].add(cho.car_price.money)
        new_datas["car_price__nums"].add(cho.car_price.nums)
    if request.method == "GET":
        return render(request, "../templates/shujuku/showdata.html", {"datas": new_datas, "showdatas": datas})
    res_types = request.POST.get("res_types")
    res_volume = request.POST.get("res_volume")
    res_car_road_begin = request.POST.get("res_car_road_begin")
    res_car_road_ends = request.POST.get("res_car_road_ends")
    res_car_road_begintime = request.POST.get("res_car_road_begintime")
    res_car_road_needtime = request.POST.get("res_car_road_needtime")
    res_car_price_money = request.POST.get("res_car_price_money")
    res_car_price_nums = request.POST.get("res_car_price_nums")
    if res_car_road_begintime is not None:
        res_car_road_begintime = datetime.strptime(res_car_road_begintime, "%Y年%m月%d日 %H:%M")
        res_car_road_begintime = res_car_road_begintime.strftime("%Y-%02m-%02d %02H:%02M")
    dnums = {"types": res_types, "volume": res_volume,
             "car_road__begin": res_car_road_begin,
             "car_road__ends": res_car_road_ends,
             "car_road__begintime": res_car_road_begintime,
             "car_road__needtime": res_car_road_needtime,
             "car_price__money": res_car_price_money,
             "car_price__nums": res_car_price_nums}
    print(res_car_road_begintime)
    show_data = datas.filter(**{k: v for k, v in dnums.items() if v is not None})
    for cho in new_datas:
        print(cho)
    # datas表示查询条件
    # show_data表示查询得到的所有数据
    # dnums用以锁定用户选中的条件
    return render(request, "../templates/shujuku/showdata.html",
                  {"datas": new_datas, "showdatas": show_data, "dnums": dnums})


def buys(request):
    res_car_id = request.POST.get("res_carid")
    # print(">>>", res_car_id)
    # print("name:", request.session.get("info"))
    user_buy_things = userbuy.objects.filter(userbuyname=request.session.get("info")["name"])[0]
    # print("u***************userthings", user_buy_things)
    now_count = user_buy_things.userbuycount
    if now_count == 3 or res_car_id is None:
        return render(request, "../templates/shujuku/buy_successful.html",
                      {"judge": "Fail", "things": "已到达最大上限额度/未选择汽车"})
    else:
        now_count += 1
        # print("res_priceid:", res_priceid)
        now_nums = price.objects.filter(car_price__carid=res_car_id)[0].nums
        # print(now_nums)
        xxx = price.objects.filter(car_price__carid=res_car_id)[0].nums
        if xxx == 0:
            return render(request, "../templates/shujuku/buy_successful.html", {"things": "失败"})
        price.objects.filter(car_price__carid=res_car_id).update(nums=now_nums - 1)
        if user_buy_things.first_userbuy_car is None:
            userbuy.objects.filter(userbuyname=request.session.get("info")["name"]).update(userbuycount=now_count,
                                                                                           first_userbuy_car=res_car_id)
        elif user_buy_things.second_userbuy_car is None:
            userbuy.objects.filter(userbuyname=request.session.get("info")["name"]).update(userbuycount=now_count,
                                                                                           second_userbuy_car=res_car_id)
        elif user_buy_things.third_userbuy_car is None:
            userbuy.objects.filter(userbuyname=request.session.get("info")["name"]).update(userbuycount=now_count,
                                                                                           third_userbuy_car=res_car_id)
        return render(request, "../templates/shujuku/buy_successful.html",
                      {"judge": "Successful", "things": "购买成功"})


def userthings(request):
    showdatas = userbuy.objects.filter(userbuyname=request.session.get("info")["name"])[0]
    print(showdatas)
    return render(request, "../templates/shujuku/userthings.html", {"showdatas": showdatas})


def deletecar(request):
    delete_car_id = request.POST.get("delete_carid")
    if delete_car_id is None:
        return render(request, "../templates/shujuku/delete_successful.html",
                      {"judge": "失败", "things": "无可删除信息"})
    delete_car_id = int(delete_car_id)
    # now_count=price.objects.filter()
    now_count = price.objects.filter(car_price__carid=delete_car_id)[0].nums
    print(now_count)
    price.objects.filter(car_price__carid=delete_car_id).update(nums=now_count + 1)
    if delete_car_id is not None:
        userthing = userbuy.objects.filter(userbuyname=request.session.get("info")["name"])[0]
        now_count = userthing.userbuycount - 1
        if userthing.first_userbuy_car is not None:
            if userthing.first_userbuy_car.carid == delete_car_id:
                userbuy.objects.filter(userbuyname=request.session.get("info")["name"]).update(
                    userbuycount=now_count, first_userbuy_car=None)
            else:
                if userthing.second_userbuy_car is not None:
                    if userthing.second_userbuy_car.carid == delete_car_id:
                        userbuy.objects.filter(userbuyname=request.session.get("info")["name"]).update(
                            userbuycount=now_count, second_userbuy_car=None)
                    else:
                        if userthing.third_userbuy_car is not None:
                            if userthing.third_userbuy_car.carid == delete_car_id:
                                userbuy.objects.filter(userbuyname=request.session.get("info")["name"]).update(
                                    userbuycount=now_count, third_userbuy_car=None)
                else:
                    if userthing.third_userbuy_car is not None:
                        if userthing.third_userbuy_car.carid == delete_car_id:
                            userbuy.objects.filter(userbuyname=request.session.get("info")["name"]).update(
                                userbuycount=now_count, third_userbuy_car=None)
        else:
            if userthing.second_userbuy_car is not None:
                if userthing.second_userbuy_car.carid == delete_car_id:
                    userbuy.objects.filter(userbuyname=request.session.get("info")["name"]).update(
                        userbuycount=now_count, second_userbuy_car=None)
                else:
                    if userthing.third_userbuy_car is not None:
                        userbuy.objects.filter(userbuyname=request.session.get("info")["name"]).update(
                            userbuycount=now_count, third_userbuy_car=None)
            else:
                if userthing.third_userbuy_car is not None:
                    userbuy.objects.filter(userbuyname=request.session.get("info")["name"]).update(
                        userbuycount=now_count, third_userbuy_car=None)
        return render(request, "../templates/shujuku/delete_successful.html",
                      {"judge": "Successful", "things": "删除成功"})
    else:
        return render(request, "../templates/shujuku/delete_successful.html", {"judge": "Fail", "things": "失败"})


# 公告
def noticepage(request):
    als = notice.objects.all()
    return render(request, "../templates/shujuku/notice.html", {"als": als})


# 信息介绍
def thingspage(request):
    if request.method == "GET":
        als = things.objects.all()
        return render(request, "../templates/shujuku/things.html", {"als": als})
    username = request.session["info"]["name"]
    things.objects.create(namethings=username, saythings=request.POST.get("saythings"))
    als = things.objects.all()
    return render(request, "../templates/shujuku/things.html", {"als": als})


# 日志文件
def logs(request):
    return render(request, "../templates/shujuku/logs.html")
