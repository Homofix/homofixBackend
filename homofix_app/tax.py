from .models import HodSharePercentage


def tax():

        
    hod_share_percentage = HodSharePercentage.objects.latest('id')

    