# -*- coding: utf-8 -*-
# Copyright (c) 2019 Dave Kruger.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holders nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
# THE POSSIBILITY OF SUCH DAMAGE.
from uuid import uuid4

from luxon import register
from luxon import SQLModel
from luxon.utils.timezone import now


@register.model()
class netrino_product(SQLModel):
    id = SQLModel.Uuid(default=uuid4, internal=True)
    name = SQLModel.String(null=False)
    parent_id = SQLModel.Uuid()
    price = SQLModel.Decimal(6, 2, default=0)
    monthly = SQLModel.Boolean(default=False)
    image = SQLModel.MediumBlob()
    image_type = SQLModel.String()
    description = SQLModel.LongText()
    domain = SQLModel.Fqdn(internal=True)
    creation_time = SQLModel.DateTime(default=now, internal=True)
    primary_key = id
    product_parent = SQLModel.ForeignKey(parent_id, id, on_delete='RESTRICT')

@register.model()
class netrino_custom_attr(SQLModel):
    id = SQLModel.Uuid(default=uuid4, internal=True)
    name = SQLModel.String(null=False)
    value = SQLModel.String()
    visible = SQLModel.Boolean(default=True)
    product_id = SQLModel.Uuid(internal=True)
    product_ref = SQLModel.ForeignKey(product_id, netrino_product.id)
    primary_key = id

@register.model()
class netrino_categories(SQLModel):
    id = SQLModel.Uuid(default=uuid4, internal=True)
    name = SQLModel.String(null=False)
    product_id = SQLModel.Uuid(null=False)
    product_category_ref = SQLModel.ForeignKey(product_id, netrino_product.id)
    primary_key = id

@register.model()
class netrino_product_entrypoint(SQLModel):
    id = SQLModel.Uuid(default=uuid4, internal=True)
    product_id = SQLModel.Uuid(null=False)
    entrypoint = SQLModel.String(null=False)
    metadata = SQLModel.MediumText()
    creation_time = SQLModel.DateTime(default=now, readonly=True)
    prod_entryp_ref = SQLModel.ForeignKey(product_id, netrino_product.id)
    unique_prod_entryp = SQLModel.UniqueIndex(product_id, entrypoint)
    primary_key = id

@register.model()
class netrino_payment_gateway(SQLModel):
    id = SQLModel.Uuid(default=uuid4, internal=True)
    product_id = SQLModel.Uuid(null=False)
    name = SQLModel.String(null=False)
    description = SQLModel.MediumText()
    creation_time = SQLModel.DateTime(default=now, readonly=True)
    prod_paygw_ref = SQLModel.ForeignKey(product_id, netrino_product.id)
    unique_prod_paygw = SQLModel.UniqueIndex(product_id, name)
    primary_key = id

# @Vuader: Todo: Linked products: upsell and cross sell
