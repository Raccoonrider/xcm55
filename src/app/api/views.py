from rest_framework.generics import RetrieveAPIView, ListAPIView

from api.serializers import *
  
class EventDetailAPIView(RetrieveAPIView):
    queryset = Event.objects.filter(active=True).order_by('pk')
    serializer_class = EventSerializer

class EventListAPIView(ListAPIView, EventDetailAPIView):
    pass

class RouteDetailAPIView(RetrieveAPIView):
    queryset = Route.objects.filter(active=True).order_by('pk')
    serializer_class = RouteSerializer

class RouteListAPIView(ListAPIView, RouteDetailAPIView):
    pass

  
class ApplicationDetailAPIView(RetrieveAPIView):
    queryset = Application.objects.filter(active=True).order_by('pk')
    serializer_class = ApplicationSerializer

class ApplicationListAPIView(ListAPIView, ApplicationDetailAPIView):
    pass

  
class ResultDetailAPIView(RetrieveAPIView):
    queryset = Result.objects.filter(active=True).order_by('pk')
    serializer_class = ResultSerializer

class ResultListAPIView(ListAPIView, ResultDetailAPIView):
    pass

class AgeGroupListAPIView(ListAPIView):
    serializer_class = AgeGroupSerializer

    def get_queryset(self):        
        return AgeGroup.objects.filter(event__pk=self.kwargs['event__pk'])