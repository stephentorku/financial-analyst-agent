import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sqlite3

def generate_loan_data(n_records=1000):
    """Generate synthetic loan performance data"""
    np.random.seed(42)
    
    start_date = datetime(2022, 1, 1)
    dates = [start_date + timedelta(days=x) for x in range(n_records)]
    
    loan_types = ['Personal', 'Mortgage', 'Auto', 'Small Business', 'Credit Card']
    provinces = ['ON', 'BC', 'AB', 'QC', 'MB', 'SK', 'NS', 'NB']
    
    data = {
        'loan_id': [f'L{i:06d}' for i in range(n_records)],
        'application_date': dates,
        'loan_type': np.random.choice(loan_types, n_records),
        'amount': np.random.uniform(5000, 500000, n_records).round(2),
        'interest_rate': np.random.uniform(2.5, 8.5, n_records).round(2),
        'term_months': np.random.choice([12, 24, 36, 60, 120, 240], n_records),
        'credit_score': np.random.randint(550, 850, n_records),
        'province': np.random.choice(provinces, n_records),
        'customer_age': np.random.randint(18, 75, n_records),
        'income': np.random.uniform(30000, 200000, n_records).round(2),
        'employment_status': np.random.choice(['Full-time', 'Part-time', 'Self-employed', 'Retired'], n_records),
        'defaulted': np.random.choice([0, 1], n_records, p=[0.92, 0.08]),  # 8% default rate
        'days_past_due': np.random.choice([0, 30, 60, 90, 120], n_records, p=[0.85, 0.08, 0.04, 0.02, 0.01])
    }
    
    df = pd.DataFrame(data)
    
    # Add some realistic correlations
    # Higher credit score = lower default rate
    df.loc[df['credit_score'] > 750, 'defaulted'] = np.random.choice([0, 1], sum(df['credit_score'] > 750), p=[0.98, 0.02])
    
    # Add quarterly trends (Q2 2024 spike)
    q2_2024_mask = (df['application_date'] >= '2024-04-01') & (df['application_date'] < '2024-07-01')
    df.loc[q2_2024_mask, 'defaulted'] = np.random.choice([0, 1], sum(q2_2024_mask), p=[0.85, 0.15])
    
    return df

def generate_transaction_data(n_records=5000):
    """Generate synthetic transaction data"""
    np.random.seed(43)
    
    start_date = datetime(2023, 1, 1)
    dates = [start_date + timedelta(hours=x) for x in range(n_records)]
    
    transaction_types = ['Purchase', 'Withdrawal', 'Transfer', 'Payment', 'Deposit']
    merchants = ['Amazon', 'Walmart', 'Gas Station', 'Restaurant', 'Grocery Store', 'Online Retail']
    
    data = {
        'transaction_id': [f'T{i:08d}' for i in range(n_records)],
        'timestamp': dates,
        'customer_id': [f'C{np.random.randint(1, 5000):05d}' for _ in range(n_records)],
        'type': np.random.choice(transaction_types, n_records),
        'amount': np.random.uniform(5, 5000, n_records).round(2),
        'merchant': np.random.choice(merchants, n_records),
        'is_fraud': np.random.choice([0, 1], n_records, p=[0.997, 0.003])  # 0.3% fraud rate
    }
    
    return pd.DataFrame(data)

def create_database():
    """Create SQLite database with all tables"""
    conn = sqlite3.connect('app/data/structured/banking.db')
    
    # Generate and save data
    loans_df = generate_loan_data()
    transactions_df = generate_transaction_data()
    
    loans_df.to_sql('loans', conn, if_exists='replace', index=False)
    transactions_df.to_sql('transactions', conn, if_exists='replace', index=False)
    
    # Also save as CSV for flexibility
    loans_df.to_csv('app/data/structured/loans.csv', index=False)
    transactions_df.to_csv('app/data/structured/transactions.csv', index=False)
    
    print(f"✅ Generated {len(loans_df)} loan records")
    print(f"✅ Generated {len(transactions_df)} transaction records")
    print(f"✅ Database created at app/data/structured/banking.db")
    
    conn.close()

if __name__ == "__main__":
    create_database()