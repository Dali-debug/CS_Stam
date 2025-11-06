# 🔄 Migration Guide: Express.js → FastAPI

This document explains the migration from Node.js/Express to Python/FastAPI.

## 📊 Migration Summary

| Aspect | Express.js (Before) | FastAPI (After) |
|--------|---------------------|-----------------|
| **Language** | TypeScript/Node.js | Python 3.11+ |
| **Framework** | Express.js 4.18 | FastAPI 0.109 |
| **MongoDB Driver** | Mongoose (sync/async) | Motor (async) |
| **Validation** | Joi | Pydantic |
| **Server** | Node.js | Uvicorn (ASGI) |
| **Port** | 3000 | 8000 |
| **Package Manager** | npm | pip |
| **Config Files** | package.json, tsconfig.json | requirements.txt |
| **Type System** | TypeScript | Python type hints + Pydantic |

## 🗂️ File Structure Changes

### Before (Express.js)
```
src/
├── models/          # Mongoose schemas (.ts)
├── routes/          # Express routes (.ts)
├── services/        # Business logic (.ts)
├── middleware/      # Custom middleware (.ts)
├── validators/      # Joi schemas (.ts)
├── config/          # DB connection (.ts)
├── utils/           # Logger (.ts)
├── scripts/         # Utilities (.ts)
├── app.ts           # Express app
└── server.ts        # Entry point

package.json
tsconfig.json
```

### After (FastAPI)
```
app/
├── models/          # Pydantic models (.py)
├── routes/          # FastAPI routers (.py)
├── services/        # Business logic (.py)
├── config/          # DB connection (.py)
├── scripts/         # Utilities (.py)
└── main.py          # FastAPI app + entry point

requirements.txt
```

## 🔧 Key Technical Changes

### 1. Database Connection

**Before (Mongoose)**:
```typescript
import mongoose from 'mongoose';

await mongoose.connect(MONGODB_URI, {
  maxPoolSize: 10,
  minPoolSize: 2,
});
```

**After (Motor)**:
```python
from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient(
    MONGODB_URI,
    maxPoolSize=10,
    minPoolSize=2,
)
db = client[db_name]
```

### 2. Models

**Before (Mongoose Schema)**:
```typescript
const userSchema = new Schema({
  userId: { type: String, required: true, unique: true },
  profile: {
    firstName: { type: String, required: true },
    email: { type: String, required: true, unique: true },
  }
});
```

**After (Pydantic Model)**:
```python
from pydantic import BaseModel, EmailStr, Field

class Profile(BaseModel):
    first_name: str = Field(..., min_length=1)
    email: EmailStr

class UserModel(BaseModel):
    user_id: str
    profile: Profile
```

### 3. Routes

**Before (Express)**:
```typescript
router.post('/users', async (req, res) => {
  try {
    const user = await userService.createUser(req.body);
    res.status(201).json({ userId: user });
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});
```

**After (FastAPI)**:
```python
@router.post("/users", status_code=201)
async def create_user(user: UserModel):
    try:
        result = await user_service.create_user(user.dict())
        return {"user_id": result}
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))
```

### 4. Validation

**Before (Joi)**:
```typescript
const createUserSchema = Joi.object({
  userId: Joi.string().uuid().required(),
  profile: Joi.object({
    email: Joi.string().email().required(),
  })
});
```

**After (Pydantic - automatic)**:
```python
# Validation is built into Pydantic models!
class UserModel(BaseModel):
    user_id: str = Field(..., description="UUID")
    profile: Profile
    
    # Pydantic validates automatically
```

### 5. Service Layer

**Before (TypeScript)**:
```typescript
export class UserService {
  async createUser(userData: any): Promise<string> {
    const user = new User(userData);
    await user.save();
    return user.userId;
  }
}
```

**After (Python)**:
```python
class UserService:
    async def create_user(self, user_data: dict) -> str:
        collection = db_instance.db["users"]
        await collection.insert_one(user_data)
        return user_data["user_id"]
```

### 6. Middleware

**Before (Express Middleware)**:
```typescript
app.use(express.json());
app.use(cors());
app.use(helmet());
app.use(compression());
```

**After (FastAPI Middleware)**:
```python
app.add_middleware(CORSMiddleware, allow_origins=["*"])
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Helmet equivalent: Security headers are built-in
# JSON parsing is automatic
```

### 7. Error Handling

**Before (Express)**:
```typescript
app.use((err, req, res, next) => {
  logger.error(err);
  res.status(500).json({ error: err.message });
});
```

**After (FastAPI)**:
```python
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": str(exc)}
    )
```

## 📦 Dependency Installation

### Before (npm)
```powershell
npm install
npm run dev
npm run build
npm start
```

### After (pip)
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 🌐 API Changes

### Endpoints (No Change!)
All endpoints remain the same:
- `POST /api/users`
- `GET /api/users/{user_id}`
- `POST /api/sensor-data`
- etc.

### Auto-Generated Documentation

FastAPI provides **automatic** interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

No need to manually write API docs! 🎉

## ✅ What's Better in FastAPI?

1. **Automatic API Documentation** - Swagger UI + ReDoc generated automatically
2. **Built-in Validation** - Pydantic validates request/response automatically
3. **Type Safety** - Python type hints + Pydantic = excellent IDE support
4. **Async Native** - Better async support than Express
5. **Less Code** - No need for separate validation middleware
6. **Better Performance** - FastAPI is one of the fastest Python frameworks
7. **Editor Support** - Excellent autocomplete and error checking

## ⚠️ What to Watch Out For

1. **Async/Await** - Everything must be async (use `await` everywhere)
2. **MongoDB Queries** - Motor syntax slightly different from Mongoose
3. **No Auto-Reload** - Need `--reload` flag for development
4. **Python Virtual Environment** - Must activate venv before running
5. **Port Change** - Default port changed from 3000 → 8000

## 🚀 Quick Start Guide

### 1. Setup Environment

```powershell
# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Setup environment
Copy-Item .env.example .env
# Edit .env with MongoDB connection
```

### 2. Start Development

```powershell
# Start with auto-reload
uvicorn app.main:app --reload --port 8000

# Or use the quick start script
.\start.ps1
```

### 3. Access API

- Application: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs
- Alternative Docs: http://localhost:8000/redoc

### 4. Run Scripts

```powershell
# Seed database
python -m app.scripts.seed_data

# Test database
python -m app.scripts.test_database

# Validate data
python -m app.scripts.validate_data
```

## 📝 Migration Checklist

- [x] Created Python project structure
- [x] Converted database connection to Motor
- [x] Converted User model to Pydantic
- [x] Converted RawSensorData model to Pydantic
- [x] Converted ProcessedHealthMetrics model to Pydantic
- [x] Created UserService with async operations
- [x] Created user routes with FastAPI
- [x] Created main FastAPI app
- [x] Updated environment configuration
- [x] Created README for FastAPI
- [x] Created startup script
- [ ] Convert remaining 4 models (DailySummary, HealthRiskPrediction, Notification, AICoachInteraction)
- [ ] Convert remaining 4 services (SensorData, HealthMetrics, Prediction, AICoach)
- [ ] Convert remaining 4 route files (SensorData, HealthMetrics, Prediction, Chat)
- [ ] Convert seed_data script to Python
- [ ] Convert test_database script to Python
- [ ] Convert validate_data script to Python
- [ ] Update API_DOCUMENTATION.md for FastAPI

## 🔄 Next Steps

1. **Complete model conversion** - 4 remaining models
2. **Complete service conversion** - 4 remaining services
3. **Complete route conversion** - 4 remaining route files
4. **Convert scripts** - seed, test, validate
5. **Test everything** - Ensure all endpoints work
6. **Update documentation** - API docs for FastAPI

## 💡 Pro Tips

1. **Use type hints** - They make your code clearer and help with IDE support
2. **Leverage Pydantic** - It does validation + serialization + documentation
3. **Use async/await** - Motor requires async operations
4. **Check Swagger UI** - Automatic docs save time
5. **Use uvicorn --reload** - Auto-restart on code changes

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Motor (Async MongoDB) Documentation](https://motor.readthedocs.io/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Uvicorn Documentation](https://www.uvicorn.org/)

---

**Migration is in progress! Core structure is complete, remaining endpoints need conversion.**
