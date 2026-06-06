import pandas as pd
import google.generativeai as genai
from config import GEMINI_API_KEY
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import uuid
import os
from prophet import Prophet

genai.configure(api_key=GEMINI_API_KEY)


class AnalyticsAgent:
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    def load_file(self, file_path):
        if file_path.endswith(".csv"):
            df = pd.read_csv(file_path)
        elif file_path.endswith(".xlsx"):
            df = pd.read_excel(file_path)
        else:
            raise ValueError("Only CSV and XLSX files are supported")

        df.columns = [col.strip().lower() for col in df.columns]

        if "order_date" in df.columns:
            df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

        if "revenue" not in df.columns:
            if "quantity" in df.columns and "unit_price" in df.columns:
                df["revenue"] = df["quantity"] * df["unit_price"]

        return df

    def top_products(self, df):
        result = (
            df.groupby("product")["revenue"]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )

        return result

    def top_customers(self, df):
        result = (
            df.groupby("customer")["revenue"]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )

        return result

    def region_sales(self, df):
        result = (
            df.groupby("region")["revenue"]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )

        return result

    def monthly_trend(self, df):
        if "order_date" not in df.columns:
            raise ValueError("order_date column is required for monthly trend")

        df["month"] = df["order_date"].dt.to_period("M").astype(str)

        result = (
            df.groupby("month")["revenue"]
            .sum()
            .reset_index()
        )

        return result

    def generate_chart(self, result_df, analysis_type):
        import matplotlib.pyplot as plt
        import uuid
        from pathlib import Path

        charts_dir = Path(__file__).resolve().parent.parent / "data" / "charts"
        charts_dir.mkdir(parents=True, exist_ok=True)

        chart_path = charts_dir / f"{uuid.uuid4()}.png"

        x_col = result_df.columns[0]
        y_col = result_df.columns[1]

        plt.figure(figsize=(8, 5))
        plt.bar(result_df[x_col], result_df[y_col])
        plt.title(analysis_type)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(chart_path)
        plt.close()

        return f"/charts/{chart_path.name}"

    def executive_summary(self, df):
        summary = {
            "total_revenue": float(df["revenue"].sum()),
            "total_orders": int(len(df)),
            "average_order_value": float(df["revenue"].mean()),
            "top_product": df.groupby("product")["revenue"].sum().idxmax()
            if "product" in df.columns else None,
            "top_customer": df.groupby("customer")["revenue"].sum().idxmax()
            if "customer" in df.columns else None,
            "top_region": df.groupby("region")["revenue"].sum().idxmax()
            if "region" in df.columns else None,
        }

        return pd.DataFrame([summary])
    
    def get_dashboard_metrics(self, file_path):

        df = self.load_file(file_path)

        metrics = {
            "total_revenue": float(df["revenue"].sum()),
            "total_orders": int(len(df)),
            "average_order_value": float(df["revenue"].mean())
        }

        top_product = (
            df.groupby("product")["revenue"]
            .sum()
            .idxmax()
        )

        top_customer = (
            df.groupby("customer")["revenue"]
            .sum()
            .idxmax()
        )

        top_region = (
            df.groupby("region")["revenue"]
            .sum()
            .idxmax()
        )

        metrics["top_product"] = top_product
        metrics["top_customer"] = top_customer
        metrics["top_region"] = top_region

        return metrics


    def revenue_forecast(self, df, periods=3):
        from prophet import Prophet

        if "order_date" not in df.columns:
            raise ValueError("order_date column is required for forecasting")

        if "revenue" not in df.columns:
            raise ValueError("revenue column is required for forecasting")

        df = df.copy()

        df["order_date"] = pd.to_datetime(
            df["order_date"],
            errors="coerce"
        )

        df = df.dropna(subset=["order_date"])

        monthly_df = (
            df.set_index("order_date")
            .resample("ME")["revenue"]
            .sum()
            .reset_index()
        )

        monthly_df.columns = ["ds", "y"]

        if len(monthly_df) < 2:
            raise ValueError(
                "At least 2 months of sales data are required for forecasting"
            )

        model = Prophet(
            yearly_seasonality=False,
            weekly_seasonality=False,
            daily_seasonality=False
        )

        model.fit(monthly_df)

        future = model.make_future_dataframe(
            periods=periods,
            freq="ME"
        )

        forecast = model.predict(future)

        result = forecast[
            ["ds", "yhat", "yhat_lower", "yhat_upper"]
        ].tail(periods)

        result["ds"] = result["ds"].dt.strftime("%Y-%m-%d")

        result["yhat"] = result["yhat"].round(2)
        result["yhat_lower"] = result["yhat_lower"].round(2)
        result["yhat_upper"] = result["yhat_upper"].round(2)

        return result




    def route_question(self, question):
        q = question.lower()

        # NEW
        if "forecast" in q:
            return "forecast"

        if "predict" in q:
            return "forecast"

        if "future" in q:
            return "forecast"

        # Existing
        if "product" in q or "products" in q:
            return "top_products"

        if "customer" in q or "customers" in q:
            return "top_customers"

        if "region" in q or "regions" in q:
            return "region_sales"

        if "month" in q or "monthly" in q or "trend" in q:
            return "monthly_trend"

        return "executive_summary"
    def generate_insight(self, question, analysis_type, result_df):
        result_text = result_df.to_string(index=False)

        prompt = f"""
You are a business data analyst.

The calculations below were already performed using Pandas.
Do not recalculate numbers. Use these exact results.

Question:
{question}

Analysis Type:
{analysis_type}

Pandas Result:
{result_text}

Write:
1. Direct answer
2. Key insights
3. Business recommendation
"""

        response = self.model.generate_content(prompt)

        return response.text

    def analyze(self, file_path, question):
        df = self.load_file(file_path)

        analysis_type = self.route_question(question)

        if analysis_type == "top_products":
            result_df = self.top_products(df)

        elif analysis_type == "top_customers":
            result_df = self.top_customers(df)

        elif analysis_type == "region_sales":
            result_df = self.region_sales(df)

        elif analysis_type == "monthly_trend":
            result_df = self.monthly_trend(df)

        elif analysis_type == "forecast":
            result_df = self.revenue_forecast(df)

        else:
            result_df = self.executive_summary(df)

        answer = self.generate_insight(
    question=question,
    analysis_type=analysis_type,
    result_df=result_df
)

        chart_path = self.generate_chart(
            result_df=result_df,
            analysis_type=analysis_type
        )

        return {
            "answer": answer,
            "analysis_type": analysis_type,
            "table": result_df.to_dict(orient="records"),
            "chart_path": chart_path,
            "columns": list(df.columns),
            "rows": len(df)
        }



    def revenue_forecast(self, df, periods=3):

        if "order_date" not in df.columns:
            raise ValueError("order_date column required")

        forecast_df = (
            df.groupby("order_date")["revenue"]
            .sum()
            .reset_index()
        )

        forecast_df.columns = ["ds", "y"]

        model = Prophet()

        model.fit(forecast_df)

        future = model.make_future_dataframe(
            periods=periods,
            freq="M"
        )

        forecast = model.predict(future)

        result = forecast[
            ["ds", "yhat", "yhat_lower", "yhat_upper"]
        ].tail(periods)

        return result


    def get_dashboard_data(self, file_path):

        df = self.load_file(file_path)

        product_sales = (
            df.groupby("product")["revenue"]
            .sum()
            .reset_index()
        )

        region_sales = (
            df.groupby("region")["revenue"]
            .sum()
            .reset_index()
        )

        customer_sales = (
            df.groupby("customer")["revenue"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )

        monthly_sales = (
            df.groupby(
                pd.to_datetime(
                    df["order_date"]
                ).dt.to_period("M")
            )["revenue"]
            .sum()
            .reset_index()
        )

        monthly_sales["order_date"] = (
            monthly_sales["order_date"]
            .astype(str)
        )

        return {
            "products": product_sales.to_dict("records"),
            "regions": region_sales.to_dict("records"),
            "customers": customer_sales.to_dict("records"),
            "monthly": monthly_sales.to_dict("records")
        }