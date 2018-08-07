from django.db import models
from django.utils.timezone import timedelta,datetime
from django.core.exceptions import ValidationError
import pytz


LOCAL_TZ = pytz.timezone('Asia/Kolkata',)
UTC = pytz.utc


from Items.utils import minimum_validator
from accounts.models import User

# Create your models here.
class item(models.Model):

    '''
    model to store item for bidding
    '''
    product_name = models.CharField(max_length=15)
    # duration for which the item is in auction
    expiration_time = models.DateTimeField(default=datetime.now()+timedelta(minutes=30),
                                           null=True,blank=True)
    expected_amount = models.IntegerField(blank=True,null=True)

    # date on which it was created
    creation_date = models.DateTimeField(auto_now=True)

    # column level validation
    starting_bid = models.PositiveIntegerField(validators=[minimum_validator])

    @property
    def endtime(self):
        return self.expiration_time.replace(tzinfo=pytz.utc).\
            astimezone(LOCAL_TZ).isoformat()

    def __unicode__(self):
        '''
        :return: Corrected time according to current time zone along with product name
        '''
        return self.product_name+'  |   Expiration:<' +self.endtime+'>'

    def save(self,*args,**kwargs):

        curtime = datetime.now()
        utcawarecurtime = UTC.localize(curtime)

        try:
            assert self.expiration_time - utcawarecurtime <= timedelta(hours=1)
        except AssertionError:
            raise ValidationError('Time for bidding to large')

        if not(self.expected_amount or self.expiration_time):
            raise ValidationError('both expected_amount and expiration_time not present')

        return super(item, self).save(*args, **kwargs)


class bidOnItem(models.Model):

    '''
    model to save an item's bidding
    '''

    user = models.ForeignKey(to=User,related_name='bidded_on',on_delete=models.CASCADE,null=True)
    item = models.ForeignKey(to=item,related_name='bids',on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now=True)
    amount = models.PositiveIntegerField(null=False,blank=False,
                                         validators=[minimum_validator])

    def __unicode__(self):
        return self.user.username+" >> "+str(self.amount)+" >> "+self.item.product_name

    def save(self,*args,**kwargs):
        '''
        applying table level validation by overriding the default behaviour
        :param args:
        :param kwargs:
        :return:
        '''

        try:
            minimum_validator(self.item.starting_bid)(self.amount)
        except ValidationError:
            raise ValidationError('Amount should not be lower than base amount')

        try:
            lastbid = bidOnItem.objects.filter(item=self.item).latest('creation_date')
            lastuser = lastbid.user
            lastamount = lastbid.amount

            minimum_validator(lastbid.amount)(self.amount)
        except ValidationError:
            raise ValidationError('Amount is Lesser than last Bid ')
        except bidOnItem.DoesNotExist:
            '''
                no previous bids exist for this item
            '''
            lastuser = None
            lastamount = 0
            pass


        try:
            assert self.user != lastuser
        except AssertionError:
            raise ValidationError("last bidder is the same as current bidder")

        # final validation

        curtime = datetime.now()

        utcawarecurtime = curtime.replace(tzinfo=LOCAL_TZ)


        try:


            endtime = self.item.expiration_time.replace(tzinfo=pytz.utc).astimezone(LOCAL_TZ) or\
                      utcawarecurtime

            print("curtime", utcawarecurtime)
            print("endtime", endtime)

            assert utcawarecurtime <= endtime

        except AssertionError:
            raise ValidationError("Bidding for this item got closed on:"+self.item.endtime)

        try:
            import sys
            assert lastamount <= (self.item.expected_amount or sys.maxint)

        except AssertionError:
            raise ValidationError("Item was already sold in the desired amount")

        # save in the db
        return super(bidOnItem,self).save(*args,**kwargs)