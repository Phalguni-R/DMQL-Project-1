# Complete Setup - Phase 1 to 3

## Prerequisites
- Docker running
- Python 3.9+
- Raw CSV files in `fma_metadata/`

---

## Clean Start (if restarting)

```bash
docker compose down -v
rm -rf fma_metadata_cleaned/
cd fma_analytics && rm -rf target/ logs/ && cd ..
```

---

## Setup

### Install Dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Create .env file
```bash
cat > .env << 'EOF'
DB_USER=common-user-aph
DB_PASSWORD=aph1234
DB_HOST=localhost
DB_PORT=5432
DB_NAME=fma_db
EOF
```

---

## PHASE 1: Database & Data

```bash
# Start database
docker compose up -d postgres
sleep 10

# Create schema
docker compose exec -T postgres psql -U common-user-aph -d fma_db < schema.sql

# Clean data
python clean_and_report.py

# Ingest data
python ingest_data.py

# Verify
docker compose exec postgres psql -U common-user-aph -d fma_db -c "SELECT COUNT(*) FROM \"Artists\";"
```

---

## PHASE 2: dbt Analytics

```bash
# Create indexes
docker compose exec -T postgres psql -U common-user-aph -d fma_db < phase2_optimization.sql

# Build dbt models
cd fma_analytics
dbt debug
dbt run
cd ..

# Verify
docker compose exec postgres psql -U common-user-aph -d fma_db -c "\dt analytics.*"
```

---

## PHASE 3: Streamlit Dashboard

```bash
# Build and start
docker compose down
docker compose up -d --build

# Verify
docker compose ps
docker compose logs streamlit
```

**Open:** http://localhost:8501

---

## Quick Commands

```bash
# Stop everything
docker compose down

# Start everything
docker compose up -d

# Restart streamlit only
docker compose restart streamlit

# Stop streamlit only 
docker compose stop streamlit

# View logs
docker compose logs -f streamlit

# Rebuild dbt
cd fma_analytics && dbt run && cd ..
