import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import calendar
import tkinter as tk
from tkinter import filedialog, messagebox
import plotly.express as px
from plotly.graph_objs import Scatter, Layout
from tkcalendar import DateEntry

class PokerBankrollManager:
    def __init__(self):
        self.sessions = []
        self.df = pd.DataFrame()

    def load_data_from_csv(self, file_path):
        
        df = pd.read_csv(file_path)
        self.df = df

        print(f"Columns in CSV: {df.columns}")

        
        for index, row in df.iterrows():
            
            if row['Month'].lower() == 'summary':
                continue

            
            session = {
                'start_time': datetime(int(row['Year']), datetime.strptime(row['Month'], "%B").month, 1), 
                'end_time': datetime(int(row['Year']), datetime.strptime(row['Month'], "%B").month, 1),  
                'buy_in': 0,  
                'cash_out': 0,  
                'expenses': 0,  
                'net_profit': row['Result (USD)'],
                'duration': row['Hours Played'],
                'game_type': 'Mixed'  
            }

           
            self.sessions.append(session)

        print(f"Loaded {len(df)} sessions from {file_path}")

    def filter_sessions_by_date(self, start_date, end_date):
        
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)

        
        filtered_df = pd.DataFrame(self.sessions)
        filtered_df = filtered_df[(filtered_df['start_time'] >= start_date) & (filtered_df['end_time'] <= end_date)]
        return filtered_df

    def generate_overview(self, df=None):
        
        df = df if df is not None else pd.DataFrame(self.sessions)

        
        total_buy_in = df['buy_in'].sum()
        total_cash_out = df['cash_out'].sum()
        total_net_profit = df['net_profit'].sum()
        total_duration = df['duration'].sum()
        sessions_count = df.shape[0]
        hourly_rate = total_net_profit / total_duration if total_duration > 0 else 0
        roi = (total_net_profit / total_buy_in * 100) if total_buy_in > 0 else 0
        win_rate = (df['net_profit'] > 0).mean() * 100

       
        advice = self.suggest_strategy(total_net_profit)

        overview_text = (
            f"Bankroll Overview\n"
            f"Total Sessions: {sessions_count}\n"
            f"Total Duration: {total_duration:.1f} hours\n"
            f"Total Buy-In: ${total_buy_in:.2f}\n"
            f"Total Cash-Out: ${total_cash_out:.2f}\n"
            f"Net Profit: ${total_net_profit:.2f}\n"
            f"Hourly Rate: ${hourly_rate:.2f}/hour\n"
            f"ROI: {roi:.2f}%\n"
            f"Win Rate: {win_rate:.2f}%\n"
            f"Advice: {advice}"
        )

        return overview_text

    def suggest_strategy(self, total_net_profit):
        if total_net_profit <= -1000:
            suggestion = "Consider reducing stakes to minimize losses."
        elif total_net_profit > 1000:
            suggestion = "Consider moving up stakes to maximize profits."
        else:
            suggestion = "Maintain current strategy and monitor results."
        return suggestion

    def generate_report(self, df=None, plot_type='line'):
        df = df if df is not None else pd.DataFrame(self.sessions)

        # Ensure datetime columns are in datetime format for resampling
        df['start_time'] = pd.to_datetime(df['start_time'])
        df['end_time'] = pd.to_datetime(df['end_time'])

        # Extract date, week, month and year for reporting
        df['date'] = df['start_time'].dt.date
        df['week'] = df['start_time'].dt.to_period('W').astype(str)
        df['month'] = df['start_time'].dt.to_period('M').astype(str)
        df['year'] = df['start_time'].dt.to_period('Y')

        # Daily summary
        daily_summary = df.groupby('date').agg(total_profit_loss=('net_profit', 'sum')).reset_index()

        # Weekly summary
        weekly_summary = df.groupby('week').agg(total_profit_loss=('net_profit', 'sum')).reset_index()

        # Monthly summary
        monthly_summary = df.groupby('month').agg(total_profit_loss=('net_profit', 'sum')).reset_index()

        # Calculate total profit for the annotation
        total_profit = df['net_profit'].sum()

        if plot_type == 'line':
            self.plot_line_graph(monthly_summary, 'Monthly Profit/Loss Summary', 'month', 'total_profit_loss', total_profit)
        elif plot_type == 'bar':
            self.plot_bar_graph(monthly_summary, 'Monthly Profit/Loss Summary', 'month', 'total_profit_loss')

    def plot_line_graph(self, df, title, x_col, y_col, total_profit=None):
        fig = px.line(df, x=x_col, y=y_col, title=title)

        # Plot total profit 
        if total_profit is not None:
            cumulative_profits = df[y_col].cumsum()
            fig.add_scatter(x=df[x_col], 
                            y=cumulative_profits, 
                            mode='lines+markers+text', 
                            name='Total Profit',
                            line=dict(color='green'),
                            text=[f"${profit:,.2f}" for profit in cumulative_profits],
                            textposition='top center')

        # Annotate monthly profits on the blue line
        fig.add_scatter(x=df[x_col],
                        y=df[y_col],
                        mode='markers+text',
                        name='Monthly Profit',
                        text=[f"${profit:,.2f}" for profit in df[y_col]],
                        textposition='bottom center')

        fig.show()

    def plot_bar_graph(self, df, title, x_col, y_col):
        fig = px.bar(df, x=x_col, y=y_col, title=title)
        fig.show()

class BankrollGUI:
    def __init__(self, root, manager):
        self.manager = manager
        self.root = root
        self.root.title("Poker Bankroll Manager")

        # Set the background color
        self.root.configure(bg='#333333')

        # Load CSV Button
        self.load_button = tk.Button(root, text="Load CSV", command=self.load_csv, bg='#666666', fg='white')
        self.load_button.grid(row=0, column=0, padx=5, pady=5)

        # Date Range
        tk.Label(root, text="Start Date:", bg='#333333', fg='white').grid(row=1, column=0, padx=5, pady=5)
        self.start_date = DateEntry(root)
        self.start_date.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(root, text="End Date:", bg='#333333', fg='white').grid(row=2, column=0, padx=5, pady=5)
        self.end_date = DateEntry(root)
        self.end_date.grid(row=2, column=1, padx=5, pady=5)

        self.filter_button = tk.Button(root, text="Filter by Date", command=self.filter_by_date, bg='#666666', fg='white')
        self.filter_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        # Graph Type Selection
        tk.Label(root, text="Select Graph Type:", bg='#333333', fg='white').grid(row=4, column=0, padx=5, pady=5)
        self.graph_type = tk.StringVar(value='line')
        tk.Radiobutton(root, text="Line", variable=self.graph_type, value='line', bg='#333333', fg='white', selectcolor='#666666').grid(row=4, column=1, padx=5, pady=5)
        tk.Radiobutton(root, text="Bar", variable=self.graph_type, value='bar', bg='#333333', fg='white', selectcolor='#666666').grid(row=4, column=2, padx=5, pady=5)

        # Generate Report Button
        self.generate_report_button = tk.Button(root, text="Generate Report", command=self.generate_report, bg='#666666', fg='white')
        self.generate_report_button.grid(row=5, column=0, columnspan=3, padx=5, pady=5)

        # Output Text Area
        self.output_text = tk.Text(root, height=15, width=50, bg='#d3d3d3', fg='black')
        self.output_text.grid(row=6, column=0, columnspan=3, padx=5, pady=5)

        # Text color toggle
        self.colors = ['green', 'blue', 'cyan', 'orange', 'red']
        self.current_color_index = 0

    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.manager.load_data_from_csv(file_path)
            messagebox.showinfo("Info", f"Loaded data from {file_path}")

    def filter_by_date(self):
        start_date = self.start_date.get()
        end_date = self.end_date.get()
        filtered_df = self.manager.filter_sessions_by_date(start_date, end_date)
        if not filtered_df.empty:
            overview_text = self.manager.generate_overview(filtered_df)
            self.output_text.insert(tk.END, overview_text + "\n", f"color_{self.current_color_index}")
            self.output_text.tag_configure(f"color_{self.current_color_index}", foreground=self.colors[self.current_color_index])
            self.current_color_index = (self.current_color_index + 1) % len(self.colors)
        else:
            self.output_text.insert(tk.END, "No sessions found for the selected date range.\n", f"color_{self.current_color_index}")
            self.output_text.tag_configure(f"color_{self.current_color_index}", foreground=self.colors[self.current_color_index])
            self.current_color_index = (self.current_color_index + 1) % len(self.colors)

    def generate_report(self):
        plot_type = self.graph_type.get()
        start_date = self.start_date.get()
        end_date = self.end_date.get()
        filtered_df = self.manager.filter_sessions_by_date(start_date, end_date)
        self.manager.generate_report(filtered_df, plot_type)

def main():
    manager = PokerBankrollManager()

    # Create GUI
    root = tk.Tk()
    gui = BankrollGUI(root, manager)
    root.mainloop()

if __name__ == "__main__":
    main()
