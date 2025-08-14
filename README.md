# **OKShip - Delivery Delay Prediction App**

Predict and monitor shipment delays using a simple Streamlit app with two pages: **EDA** (exploratory analysis) and **Prediction**. The project ships with raw & cleaned data, notebooks, and a trained model (pickle) you can plug in to get instant inference.

---

Tableau URL for Visualizations: [Tableau Dashboard](https://public.tableau.com/app/profile/yunido.baheramsyah/viz/LateShipmentAnalysis/Dashboard2?publish=yes)

---

## Key Features
- **EDA Dashboard**: Interactive charts (bar, line, pie) to inspect class balance, late rate by warehouse, mode of shipment, product importance, weight bins, discount levels, and customer-care calls.  
- **Prediction Form**: Input customer/order attributes and get a **delay vs. on‑time** prediction backed by a trained model.
- **Notebooks**: End‑to‑end workflow documentation in Jupyter (`final_project.ipynb`, `deep_learning.ipynb`).

---

## 📁 Project Structure
```
.
├── final_project.ipynb
├── deep_learning.ipynb
├── raw_data.csv
├── cleaned_data.csv
└── src/
    └── my_sequential_model.keras   # expected model path (see Notes)
    └── eda.py
    └── prediction.py
    └── streamlit_app.py
```
> If `src/` does not exist yet, create it and place your model there, or adjust the path in `prediction.py`.

---

## How It Works

### 1) EDA Page
The EDA page loads `cleaned_data.csv` and renders eight main visuals:
1. **Delivery Status (Class Balance)** — late vs. on‑time distribution.  
2. **Late Rate by Warehouse** — horizontal bar ranking each `warehouse_block`.  
3. **Late Rate by Mode of Shipment** — vertical bar for `Road`, `Ship`, `Flight`.  
4. **Share of Late by Mode of Shipment** — pie chart of late counts by mode.  
5. **Late Rate by Product Importance** — `high/medium/low` comparison.  
6. **Late Rate by Weight** — binned line (configurable bin size in sidebar).  
7. **Late Rate by Discount** — binned line (5-point bins).  
8. **Late Rate by Customer-Care Calls** — line across call counts.

**Target handling**: when a column like `Reached.on.Time_Y.N` exists (1 = on-time, 0 = late), the app derives `Late = 1 - on_time` and computes rates per group.

### 2) Prediction Page
A Streamlit form collects the following fields and returns a model prediction:
- `warehouse_block` (categorical)
- `mode_of_shipment` (categorical: Road/Ship/Flight)
- `customer_care_calls` (int)
- `customer_rating` (0–10)
- `cost_of_the_product` (float)
- `prior_purchases` (int)
- `product_importance` (categorical: high/medium/low)
- `gender` (categorical)
- `discount_offered` (0–100)
- `weight_in_gms` (int)

On submit, inputs are assembled into a single-row DataFrame and passed to the loaded model to output the predicted status.

---

## Quick Start


### 1) Data
Dataset URL: https://www.kaggle.com/datasets/prachi13/customer-analytics

> **Important:** In the current scripts, some file paths are **absolute Windows paths**. Change them to **relative paths** for portability.



### 2) Model file
Place your trained model at:
```
src/my_sequential_model.keras
```
If the file is missing, the Prediction page will display a friendly error instead of crashing.

### 3) Run the app
```bash
streamlit run streamlit_app.py
```

Open the provided local URL in your browser, then use the left sidebar to switch between **EDA** and **Prediction** pages.

---

## 📓 Notebooks
- **`final_project.ipynb`** — Project E2E: data understanding, cleaning, feature engineering, model training/evaluation.  
- **`deep_learning.ipynb`** — Deep learning experiments and evaluation details.

> Use `jupyter lab` or `jupyter notebook` to open, or VS Code with the Python extension.

---

## Implementation Notes
- **App shell & navigation**: `streamlit_app.py` creates a sidebar selector between **EDA** and **Prediction** pages.  
- **EDA logic**: `eda.py` reads the cleaned dataset and computes late rates across multiple dimensions; charts are built with Plotly Express.  
- **Inference**: `prediction.py` loads a pickled model from `src/my_sequential_model.keras`; if missing, Streamlit shows an error message. Inputs from the form are gathered, converted to a DataFrame, and sent to `.predict(...)`.

---

## Requirements (summary)
- altair
- pandas
- numpy
- matplotlib
- seaborn
- plotly
- pathlib
- streamlit

---

## Stacks

- Python
- Streamlit
- Matplotlib
- Tableau
- TensorFlow/Keras
- Pandas
- NumPy
- Scikit-learn
- Plotly

---

## Troubleshooting
- **File path errors**: Update absolute Windows paths in `eda.py`/`prediction.py` to relative paths (see “Quick Start > Data”).  
- **Model not found**: Ensure `src/my_sequential_model.keras` exists. The app will show an error if it doesn’t.  
- **Category mismatches**: Ensure categorical values (e.g., `mode_of_shipment`, `product_importance`) match those seen during training, or apply the same preprocessing pipeline.

---

## Reference
- [Kaggle - E-Commerce Shipping Data](https://www.kaggle.com/datasets/prachi13/customer-analytics)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Huggingface](https://huggingface.co/spaces/yunidobaheramsyah/delivery_predictor)


