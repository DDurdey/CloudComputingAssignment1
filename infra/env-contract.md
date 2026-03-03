# Environment Contract (Phase 2)

## Backend Environment Variables (Azure Function App Settings)

- AZURE_STORAGE_CONNECTION_STRING = (real Azure connection string)
- BLOB_CONTAINER = datasets
- BLOB_NAME = All_Diets.csv

---

## API Endpoint

GET /api/diets

---

## Response Format

```json
{
  "data": [
    {
      "Diet_type": "keto",
      "Protein(g)": 101.2,
      "Carbs(g)": 58.0,
      "Fat(g)": 153.1
    }
  ],
  "meta": {
    "recordCount": 1234,
    "executionMs": 87
  }
}