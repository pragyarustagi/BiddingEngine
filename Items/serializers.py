from rest_framework import serializers

from Items.models import item,bidOnItem
from accounts.models import User


class ItemSerializer(serializers.ModelSerializer):
    '''
    serializers for serializing Item model
    '''

    class Meta:
        model = item
        fields = ('product_name',
                  'expiration_time',
                  'starting_bid',
                  'id',
                  )


class BidOnItemSerializer(serializers.ModelSerializer):
    '''
    serializer for serializing BidOnitem model
    '''
    d = serializers.DateTimeField()
    item = serializers.SlugRelatedField(slug_field='product_name',
                                        queryset=item.objects.all()
                                        )
    user = serializers.SlugRelatedField(slug_field='username',
                                        queryset=User.objects.all())

    class Meta:
        model = bidOnItem
        fields = ('item',
                  'user',
                  'creation_date',
                  'amount',
                  )