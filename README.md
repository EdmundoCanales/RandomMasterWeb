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

## 🧩 Combinations Properties
- When a `combination` object is created it contains a set of properties that can be used for data clustering and classification. <br> below are described current calculated properties using `{1,3,13,18,26}` for refference.

  |Property|Description|Result|
  |:--------:|:-----------:|------|
  |LevelKey|Entire *'Sample'* is divided in levels of *size* 10, e.g. 28/10 results in 3 levels: L1 = 1 to 10, L2 = 11 to 20, L3 = 21 to 28.| **2-2-1** : L1 = 1,3, L2 = 13,18 and L3 = 26|
  |SeqKey| Represents Sequential numbers in combination (n, n+1, n+2 ...) when a member is not in *Sequence* is represented by a unit.| **1-1-1-1-1** : no sequential members found.|
  |Level Members| JSON format returning an array of levels with respective members.|`[{"L1":"1,3","L2":"13,18", "L3":"26"}]`|
  |Prime Count| Returns the count of Prime numbers in combination | **2** : 3 and 13 are prime numbers.|
  
  In progress properties calculation:
  |Property|Description|Result|
  |:--------:|:-----------:|------|
  |Gap Variance| variability of gaps between sorted numbers.| **2-10-5-8** : 1 + gap = 3 => gap = 2, 3 + gap = 13 => gap = 10 ...|
  |MaxGap| Largest interval between combination members (sorted).| **10** : `MAX({2-10-5-8})`|
  |AvgGap| Average of gaps list | **~6.2** : `AVG({2-10-5-8})`|
  |ArithTotal|Total sum of combination's members.| **61** : `SUM({1,3,13,18,26})`|
  |ArithAvg| Average of combination's members.| **12.2** : `AVG({1,3,13,18,26})`|
  |ArithStd| Stardard Deviation of combination's members.| **~9.32** : `STDEV({1,3,13,18,26})`|





---
Made with ❤️, caffeine, and slightly too much Blink-182.
"""