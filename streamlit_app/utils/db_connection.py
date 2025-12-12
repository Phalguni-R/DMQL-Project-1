"""
Database Connection Utility
Handles PostgreSQL connections for the Streamlit dashboard
"""

import psycopg2
from psycopg2.extras import RealDictCursor
import pandas as pd
import streamlit as st
from typing import Optional

# Database configuration
DB_CONFIG = {
    'host': 'postgres',  # Docker service name
    'port': 5432,
    'database': 'fma_db',
    'user': 'common-user-aph',
    'password': 'aph1234'
}


@st.cache_resource
def get_connection():
    """
    Create and cache a database connection
    Returns: psycopg2 connection object
    """
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        st.error(f"❌ Database connection failed: {str(e)}")
        st.info("💡 Make sure PostgreSQL container is running: `docker compose up -d`")
        return None


def execute_query(query: str, params: Optional[tuple] = None) -> pd.DataFrame:
    """
    Execute a SQL query and return results as a pandas DataFrame

    Args:
        query: SQL query string
        params: Optional tuple of parameters for parameterized queries

    Returns:
        pandas DataFrame with query results
    """
    conn = get_connection()
    if conn is None:
        return pd.DataFrame()

    try:
        df = pd.read_sql_query(query, conn, params=params)
        return df
    except Exception as e:
        st.error(f"❌ Query execution failed: {str(e)}")
        st.code(query, language='sql')
        return pd.DataFrame()


def test_connection():
    """
    Test the database connection
    Returns: True if successful, False otherwise
    """
    conn = get_connection()
    if conn is None:
        return False

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        cursor.close()
        st.success(f"✅ Connected to PostgreSQL")
        st.caption(version)
        return True
    except Exception as e:
        st.error(f"❌ Connection test failed: {str(e)}")
        return False


def get_table_info(schema: str = 'analytics') -> pd.DataFrame:
    """
    Get information about tables in a schema

    Args:
        schema: Schema name (default: 'analytics')

    Returns:
        DataFrame with table information
    """
    query = """
    SELECT 
        table_name,
        pg_size_pretty(pg_total_relation_size(quote_ident(table_schema)||'.'||quote_ident(table_name))) AS size
    FROM information_schema.tables
    WHERE table_schema = %s
    ORDER BY table_name;
    """
    return execute_query(query, (schema,))
