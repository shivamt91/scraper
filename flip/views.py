from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from . tasks import start_crawl
from time import sleep
import json
from celery.result import AsyncResult
from rest_framework import viewsets
from . models import Data
from . serializers import DataSerializer


class HomePageView(APIView):
    def get(self, request):
        return HttpResponse("This is a simple Scraper API!")


class CrawlView(APIView):
    def post(self, request):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        urls = json.loads(body['urls'])
        task_result = start_crawl.apply_async(args=[urls, ])
        sleep(3)
        return JsonResponse({"id": task_result.id})


class StatusView(APIView):
    def get(self, request):
        task_id = request.GET.get('id')
        task = AsyncResult(task_id)
        if task.ready():
            context = {"state": task.state, }
        else:
            context = {
                "info": task.info,
                "state": task.state,
            }
        return JsonResponse(context)


class DataViewSet(viewsets.ModelViewSet):
    queryset = Data.objects.all()
    serializer_class = DataSerializer


class RequiredData(APIView):
    def post(self, request):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        my_price = int(body['price'])
        distance = 10
        my_list = []
        for data in Data.objects.all():
            item = dict({
                "id": data.id,
                "name": data.name,
                "url": data.url,
                "price": data.price,
            })
            my_list.append(item)

        sorted_list = sorted(my_list, key=lambda k: k['price'])
        sorted_prices = [i['price'] for i in sorted_list]

        dist = distance//2
        products = []
        if len(sorted_list) == len(sorted_prices):
            left = 0
            right = 0
            mid = self.search(sorted_prices, 0, len(sorted_prices)-1, my_price)
            list_len = len(sorted_list)
            if mid - dist >= 0 and mid + dist < list_len:
                left = mid - dist
                right = mid + dist
            elif mid - dist < 0:
                left = 0
                right = (2 * dist)
            elif mid + dist >= list_len:
                left = list_len - (2 * dist) - 1
                right = list_len - 1

            if left or right:
                for i in range(left, right+1):
                    if i == mid:
                        continue
                    products.append(sorted_list[i])
        return JsonResponse({"The following 10 products have prices close to the given price": products})

    def search(self, arr, l, r, x):
        mid = 0
        while l <= r:
            mid = l + (r - l) // 2
            if arr[mid] == x:
                return mid
            elif arr[mid] < x:
                l = mid + 1
            else:
                r = mid - 1
        return mid
