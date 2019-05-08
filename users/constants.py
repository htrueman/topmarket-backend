from django.utils.translation import ugettext as _

DOMEN = (
    ('DM', _("Домен")),
    ('SDM', _('Поддомен'))
)

CALL_BACK = (
    ('YES', _('Включена')),
    ('NO', _('Выключена'))
)

USER_ROLE = (
    ('CONTRACTOR', _('Поставщик')),
    ('PARTNER', _('Партнер')),
)


USER_POCKET = (
    ('BASE', 'Base'),
    ('FULL', 'Full'),
    ('NO', 'No')
)