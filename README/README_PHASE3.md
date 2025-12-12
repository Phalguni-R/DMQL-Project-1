# Phase 3: Streamlit Dashboard

## 👥 Team Structure

**3 Team Members × 2 Visualizations Each = 6 Total Visualizations**

- **Arun** - Page 1 (✅ COMPLETE)
  - Genre Radar Chart
  - Artist Geographic Heatmap

- **Phalguni** - Page 2 (🚧 TODO)
  - Visualization 1: TBD
  - Visualization 2: TBD

- **Halle** - Page 3 (🚧 TODO)
  - Visualization 1: TBD
  - Visualization 2: TBD

---

## 🚀 How to Run

### Step 1: Make sure you have all files in place

```
your-project/
├── streamlit_app/
│   ├── app.py
│   ├── .streamlit/config.toml
│   ├── pages/
│   │   ├── 1_Arun_Visualizations.py
│   │   ├── 2_Phalguni_Visualizations.py
│   │   └── 3_Halle_Visualizations.py
│   ├── utils/
│   │   ├── db_connection.py
│   │   └── queries.py
│   ├── Dockerfile
│   └── requirements.txt
├── docker-compose.yml (NEW - replaced)
└── ... (your existing Phase 1 & 2 files)
```

### Step 2: Stop existing containers

```bash
docker compose down
```

### Step 3: Start everything

```bash
docker compose up -d --build
```

### Step 4: Access dashboard

Open browser: **http://localhost:8501**

---

## 🐛 Troubleshooting

**Dashboard won't load?**
```bash
docker compose ps              # Check status
docker compose logs streamlit  # Check logs
```

**Database connection error?**
```bash
docker compose exec postgres psql -U common-user-aph -d fma_db -c "\dt analytics.*"
```

**Port already in use?**
```bash
lsof -ti:8501 | xargs kill -9  # Mac/Linux
```
