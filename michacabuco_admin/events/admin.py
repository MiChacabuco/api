from django.contrib import admin


from .models import Event, EventDate


class EventDateInline(admin.StackedInline):
    model = EventDate
    extra = 1


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fields = ("title", "body", "image", "youtube")
    inlines = (EventDateInline,)

    def get_queryset(self, request):
        return Event.objects.filter(created_by=request.user)

    def save_model(self, request, event: Event, *args, **kwargs):
        # Save user that created the event
        event.created_by = request.user
        event.save()
