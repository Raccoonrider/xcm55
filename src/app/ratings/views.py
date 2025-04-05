from collections import defaultdict, namedtuple
from datetime import date

from django.shortcuts import render
from django.http import Http404
from django.urls import reverse

from events.models import Event, Result
from common.enums import ResultStatus

DropdownData = namedtuple('DropdownData', ['text', 'url'])

scores = [80, 74, 68, 63, 59, 56, 54, 52, 50, 48, 46, 44, 42, 40, 38, 36, 34, 32, 30, 28, 26, 24, 22, 20, 18, 16, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
SCORES = defaultdict(lambda: 1, {a:b for a,b in enumerate(scores)})

def rating(request, year:int=None):
    if year is None:
        if date.today().month < 11:
            year = date.today().year - 1
        else:
            year = date.today().year

    events = Event.objects.filter(date__year=year)

    if not events:
        raise Http404
    
    rating_items = {}

    for event in events:
        results = Result.objects.filter(
            event=event,
            active=True, 
            route__halfmarathon=False,
            status=ResultStatus.OK,
        ).order_by('time', 'user_profile__last_name')

        for place, result in enumerate(results):
            rating_item = (
                rating_items.get(result.user_profile.id)
                or {
                    'user_profile': result.user_profile,
                    'score': 0,
                    'places': [],
                }
            )
            rating_item['score'] += SCORES[place]
            rating_item['places'].append(place + 1)
            rating_items[result.user_profile.id] = rating_item

    rating = sorted(rating_items.values(), key=lambda x: (-x['score'], x['user_profile'].last_name))
    
    place = 0
    prev_score = 0
    for i, item in enumerate(rating, start=1):
        if item['score'] != prev_score:
            place = i
        prev_score = item['score']
        item['place'] = place
        item['places'] = ', '.join(str(x) for x in item['places'])

    context = {
        'request': request,
        'rating': rating,
        'year': year,
        'scores': SCORES,
    }
    return render(
        request=request, 
        template_name='ratings/rating.html', 
        context=context)

def hx_ratings(request):
        events = Event.objects.filter(active=True, finished=True)

        years = sorted([event.date.year for event in events], reverse=True)
        if date.today().month < 11 and years[0] == date.today().year:
            years = years[1:]
        data = [DropdownData(url=reverse('rating_detail', kwargs = {'year':year}), text=F"Рейтинг-{year}") for year in years]

        context = {
            'data': data
        }
        return render(request=request, template_name='hx-nav-dropdown.html', context=context)

                
