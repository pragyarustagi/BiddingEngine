from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from Items.serializers import ItemSerializer,BidOnItemSerializer
from Items.models import item,bidOnItem

################ further improvments ##################
#
#
#   * add pagination in top bidders retrieval
#
#######################################################




# Create your views here.

class ItemCreate(viewsets.ViewSet):
    '''
    creates the item
    '''

    permission_classes = (permissions.IsAuthenticated,)

    def post(self,request, format='json'):
        serializer = ItemSerializer(data=request.data,)

        if serializer.is_valid():
            _item = serializer.save()

            if _item:
                return Response(serializer.data,
                                status = status.HTTP_201_CREATED)

        return Response(serializer.errors,
                        status = status.HTTP_400_BAD_REQUEST)

    def get(self,request,itemid):

        product_name = request.query_params.get('product_name', None)
        pk = request.query_params.get('itemid', None) or itemid

        if product_name:
            product = item.objects.get(username=product_name)
            pass

        elif pk:
            product = item.objects.get(pk=pk)
            pass

        else:
            return Response({'data-missing':'both product_name and itemid missing'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = ItemSerializer(product)

        return Response(serializer.data,
                        status=status.HTTP_200_OK)

    def get_all(self,request):
        items = item.objects.all()
        serializer = ItemSerializer(items,
                                    many= True)

        return Response(data=serializer.data,
                        status=status.HTTP_200_OK)

class bidOnItemView(viewsets.ViewSet):
    '''
    creates the bidOnItem
    '''

    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request):

        bidOnItems = bidOnItem.objects.all()
        serializer = BidOnItemSerializer(bidOnItems,many=True)

        return Response(serializer.data,
                        status=status.HTTP_200_OK)

    def get_itemid(self,request):

        pk = request.query_params.get('itemid',None)

        if pk:
            bidonitem = bidOnItem.objects.get(pk = pk)
        else:
            return Response(data = {'data-missing':'itemid missing'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = BidOnItemSerializer(bidOnItem,)

        return Response(serializer.data,
                        status = status.HTTP_200_OK)

    def get_topbidders(self,request,itemid):

        limit = request.query_params.get('limit',5)
        itemid = request.query_params.get('itemid', None) or itemid

        if item:
            bidonitems = bidOnItem.objects.filter(item=itemid).order_by('-amount')[:limit]
        else:
            return Response(data={'data-missing':'itemid missing'},
                            status=status.HTTP_400_BAD_REQUEST)

        from collections import OrderedDict
        data = OrderedDict()

        for bidonitem in bidonitems:
            user = bidonitem.user
            amount = bidonitem.amount

            data[user.username] = amount

        return Response(data=data,
                        status=status.HTTP_200_OK)


    def post(self,request):
        '''
        bidonitem creation
        :param request:
        :return:
        '''

        data = request.data
        serializer = BidOnItemSerializer(data=data,)

        if serializer.is_valid():
            bidonitem = serializer.save()
            return Response(data=serializer.data,
                            status=status.HTTP_201_CREATED)


        return Response(data=serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)