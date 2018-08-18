from mysiteApp.models import User,Pressure,Velocity
from django.http import HttpResponse
def velocity(request):
    # logger=logging.getLogger('mysiteApp.views')

    # data = simplejson.loads(req.body)
    user=User.objects.get(id=2)
    # return HttpResponse(user)
    start_time=1453442901782
    end_time=1453442901962
    d = Pressure.objects.filter(timestamp__range=(start_time,end_time))
    pList=[]
    for p in d:
        pList.append(p.device_id)
    # velocitytemp = Velocity(user=user, device_id=1, velocity=10.1232, distance=12.12234)
    # velocitytemp.save()
    vList=[]
    for vTem in pList:
        velocitytemp = Velocity(user=user,device_id=vTem,velocity=10.43431,distance=12.1222)
        vList.append(velocitytemp)
    # velocitytemp = Velocity(user_name=velocitytemp1,device_id=d,velocity=10.1231, distance=12.1222)
    # velocitytemp.save()
    # resultlist=[]
    # for temp in result:
    #      velocitytemp=Velocity(user=user,device_id=d.device_id,velocity=temp.velocity,distance=temp.distance)
    #      resultlist.append(velocitytemp)
    Velocity.objects.bulk_create(vList)
    return HttpResponse(d)