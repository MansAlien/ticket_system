from django.contrib import admin
from .models import Ticket, TicketReply
from django.utils.html import format_html
from django.urls import reverse

class TicketAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'status', 'created_at', 'image')

    def get_list_display(self, request):
        base_fields = ['name', 'user', 'status', 'created_at', 'image']
        if request.user.has_perm('auth.view_user'):
            return base_fields + ['reply_link']
        return base_fields

    def reply_link(self, obj):
        url = reverse('admin:tickets_ticketreply_add') + f'?ticket={obj.id}'
        return format_html('<a class="button" href="{}">Reply</a>', url)
    
    reply_link.short_description = 'Reply'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.has_perm('auth.view_user'):
            return qs
        return qs.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        obj.save()

    # 🔒 Hide 'user' field from form
    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        fields = [f for f in fields if f != 'user']
        return fields

    # 🛡️ Prevent user from editing 'user' field even if passed in request
    def get_readonly_fields(self, request, obj=None):
        readonly = super().get_readonly_fields(request, obj)
        if request.user.has_perm('auth.view_user'):
            return readonly + ('user',)
        return readonly
    
    
class TicketReplyAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'reply')

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        ticket_id = request.GET.get('ticket')
        if ticket_id:
            initial['ticket'] = ticket_id
        return initial
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.has_perm('auth.view_user'):
            return qs
        # Show only replies to user's own tickets
        return qs.filter(ticket__user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "ticket" and not request.user.has_perm('auth.view_user'):
            kwargs["queryset"] = Ticket.objects.filter(user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Ticket, TicketAdmin)
admin.site.register(TicketReply, TicketReplyAdmin)
