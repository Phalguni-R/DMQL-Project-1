# FMA Analytics - Windows Setup

## Prerequisites
- Docker Desktop running
- Python 3.9+
- Raw CSV files in `fma_metadata/`

---

## 1. Install Python Dependencies

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Windows:**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## 2. Create .env File

**Mac/Linux:**
```bash
cat > .env << 'EOF'
DB_USER=common-user-aph
DB_PASSWORD=aph1234
DB_HOST=localhost
DB_PORT=5432
DB_NAME=fma_db
EOF
```

**Windows:**
```powershell
@"
DB_USER=common-user-aph
DB_PASSWORD=aph1234
DB_HOST=localhost
DB_PORT=5432
DB_NAME=fma_db
"@ | Out-File .env -Encoding utf8
```

---

## 3. Configure dbt (One-time setup)

**Mac/Linux:**
```bash
mkdir -p ~/.dbt
cat > ~/.dbt/profiles.yml << 'EOF'
fma_analytics:
  target: dev
  outputs:
    dev:
      type: postgres
      host: localhost
      user: common-user-aph
      password: aph1234
      port: 5432
      dbname: fma_db
      schema: analytics
      threads: 1
EOF
```

**Windows:**
```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.dbt"
@"
fma_analytics:
  target: dev
  outputs:
    dev:
      type: postgres
      host: localhost
      user: common-user-aph
      password: aph1234
      port: 5432
      dbname: fma_db
      schema: analytics
      threads: 1
"@ | Out-File "$env:USERPROFILE\.dbt\profiles.yml" -Encoding utf8
```

---

## 4. PHASE 1 - Database Setup

**Mac/Linux:**
```bash
docker compose up -d postgres
sleep 10
docker compose exec -T postgres psql -U common-user-aph -d fma_db < schema.sql
python clean_and_report.py
python ingest_data.py
```

**Windows:**
```powershell
docker compose up -d postgres
Start-Sleep 10
Get-Content schema.sql | docker compose exec -T postgres psql -U common-user-aph -d fma_db
python clean_and_report.py
python ingest_data.py
```

---

## 5. PHASE 2 - dbt Analytics

**Mac/Linux:**
```bash
docker compose exec -T postgres psql -U common-user-aph -d fma_db < phase2_optimization.sql
cd fma_analytics
dbt debug
dbt run
cd ..
```

**Windows:**
```powershell
Get-Content phase2_optimization.sql | docker compose exec -T postgres psql -U common-user-aph -d fma_db
cd fma_analytics
dbt debug
dbt run
cd ..
```

---

## 6. PHASE 3 - Streamlit Dashboard

**All Platforms:**
```bash
docker compose down
docker compose up -d --build
```

**Open:** http://localhost:8501

---

## Common Commands

**Stop:**
```bash
docker compose down
```

**Start:**
```bash
docker compose up -d
```

**Restart Streamlit:**
```bash
docker compose restart streamlit
```

**Stop Streamlit:**
```bash
docker compose stop streamlit
```

**Rebuild dbt:**
```bash
cd fma_analytics && dbt run && cd ..
```

Done! 🎉
```

**NOW IT HAS dbt PROFILES SETUP FOR WINDOWS!** 🚀