# Sales Analytics Dashboard - Quick Start Guide

## 📥 Dataset Options

### Option 1: Use Provided Sample Data (Recommended for Quick Start)
The project includes `data/sample_sales_data.csv` with 138 realistic sales records.

### Option 2: Download Real Kaggle Dataset
For more extensive analysis, download one of these datasets:

**Recommended Kaggle Datasets:**
1. **"Sample - Superstore"** by Tableau
   - URL: https://www.kaggle.com/datasets/rohitsahoo/sales-forecasting
   - Contains: Orders, Sales, Profit, Region, Category
   
2. **"Global Superstore Dataset"**
   - URL: https://www.kaggle.com/datasets/apoorvaappz/global-super-store-dataset
   - Contains: Comprehensive retail sales data

**How to use Kaggle data:**
1. Download CSV file from Kaggle
2. Place it in the `data/` folder
3. Update `DATA_FILE` variable in [sales_analysis.py](sales_analysis.py) (line 14):
   ```python
   DATA_FILE = 'data/your_kaggle_file.csv'
   ```

## 🚀 Installation & Execution

```bash
# Install dependencies
pip install -r requirements.txt

# Run the analysis
python sales_analysis.py
```

## 📊 Expected Output

After running, check the `outputs/` folder for:
- Interactive HTML visualizations
- Console output with PM insights and recommendations

---

**Tip**: Start with the sample data to verify everything works, then substitute with Kaggle datasets for deeper analysis!
