# -*- coding: utf-8 -*-
"""Configuration module for allocation library.

Created on: 20/6/22
@author: Heber Trujillo <heber.trj.urt@gmail.com>
Licence,
"""
import os


def get_postgres_uri() -> str:
    """Postgres url."""
    host = os.environ.get("DB_HOST", "localhost")
    port = 5432 if host == "localhost" else 5432
    password = os.environ.get("DB_PASSWORD", "allocation")
    user, db_name = "allocation", "allocation"
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"


def get_api_url() -> str:
    """Get API URL."""
    host = os.environ.get("API_HOST", "localhost")
    port = 5005 if host == "localhost" else 80
    return f"http://{host}:{port}"
