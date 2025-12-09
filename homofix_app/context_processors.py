from .models import AutoAssignSetting

def auto_assign_status(request):
    setting = AutoAssignSetting.objects.first()  # Only one record expected
    return {'auto_setting': setting}
