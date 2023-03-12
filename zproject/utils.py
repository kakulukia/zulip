from django.contrib.auth import get_user_model

from django_sso.sso_service.backend import EventAcceptor, acceptor


class LiebendgernEventAcceptor(EventAcceptor):
    """
    This class processes all events received from SSO service
    You can override it for change behavior

    Here the method name is equal to the event type. All event handlers must be decorated with @acceptor,
    or they will not be resolved as event receiver methods.
    """

    @acceptor
    def update_account(self, fields: dict):
        """
        Update or create user by identy

        Args:
            fields (dict): Array of fields for create/update user
        """
        user_model = get_user_model()
        user_identity = fields['user_identy']
        fields.pop('user_identy')

        additional_fields = {
            'realm_id': 2,
            'default_language': 'de',
            'twenty_four_hour_time': True,
            'color_scheme': 2,
            'tos_version': '1.0',
            'enable_login_emails': False,
        }

        fields.update(additional_fields)

        user_model.objects.update_or_create(**{
            user_model.USERNAME_FIELD: user_identity,
            'defaults': fields
        })

