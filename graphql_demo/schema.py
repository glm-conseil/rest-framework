# Copyright 2018 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

# disable undefined variable error, which erroneously triggers
# on forward declarations of classes in lambdas
# pylint: disable=E0602

import graphene

from odoo import _
from odoo.exceptions import UserError

from odoo.addons.graphql_base import OdooObjectType
from odoo.addons.graphql_demo.query_vg import QueryPartner, CreatePartner


class Query(QueryPartner):
    pass


class Mutation(graphene.ObjectType):
    create_partner = CreatePartner.Field(description="Documentation of CreatePartner")


schema = graphene.Schema(query=Query, mutation=Mutation)
