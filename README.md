# RandomMasterWeb
This is the first attempt to implement CI/CD to RandomMaster, move core features and functionality to web.

"""
# 🎲 Combination Generator API (Azure Functions)

A backend API built with Azure Functions (Python) to:
- 🎰 Generate random combinations from a sample
- 📝 Insert combinations into a database (future step)

## 🔌 Example Request (POST)
```json
{
  "functionName": "generateCombination",
  "sample": [1,2,3,4,5,6,7,8,9,10],
  "combinationSize": 5
}
```

## 📦 Endpoints
- `/api/HttpTriggerAPI` (POST only)

## 🚀 Run Locally
```bash
func start
```

## 📁 Folder Reference
- `HttpTriggerAPI/__init__.py` → routes and handles API logic
- `utils/logic.py` → contains `generate_combination()` function

---
Made with ❤️, caffeine, and slightly too much Blink-182.
"""