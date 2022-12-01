# -*- coding: utf-8 -*-
"""API module.

Created on: 20/6/22
@author: Heber Trujillo <heber.trj.urt@gmail.com>
Licence,
"""
from flask import (
    Flask,
    request,
)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import corelib.allocation.adapters.orm as orm
import corelib.allocation.adapters.repository as repository
import corelib.allocation.config as config
import corelib.allocation.domain.model as model
import corelib.allocation.service_layer.services as services

orm.start_mappers()
get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))
app = Flask(__name__)


@app.route("/allocate", methods=["POST"])
def allocate_endpoint():
    """Allocate order line to database batches."""
    session = get_session()
    repo = repository.SQLAlchemyRepository(session)
    line = model.OrderLine(
        request.json["orderid"],
        request.json["sku"],
        request.json["qty"],
    )

    try:
        batchref = services.allocate(line, repo, session)
    except (model.OutOfStock, services.InvalidSku) as e:
        return {"message": str(e)}, 400

    return {"batchref": batchref}, 201
