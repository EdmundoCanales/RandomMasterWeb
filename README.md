# RandomMasterWeb
Current version implements an Azure Function that performs a set of actions described below.
General purpose is to generate models that simulate a full set of data essentialy random, these models are
stored in an Azure Blob Storage then later is consumed by Power BI dashboard.
This report uses entire universe of combinatons from defined members and combination size:
e.g. 28 C 5, this generates 98,280 combination objects, each object contains a collection of properties:
- Level Key = Is a string that represents members of combination from each level (level1 = between 1 and 10, level2 = between 11 and 20, level3 = between 21 - 30) then for combination '2-5-17-22-28' returns '2-1-2'.
- Sequence Key = Is a string that represents the pattern of sequencial members in combination, taking same combination '2-5-17-22-28' it's SeqKey would be '1-1-1-1-1' as there are no sequential members, but for '1-2-13-14-21' it's SeqKey would be '2-2-1'.
- Prime count = returns the number of prime members within combination.
based on these properties report monitors accuracy of finding combinations of member groups with highest probability.


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