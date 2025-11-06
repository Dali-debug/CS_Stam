# CS_Stam

Healthcare wearable data processing and analysis system built with FastAPI and MongoDB.

## 📖 Overview

This repository contains a complete backend infrastructure for healthcare wearable applications, featuring real-time sensor data processing, health metrics analysis, AI-powered risk predictions, and an interactive health coach chatbot.

## 🏗️ Repository Structure

```
CS_Stam/
└── healthcare-mongodb-app/    # Main FastAPI application
    ├── app/                   # Application source code
    ├── README.md              # Detailed application documentation
    ├── START_HERE.md          # Quick start guide
    ├── DEPLOYMENT.md          # Production deployment guide
    └── MIGRATION.md           # Express.js to FastAPI migration notes
```

## 🚀 Quick Start

The main application is located in the `healthcare-mongodb-app` directory.

### Prerequisites

- **Python 3.11+**
- **MongoDB 6.0+** (local) or **MongoDB Atlas** account
- **pip** package manager

### Getting Started

1. **Navigate to the application directory**:
   ```bash
   cd healthcare-mongodb-app
   ```

2. **Follow the detailed setup instructions**:
   - See [healthcare-mongodb-app/README.md](./healthcare-mongodb-app/README.md) for complete installation and setup guide
   - See [healthcare-mongodb-app/START_HERE.md](./healthcare-mongodb-app/START_HERE.md) for a quick start walkthrough

## ✨ Key Features

- **Real-time Sensor Data Processing** - Handle PPG, IMU, temperature, and EDA data from wearable devices
- **Health Metrics Analysis** - Cardiovascular, activity, stress, and sleep tracking
- **AI Health Risk Predictions** - Multi-category risk assessment
- **AI Health Coach** - Interactive chatbot for health guidance
- **Automatic Data Lifecycle** - TTL indexes for efficient storage management
- **Production-Ready** - Async operations, logging, error handling, validation
- **RESTful API** - 30+ documented endpoints with auto-generated Swagger UI
- **Optimized for MongoDB Atlas Free Tier** - Supports ~100 users with 512MB storage

## 📚 Documentation

All detailed documentation is available in the `healthcare-mongodb-app` directory:

- **[README.md](./healthcare-mongodb-app/README.md)** - Complete setup guide, API documentation, and usage instructions
- **[START_HERE.md](./healthcare-mongodb-app/START_HERE.md)** - Quick start guide for getting up and running
- **[DEPLOYMENT.md](./healthcare-mongodb-app/DEPLOYMENT.md)** - Production deployment instructions
- **[MIGRATION.md](./healthcare-mongodb-app/MIGRATION.md)** - Notes on Express.js to FastAPI migration

## 🛠️ Tech Stack

- **FastAPI 0.109+** - Modern async Python web framework
- **Motor 3.3+** - Async MongoDB driver
- **Pydantic 2.5+** - Data validation and settings management
- **Uvicorn** - Lightning-fast ASGI server
- **MongoDB 6.0+** - NoSQL database with TTL indexes
- **Python 3.11+** - Required runtime

## 🔌 API Documentation

Once the application is running, you can access the auto-generated API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 📦 Main Application Components

### Collections
- **users** - User profiles, medical info, goals
- **rawSensorData** - Sensor readings (7-day TTL)
- **processedHealthMetrics** - Calculated metrics (30-day TTL)
- **dailySummary** - Daily aggregations (365-day TTL)
- **healthRiskPredictions** - AI predictions (90-day TTL)
- **notifications** - User alerts
- **aiCoachInteractions** - Chat history

### API Endpoints
- User Management (CRUD operations)
- Sensor Data Recording (single & batch)
- Health Metrics Retrieval & Analysis
- Risk Predictions
- Notifications Management
- AI Coach Chat Interface

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linting
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📄 License

MIT License

## 🆘 Support

For issues, questions, or support:
- Check the [detailed documentation](./healthcare-mongodb-app/README.md)
- Review the [deployment guide](./healthcare-mongodb-app/DEPLOYMENT.md)
- Open a GitHub issue

## 🎯 Project Status

This is an active project. The core FastAPI infrastructure is complete and production-ready. The application includes:

✅ Complete user management system  
✅ Real-time sensor data processing  
✅ Health metrics analysis  
✅ Database connection and pooling  
✅ Auto-generated API documentation  
✅ Comprehensive error handling and logging  
✅ Production deployment guides  

---

**Built with FastAPI ❤️ Python**

For detailed instructions and documentation, please refer to the [healthcare-mongodb-app README](./healthcare-mongodb-app/README.md).
