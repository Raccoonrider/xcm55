from rest_framework.generics import RetrieveAPIView, ListAPIView

from api.serializers import *
  

class EventDetailAPIView(RetrieveAPIView):
    queryset = Event.objects.filter(active=True).order_by('pk')
    serializer_class = EventSerializer


class EventListAPIView(ListAPIView, EventDetailAPIView):
    queryset = Event.objects.filter(active=True, finished=False).order_by('date')


class AgeGroupListAPIView(ListAPIView):
    serializer_class = AgeGroupSerializer

    def get_queryset(self):        
        return AgeGroup.objects.filter(event__pk=self.kwargs['event__pk'])


class ApplicationListAPIView(ListAPIView):
    serializer_class = ApplicationSerializer

    def get_queryset(self):        
        return Application.objects.filter(event__pk=self.kwargs['event__pk'])

  
class ResultListAPIView(ListAPIView):
    serializer_class = ResultSerializer

    def get_queryset(self):        
        return Result.objects.filter(event__pk=self.kwargs['event__pk']).order_by('route')