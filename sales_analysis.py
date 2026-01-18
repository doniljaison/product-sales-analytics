"""
Sales Analytics Dashboard - Data Analysis Script
Analyzes global sales data to identify revenue optimization opportunities
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime

def load_and_clean_data(file_path):
    """Load and clean the sales data"""
    print("📊 Loading data...")
    
    # Load data with latin-1 encoding for Global Superstore
    df = pd.read_csv(file_path, encoding='latin-1')
    
    # Standardize column names for Global Superstore format
    column_mapping = {
        'Order Date': 'Date',
        'Sales': 'Sales_Amount',
        'Category': 'Product_Category',
        'Customer ID': 'Customer_ID'
    }
    
    df.rename(columns=column_mapping, inplace=True)
    
    # Convert date column
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Handle missing values
    numeric_columns = ['Sales_Amount', 'Profit', 'Quantity']
    for col in numeric_columns:
        if col in df.columns:
            df[col].fillna(df[col].median(), inplace=True)
    
    print(f"✅ Loaded {len(df)} transactions")
    return df

def calculate_pm_metrics(df):
    """Calculate key Product Manager metrics"""
    print("📈 Calculating PM metrics...")
    
    # Monthly Recurring Revenue (MRR) Growth
    df['Month'] = df['Date'].dt.to_period('M')
    monthly_revenue = df.groupby('Month')['Sales_Amount'].sum()
    mrr_growth = monthly_revenue.pct_change().mean() * 100
    
    # Customer Acquisition Cost (CAC) trend
    monthly_customers = df.groupby('Month')['Customer_ID'].nunique()
    monthly_cost = df.groupby('Month')['Sales_Amount'].sum()
    cac = (monthly_cost / monthly_customers).mean()
    
    # Regional profit margins
    regional_margins = df.groupby('Region').agg({
        'Sales_Amount': 'sum',
        'Profit': 'sum'
    })
    regional_margins['Margin_%'] = (regional_margins['Profit'] / regional_margins['Sales_Amount']) * 100
    
    # Category performance
    category_performance = df.groupby('Product_Category').agg({
        'Sales_Amount': 'sum',
        'Profit': 'sum',
        'Quantity': 'sum'
    })
    
    metrics = {
        'mrr_growth': mrr_growth,
        'cac': cac,
        'regional_margins': regional_margins,
        'category_performance': category_performance,
        'monthly_revenue': monthly_revenue
    }
    
    print(f"✅ MRR Growth: {mrr_growth:.2f}%")
    return metrics

def create_visualizations(df, metrics):
    """Create interactive Plotly visualizations"""
    print("🎨 Creating visualizations...")
    
    # 1. Sales Trend Over Time
    monthly_data = df.groupby(df['Date'].dt.to_period('M')).agg({
        'Sales_Amount': 'sum'
    }).reset_index()
    monthly_data['Date'] = monthly_data['Date'].dt.to_timestamp()
    
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=monthly_data['Date'],
        y=monthly_data['Sales_Amount'],
        mode='lines+markers',
        name='Monthly Revenue',
        line=dict(color='#3b82f6', width=3),
        marker=dict(size=8)
    ))
    fig_trend.update_layout(
        title='Sales Trend Analysis - Monthly Revenue',
        xaxis_title='Month',
        yaxis_title='Revenue ($)',
        template='plotly_white',
        hovermode='x unified'
    )
    fig_trend.write_html('docs/reports/sales_trend.html')
    
    # 2. Regional Performance
    regional_data = metrics['regional_margins'].reset_index()
    fig_region = go.Figure()
    fig_region.add_trace(go.Bar(
        x=regional_data['Region'],
        y=regional_data['Margin_%'],
        marker_color='#8b5cf6',
        text=regional_data['Margin_%'].round(2),
        textposition='outside'
    ))
    fig_region.update_layout(
        title='Regional Performance - Profit Margins',
        xaxis_title='Region',
        yaxis_title='Profit Margin (%)',
        template='plotly_white'
    )
    fig_region.write_html('docs/reports/regional_performance.html')
    
    # 3. Category Distribution
    category_data = metrics['category_performance']
    fig_category = go.Figure(data=[go.Pie(
        labels=category_data.index,
        values=category_data['Profit'],
        hole=0.4,
        marker_colors=['#3b82f6', '#8b5cf6', '#ec4899']
    )])
    fig_category.update_layout(
        title='Category Profit Distribution',
        template='plotly_white'
    )
    fig_category.write_html('docs/reports/category_distribution.html')
    
    print("✅ Created 3 visualization reports")

def analyze_customer_segments(df):
    """Analyze customer segments by frequency and value"""
    print("👥 Analyzing customer segments...")
    
    # Customer frequency analysis
    customer_stats = df.groupby('Customer_ID').agg({
        'Sales_Amount': 'sum',
        'Profit': 'sum',
        'Date': 'count'
    }).rename(columns={'Date': 'Order_Count'})
    
    # Segment by frequency (top 20% = high frequency)
    frequency_threshold = customer_stats['Order_Count'].quantile(0.8)
    customer_stats['Segment'] = customer_stats['Order_Count'].apply(
        lambda x: 'High Frequency' if x >= frequency_threshold else 'Standard'
    )
    
    # Segment statistics
    segment_stats = customer_stats.groupby('Segment').agg({
        'Sales_Amount': ['sum', 'mean', 'count'],
        'Profit': 'sum',
        'Order_Count': 'mean'
    }).round(2)
    
    # Calculate profit margins by segment
    segment_stats['Margin_%'] = (
        segment_stats[('Profit', 'sum')] / segment_stats[('Sales_Amount', 'sum')]
    ) * 100
    
    print(f"✅ Segmented {len(customer_stats)} customers")
    print(f"   High Frequency: {len(customer_stats[customer_stats['Segment'] == 'High Frequency'])} customers")
    print(f"   Standard: {len(customer_stats[customer_stats['Segment'] == 'Standard'])} customers")
    
    return customer_stats, segment_stats

def create_customer_visualization(customer_stats, segment_stats):
    """Create customer segmentation visualizations"""
    print("🎨 Creating customer segmentation dashboard...")
    
    # Create subplot with 4 charts
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Revenue by Segment', 'Customer Distribution', 
                       'Top 5 Products by Segment', 'Order Frequency vs Revenue'),
        specs=[[{'type': 'pie'}, {'type': 'bar'}],
               [{'type': 'bar'}, {'type': 'scatter'}]]
    )
    
    # 1. Revenue distribution pie chart
    if len(segment_stats) >= 2:
        segment_revenue = segment_stats[('Sales_Amount', 'sum')]
        fig.add_trace(go.Pie(
            labels=segment_revenue.index,
            values=segment_revenue.values,
            hole=0.3
        ), row=1, col=1)
        
        # 2. Customer count bar chart
        segment_count = segment_stats[('Sales_Amount', 'count')]
        fig.add_trace(go.Bar(
            x=segment_count.index,
            y=segment_count.values,
            marker_color=['#3b82f6', '#8b5cf6']
        ), row=1, col=2)
        
        # 3. Average revenue per customer
        avg_revenue = segment_stats[('Sales_Amount', 'mean')]
        fig.add_trace(go.Bar(
            x=avg_revenue.index,
            y=avg_revenue.values,
            marker_color=['#ec4899', '#f59e0b']
        ), row=2, col=1)
        
        # 4. Scatter: Order count vs Revenue
        fig.add_trace(go.Scatter(
            x=customer_stats['Order_Count'],
            y=customer_stats['Sales_Amount'],
            mode='markers',
            marker=dict(
                color=customer_stats['Segment'].map({'High Frequency': '#3b82f6', 'Standard': '#8b5cf6'}),
                size=8
            )
        ), row=2, col=2)
    
    fig.update_layout(
        title_text='Customer Segmentation Analysis Dashboard',
        showlegend=False,
        height=800
    )
    
    fig.write_html('docs/reports/customer_segments.html')
    print("✅ Created customer segmentation dashboard")

def generate_pm_insights(df, metrics, customer_stats, segment_stats):
    """Generate Product Manager insights and recommendations"""
    print("\n" + "="*80)
    print("📊 PRODUCT MANAGER INSIGHTS")
    print("="*80 + "\n")
    
    # Key metrics summary
    print("1. BUSINESS HEALTH METRICS")
    print(f"   • MRR Growth Rate: {metrics['mrr_growth']:.2f}%")
    print(f"   • Total Profit: ${metrics['category_performance']['Profit'].sum():,.0f}")
    print(f"   • Average CAC: ${metrics['cac']:.2f}")
    
    # Regional insights
    print("\n2. REGIONAL PERFORMANCE")
    top_region = metrics['regional_margins']['Margin_%'].idxmax()
    worst_region = metrics['regional_margins']['Margin_%'].idxmin()
    print(f"   • Best Region: {top_region} ({metrics['regional_margins'].loc[top_region, 'Margin_%']:.2f}% margin)")
    print(f"   • Needs Attention: {worst_region} ({metrics['regional_margins'].loc[worst_region, 'Margin_%']:.2f}% margin)")
    
    # Customer segment insights
    print("\n3. CUSTOMER SEGMENTATION")
    if len(segment_stats) >= 2:
        high_freq_revenue = segment_stats.loc['High Frequency', ('Sales_Amount', 'sum')]
        total_revenue = segment_stats[('Sales_Amount', 'sum')].sum()
        revenue_pct = (high_freq_revenue / total_revenue) * 100
        
        print(f"   • Power Users (Top 20%): Drive {revenue_pct:.1f}% of revenue")
        print(f"   • Avg Revenue per Power User: ${segment_stats.loc['High Frequency', ('Sales_Amount', 'mean')]:,.0f}")
        print(f"   • Avg Revenue per Standard User: ${segment_stats.loc['Standard', ('Sales_Amount', 'mean')]:,.0f}")
    
    # Category insights
    print("\n4. PRODUCT CATEGORY PERFORMANCE")
    top_category = metrics['category_performance']['Profit'].idxmax()
    print(f"   • Top Category: {top_category} (${metrics['category_performance'].loc[top_category, 'Profit']:,.0f} profit)")
    
    print("\n" + "="*80)
    print("✅ Analysis complete! Check the 'docs/reports/' folder for visualizations")
    print("="*80 + "\n")

def main():
    """Main execution function"""
    
    # File path
    data_file = 'data/Global_Superstore2.csv'
    
    try:
        # Load and clean data
        df = load_and_clean_data(data_file)
        
        # Calculate metrics
        metrics = calculate_pm_metrics(df)
        
        # Create visualizations
        create_visualizations(df, metrics)
        
        # Customer segmentation analysis
        customer_stats, segment_stats = analyze_customer_segments(df)
        create_customer_visualization(customer_stats, segment_stats)
        
        # Generate insights
        generate_pm_insights(df, metrics, customer_stats, segment_stats)
        
    except FileNotFoundError:
        print(f"\n❌ Error: Could not find {data_file}")
        print("📁 Please place your dataset in the 'data/' folder")
        print("   Expected file: data/Global_Superstore2.csv")
        print("\n")
    except Exception as e:
        print(f"\n❌ Error occurred: {str(e)}\n")

if __name__ == "__main__":
    main()
