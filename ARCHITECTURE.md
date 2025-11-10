# AutoPipelineAI v0.3.0 - System Architecture

## 📊 Visual Architecture Diagram

![Architecture Diagram](./architecture_diagram.png)

---

## 🏗️ Architecture Overview

AutoPipelineAI is built on a layered architecture with clear separation of concerns, enabling modularity, scalability, and maintainability.

---

## 📐 Architecture Layers

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     USER INTERFACE LAYER                                 │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │          Streamlit Web Application (Port 8501)                    │  │
│  │  • Interactive Dashboard • Real-time Updates • 5 Modes            │  │
│  └───────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────┬──────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                  MODE SELECTION & ROUTING LAYER                         │
│  ┌────────────────────────────────────────────────────────┐            │
│  │                   Mode Router                           │            │
│  └───┬────────┬────────┬────────┬────────┬────────────────┘            │
│      │        │        │        │        │                              │
│  ┌───▼──┐ ┌──▼──┐ ┌───▼──┐ ┌──▼──┐ ┌──▼─────┐                         │
│  │Manual│ │ LLM │ │Agent │ │ PDF │ │Database│                         │
│  │ Mode │ │Mode │ │ Mode │ │Mode │ │  Mode  │                         │
│  └──┬───┘ └──┬──┘ └───┬──┘ └──┬──┘ └───┬────┘                         │
└─────┼────────┼─────────┼───────┼─────────┼──────────────────────────────┘
      │        │         │       │         │
      ▼        ▼         ▼       ▼         ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                     CORE PROCESSING LAYER                                │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │   ETL    │  │  Ollama  │  │  Agent   │  │   PDF    │  │    DB    │ │
│  │  Module  │  │  Client  │  │Orchestr. │  │Extractor │  │ Handlers │ │
│  ├──────────┤  ├──────────┤  ├──────────┤  ├──────────┤  ├──────────┤ │
│  │• Loading │  │• llama3  │  │• ETL Agt │  │• Text    │  │• DuckDB  │ │
│  │• Trans.  │  │• mistral │  │• Query   │  │• Tables  │  │• SQLite  │ │
│  │• Schema  │  │• phi3    │  │• Profile │  │• NER     │  │• SQL UI  │ │
│  │  Valid.  │  │• Prompts │  │• Router  │  │• Entity  │  │• Query   │ │
│  │          │  │• CodeExe │  │          │  │          │  │          │ │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘ │
└───────┼─────────────┼─────────────┼─────────────┼─────────────┼────────┘
        │             │             │             │             │
        └─────┬───────┴──────┬──────┴──────┬──────┴──────┬──────┘
              │              │             │             │
              ▼              ▼             ▼             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                     SUPPORT SERVICES LAYER                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐               │
│  │  Cache   │  │  Memory  │  │  Config  │  │ Security │               │
│  │ Manager  │  │  Store   │  │          │  │  Layer   │               │
│  ├──────────┤  ├──────────┤  ├──────────┤  ├──────────┤               │
│  │• Memory  │  │• Conv.   │  │• Env Var │  │• Sandbox │               │
│  │• Disk    │  │  History │  │• Dir     │  │• Safety  │               │
│  │• TTL     │  │• Session │  │  Setup   │  │  Checks  │               │
│  │  Mgmt    │  │• Context │  │• Settings│  │• Module  │               │
│  │          │  │• Logging │  │          │  │  White.  │               │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘               │
└───────┼─────────────┼─────────────┼─────────────┼────────────────────────┘
        │             │             │             │
        └─────┬───────┴──────┬──────┴──────┬──────┘
              │              │             │
              ▼              ▼             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                     DATA STORAGE LAYER                                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐               │
│  │  DuckDB  │  │  SQLite  │  │ Parquet  │  │   CSV    │               │
│  │Analytics │  │ Storage  │  │  Files   │  │  Files   │               │
│  ├──────────┤  ├──────────┤  ├──────────┤  ├──────────┤               │
│  │• High    │  │• Light   │  │• Column  │  │• Simple  │               │
│  │  Perf    │  │  weight  │  │  Format  │  │  Format  │               │
│  │• OLAP    │  │• OLTP    │  │• Fast    │  │• Export  │               │
│  │• In-Mem  │  │• Persist │  │  Read    │  │• Compat  │               │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘               │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Data Flow Patterns

### 1. **Manual ETL Flow**
```
User Input → Manual Mode → ETL Module → Schema Validation
→ Transformation → Cache → Storage (CSV/Parquet)
```

### 2. **LLM Query Flow**
```
User Question → LLM Mode → Ollama Client → Prompt Template
→ Code Generation → Safe Execution → Result Display
→ Memory Store (History)
```

### 3. **Agent Workflow Flow**
```
User Description → Agent Mode → Orchestrator → Task Breakdown
→ [ETL Agent | Query Agent | Profiling Agent] → Execution
→ Result Aggregation → Cache → Display
```

### 4. **PDF Processing Flow**
```
PDF Upload → PDF Mode → PDF Extractor → [Text | Tables | NER]
→ Entity Recognition → Structured Data → Storage
```

### 5. **Database Analytics Flow**
```
SQL Query → Database Mode → DB Handler → [DuckDB | SQLite]
→ Query Execution → Result Set → Display
```

---

## 🧩 Component Details

### **Layer 1: User Interface**
- **Technology:** Streamlit 1.30+
- **Features:**
  - Responsive web interface
  - Real-time updates
  - Session state management
  - Multi-tab navigation

### **Layer 2: Mode Router**
- **Responsibility:** Route user requests to appropriate mode
- **Modes:**
  1. **Manual Mode** - Traditional ETL operations
  2. **LLM Mode** - Natural language queries
  3. **Agent Mode** - Multi-agent workflows
  4. **PDF Mode** - Document processing
  5. **Database Mode** - SQL analytics

### **Layer 3: Core Processing**

#### **ETL Module**
- **Purpose:** Extract, Transform, Load operations
- **Features:**
  - Multiple format support (CSV, Excel, Parquet)
  - Schema validation
  - Data cleaning and transformation
  - Error handling and logging

#### **Ollama Client**
- **Purpose:** LLM integration for natural language processing
- **Models:** llama3, mistral, phi3
- **Features:**
  - Connection health checks
  - Prompt template management
  - Safe code execution
  - Response parsing

#### **Agent Orchestrator**
- **Purpose:** Multi-agent task coordination
- **Agents:**
  - **ETL Agent** - Data transformation tasks
  - **Query Agent** - Natural language queries
  - **Profiling Agent** - Data quality assessment
- **Features:**
  - Task routing
  - Workflow execution
  - Result aggregation
  - Error recovery

#### **PDF Extractor**
- **Purpose:** Document intelligence
- **Features:**
  - Text extraction (pdfplumber, PyMuPDF)
  - Table extraction with structure
  - Named Entity Recognition (spaCy)
  - Image extraction
  - Metadata extraction

#### **Database Handlers**
- **DuckDB Handler:**
  - High-performance analytics
  - In-memory OLAP
  - Direct Parquet/CSV reading
- **SQLite Handler:**
  - Lightweight persistent storage
  - Transaction support
  - Backup functionality

### **Layer 4: Support Services**

#### **Cache Manager**
- **Backends:** Memory + Disk
- **Features:**
  - TTL (Time-To-Live) management
  - Automatic expiration
  - Key generation
  - Statistics tracking

#### **Memory Store**
- **Purpose:** Session and context management
- **Features:**
  - Conversation history (max 100 entries)
  - Session data persistence
  - Context sharing
  - Execution logging
  - JSON export/import

#### **Configuration**
- **Method:** Environment variables (.env)
- **Settings:**
  - Ollama connection
  - Database paths
  - Cache configuration
  - Logging levels
  - Directory structure

#### **Security Layer**
- **Features:**
  - Code execution sandbox
  - Dangerous pattern detection
  - Module whitelist
  - Input validation
  - Safe imports only

### **Layer 5: Data Storage**

#### **DuckDB** (Analytics)
- OLAP workloads
- Fast aggregations
- Analytical queries

#### **SQLite** (Storage)
- OLTP workloads
- Session persistence
- Relational data

#### **Parquet** (Column Format)
- Efficient compression
- Fast columnar reads
- Schema evolution

#### **CSV** (Simple Format)
- Universal compatibility
- Easy export/import
- Human-readable

---

## 🔐 Security Architecture

```
┌─────────────────────────────────────────────┐
│         Security Checkpoints                │
├─────────────────────────────────────────────┤
│ 1. Input Validation                         │
│    └─ User inputs sanitized                 │
│                                              │
│ 2. Code Sandbox                             │
│    └─ Restricted execution environment      │
│                                              │
│ 3. Module Whitelist                         │
│    └─ Only safe modules allowed             │
│                                              │
│ 4. Pattern Detection                        │
│    └─ Dangerous code patterns blocked       │
│                                              │
│ 5. Connection Validation                    │
│    └─ Ollama health checks                  │
└─────────────────────────────────────────────┘
```

---

## ⚡ Performance Optimizations

### **Caching Strategy**
- **L1 Cache:** In-memory (fastest, limited size)
- **L2 Cache:** Disk-based (persistent, larger)
- **TTL:** Automatic expiration (default 1 hour)

### **Database Selection**
- **DuckDB:** For analytics and aggregations
- **SQLite:** For transactional operations
- **Parquet:** For column-based storage

### **Lazy Loading**
- Heavy dependencies loaded on-demand
- Reduced initial startup time
- Memory-efficient operation

---

## 🧪 Testing Architecture

```
tests/
├── test_cache.py          # Cache manager & memory store
├── test_database.py       # DuckDB & SQLite handlers
├── test_llm.py           # LLM utilities & code executor
└── test_agents.py        # Agent system (future)

Testing Strategy:
✅ Unit tests for all core modules
✅ Integration tests for workflows
✅ Mock external dependencies (Ollama)
✅ Edge case coverage
✅ Performance benchmarks
```

---

## 📈 Scalability Considerations

### **Horizontal Scaling**
- Stateless design enables multiple instances
- Session data in SQLite for sharing
- Cache synchronization via Redis (planned)

### **Vertical Scaling**
- DuckDB for in-memory analytics
- Efficient data structures
- Lazy loading and caching

### **Future Enhancements**
- Docker containerization
- FastAPI REST endpoints
- Distributed task queue
- WebSocket support for real-time updates

---

## 🔧 Technology Stack

| Layer | Technologies |
|-------|-------------|
| **UI** | Streamlit, Plotly, Altair |
| **Backend** | Python 3.10+, Pandas, PyArrow |
| **LLM** | Ollama, LangChain, CrewAI |
| **Database** | DuckDB, SQLite, SQLAlchemy |
| **Documents** | PyMuPDF, pdfplumber, spaCy |
| **Cache** | diskcache, Redis |
| **Testing** | pytest, unittest |
| **Logging** | Loguru |

---

## 📝 Design Principles

1. **Modularity** - Each component has a single responsibility
2. **Extensibility** - Easy to add new modes and agents
3. **Privacy-First** - 100% local execution, no cloud dependencies
4. **Safety** - Sandboxed code execution, input validation
5. **Performance** - Multi-level caching, efficient databases
6. **Maintainability** - Type hints, docstrings, tests
7. **User-Friendly** - Intuitive UI, clear error messages

---

## 🎯 Key Design Decisions

### **Why Streamlit?**
- Rapid prototyping
- Beautiful UI out-of-the-box
- Python-native (no HTML/CSS/JS needed)
- Active community

### **Why Ollama?**
- 100% local execution
- Privacy-first
- No API costs
- Multiple model support

### **Why DuckDB?**
- Analytical query performance
- Zero-dependency installation
- In-memory and persistent modes
- Direct Parquet/CSV reading

### **Why Multi-Agent?**
- Task specialization
- Parallel execution potential
- Better error isolation
- Easier maintenance

---

## 📚 Further Reading

- [Detailed Documentation](README_v0.3.md)
- [Quick Start Guide](QUICKSTART.md)
- [Upgrade Summary](UPGRADE_SUMMARY.md)
- [PlantUML Diagram](architecture.puml)

---

**Architecture Version:** 0.3.0
**Last Updated:** November 2025
**Author:** Nitesh Ranjan Singh
