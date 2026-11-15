# PlantCare AI - Comprehensive Model Evaluation Report

**Evaluated Model:** `plant_disease_model_best.keras`  
**Test Set Samples:** 126  

## Overall Performance Summary

- **Accuracy:** 14.29%
- **Macro Precision:** 0.0213
- **Macro Recall:** 0.1429
- **Macro F1-Score:** 0.0369
- **Weighted F1-Score:** 0.0369

## Classification Report

| Class Name | Precision | Recall | F1-Score | Support |
| :--- | :---: | :---: | :---: | :---: |
| `Apple___Apple_scab` | 0.0 | 0.0 | 0.0 | 9 |
| `Apple___Black_rot` | 0.0 | 0.0 | 0.0 | 9 |
| `Apple___healthy` | 0.0 | 0.0 | 0.0 | 9 |
| `Corn___Common_rust` | 0.0 | 0.0 | 0.0 | 9 |
| `Corn___Northern_Leaf_Blight` | 0.0 | 0.0 | 0.0 | 9 |
| `Corn___healthy` | 0.0 | 0.0 | 0.0 | 9 |
| `Grape___Black_rot` | 0.0 | 0.0 | 0.0 | 9 |
| `Grape___healthy` | 0.0 | 0.0 | 0.0 | 9 |
| `Potato___Early_blight` | 0.0 | 0.0 | 0.0 | 9 |
| `Potato___Late_blight` | 0.0 | 0.0 | 0.0 | 9 |
| `Potato___healthy` | 0.18 | 1.0 | 0.3051 | 9 |
| `Tomato___Early_blight` | 0.0 | 0.0 | 0.0 | 9 |
| `Tomato___Late_blight` | 0.1184 | 1.0 | 0.2118 | 9 |
| `Tomato___healthy` | 0.0 | 0.0 | 0.0 | 9 |
| `macro avg` | 0.0213 | 0.1429 | 0.0369 | 126 |
| `weighted avg` | 0.0213 | 0.1429 | 0.0369 | 126 |

## Confusion Matrix Artifact

Saved to: `ml-model/models/confusion_matrix.png`
