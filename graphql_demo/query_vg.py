# Copyright 2018 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

# disable undefined variable error, which erroneously triggers
# on forward declarations of classes in lambdas
# pylint: disable=E0602

import graphene

from odoo import _
from odoo.exceptions import UserError

from odoo.addons.graphql_base import OdooObjectType

from odoo.addons.graphql_demo.model import Partner


class QueryPartner(graphene.ObjectType):
    all_partners = graphene.List(
        graphene.NonNull(Partner),
        required=True,
        companies_only=graphene.Boolean(),
        id=graphene.Int(),
        limit=graphene.Int(),
        offset=graphene.Int(),
    )

    reverse = graphene.String(
        required=True,
        description="Reverse a string",
        word=graphene.String(required=True),
    )

    error_example = graphene.String()

    @staticmethod
    def resolve_all_partners(root, info, id=False, companies_only=False, limit=None, offset=None):
        domain = []
        if companies_only:
            domain.append(("is_company", "=", True))
        if id:
            domain.append(("id", "=", id))
        return info.context["env"]["res.partner"].search(
            domain, limit=limit, offset=offset
        )

    @staticmethod
    def resolve_reverse(root, info, word):
        return word[::-1]

    @staticmethod
    def resolve_error_example(root, info):
        raise UserError(_("UserError example"))


class CreatePartner(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        is_company = graphene.Boolean()
        raise_after_create = graphene.Boolean()

    Output = Partner

    @staticmethod
    def mutate(self, info, name, email, is_company=False, raise_after_create=False):
        env = info.context["env"]
        partner = env["res.partner"].create(
            {"name": name, "email": email, "is_company": is_company}
        )
        if raise_after_create:
            raise UserError(_("as requested"))
        return partner