import json

from odoo.http import request

from lxml import etree
from lxml.builder import E
from odoo.exceptions import UserError
from odoo import api, fields, models, tools, SUPERUSER_ID, _


TICKET_PRIORITY = [
    ('0', 'All'),
    ('1', 'Low priority'),
    ('2', 'High priority'),
    ('3', 'Urgent'),
]


#
def name_boolean_group(id):
    return 'in_group_' + str(id)


def name_selection_groups(ids):
    return 'sel_groups_' + '_'.join(str(it) for it in ids)


def is_boolean_group(name):
    return name.startswith('in_group_')


def is_selection_groups(name):
    return name.startswith('sel_groups_')


def is_reified_group(name):
    return is_boolean_group(name) or is_selection_groups(name)


def get_boolean_group(name):
    return int(name[9:])


def get_selection_groups(name):
    return [int(v) for v in name[11:].split('_')]


class IrMailServer(models.Model):
    """Represents an SMTP server, able to send outgoing emails, with SSL and TLS capabilities."""
    _inherit = "ir.mail_server"
    _description = 'Mail Server'

    smtp_user = fields.Char(string='Username', help="Optional username for SMTP authentication",
                            groups='user_security.group_system,user_security.group_admin')
    smtp_pass = fields.Char(string='Password', help="Optional password for SMTP authentication",
                            groups='base.group_system,user_security.group_admin')


class Http(models.AbstractModel):
    _inherit = 'ir.http'

    def webclient_rendering_context(self):
        """ Overrides community to prevent unnecessary load_menus request """
        return {
            'session_info': json.dumps(self.session_info()),
        }

    def session_info(self):
        ICP = request.env['ir.config_parameter'].sudo()
        User = request.env['res.users']

        if User.has_group('base.group_system'):
            warn_enterprise = 'admin'
        elif User.has_group('user_security.group_admin'):
            warn_enterprise = 'hadmin'
        elif User.has_group('base.group_user'):
            warn_enterprise = 'user'
        else:
            warn_enterprise = False

        result = super(Http, self).session_info()
        result['warning'] = warn_enterprise
        result['expiration_date'] = ICP.get_param('database.expiration_date')
        result['expiration_reason'] = ICP.get_param('database.expiration_reason')
        return result


class GroupsView(models.Model):
    _inherit = 'res.groups'

    @api.model
    def _update_user_groups_view(self):
        """ Modify the view with xmlid ``base.user_groups_view``, which inherits
            the user form view, and introduces the reified group fields.
        """
        if self._context.get('install_mode'):
            # use installation/admin language for translatable names in the view
            user_context = self.env['res.users'].context_get()
            self = self.with_context(**user_context)

        # We have to try-catch this, because at first init the view does not
        # exist but we are already creating some basic groups.
        # field_name = name_boolean_group(g.id)
        view = self.env.ref('base.user_groups_view', raise_if_not_found=False)
        if view and view.exists() and view._name == 'ir.ui.view':
            group_no_one = view.env.ref('base.group_no_one')
            group_employee = view.env.ref('base.group_user')
            group_admin = view.env.ref('access_right.group_lgis')
            xml1, xml2, xml3 = [], [], []
            xml1.append(E.separator(string=_('User Type'), colspan="2", groups='base.group_no_one'))
            xml2.append(E.separator(string=_('Application Accesses'), colspan="2"))

            user_type_field_name = ''
            for app, kind, gs in self.get_groups_by_application():
                attrs = {}
                # hide groups in categories 'Hidden' and 'Extra' (except for group_no_one)
                # if app.xml_id in ('base.module_category_hidden', 'base.module_category_extra', 'base.module_category_usability'):
                #     attrs['groups'] = 'base.group_no_one'

                # attrs = {'groups': 'base.group_no_one,base.group_system'} if app and (
                attrs = {'groups': 'base.group_system'} if app and (
                        app.xml_id == 'base.module_category_hidden'
                        or app.xml_id == 'base.module_category_extra'
                        or app.xml_id == 'base.module_category_usability'
                        or app.xml_id == 'base.module_category_administration'
                ) else {}

                # User type (employee, portal or public) is a separated group. This is the only 'selection'
                # group of res.groups without implied groups (with each other).
                if app.xml_id == 'base.module_category_user_type':
                    # application name with a selection field
                    field_name = name_selection_groups(gs.ids)
                    user_type_field_name = field_name
                    attrs['widget'] = 'radio'
                    attrs['groups'] = 'base.group_no_one'
                    xml1.append(E.field(name=field_name, **attrs))
                    xml1.append(E.newline())

                elif kind == 'selection':
                    # application name with a selection field
                    field_name = name_selection_groups(gs.ids)
                    xml2.append(E.field(name=field_name, **attrs))
                    xml2.append(E.newline())
                else:
                    # application separator with boolean fields
                    app_name = app.name or _('Other')
                    xml3.append(E.separator(string=app_name, colspan="4", **attrs))
                    for g in gs:
                        field_name = name_boolean_group(g.id)
                        if g == group_no_one:
                            # make the group_no_one invisible in the form view
                            xml3.append(E.field(name=field_name, invisible="1", **attrs))
                        # elif g == group_admin and self.env.user.has_group('user_security.group_application'):
                        elif g == group_admin and not self.env.user.has_group('base.group_erp_manager'):
                            # raise UserWarning('Yes')
                            # elif g == group_admin:
                            # raise UserWarning(self.env['res.users'].has_group('user_security.group_application'))
                            # make the group_no_one invisible in the form view
                            xml3.append(E.field(name=field_name, invisible="1", **attrs))
                        else:
                            xml3.append(E.field(name=field_name, **attrs))

            xml3.append({'class': "o_label_nowrap"})
            if user_type_field_name:
                user_type_attrs = {'invisible': [(user_type_field_name, '!=', group_employee.id)]}
            else:
                user_type_attrs = {}

            xml = E.field(
                E.group(*(xml1), col="2"),
                E.group(*(xml2), col="2", attrs=str(user_type_attrs)),
                E.group(*(xml3), col="4", attrs=str(user_type_attrs)), name="groups_id", position="replace")
            xml.addprevious(etree.Comment("GENERATED AUTOMATICALLY BY GROUPS"))
            xml_content = etree.tostring(xml, pretty_print=True, encoding="unicode")

            new_context = dict(view._context)
            new_context.pop('install_mode_data', None)  # don't set arch_fs for this computed view
            new_context['lang'] = None
            view.with_context(new_context).write({'arch': xml_content})
