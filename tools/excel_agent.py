import pandas as pd
import numpy as np

class ExcelAgent:
    def __init__(self, df):
        self.raw_df = df
        self.df = self._clean_data(df)
        self.schema = self._analyze_schema()

    def _clean_data(self,df):
        df = df.copy
        
        df.columns = df.columns.srt.strip().str.lower()
        
        for col in df.columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                df[col] = df[col].fillna(df[col].median())
            else:
                df[col]=df[col].fillna("unknown")
                
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors = "coerce")
        
        return df
    def _analyze_schema(self):
        schema = {}
        for col in self.df.columns:
            
            if pd.api.types.is_numeric_dtype(self.df[col]):
                schema[col] = "numeric"
                
            elif self.df[col].nunique()<20:
                schema[col] = "categorical"
                
            else:
                schema[col]= "text"
                
        return schema
    
    def summary(self):
        report = []
        report.append("📊 DATASET OVERVIEW")
        report.append(f"Rows: {len(self.df)}, Columns: {len(self.df.columns)}\n")
        
        for col, typ in self.schema.items():
            if typ == "numeric":
                report.append(f"🔢 {col} (Numeric) - Mean: {self.df[col].mean():.2f}\n,Max= {self.df[col].max():.2f}\n,Min= {self.df[col].min():.2f}\n,Median: {self.df[col].median():.2f}\n, Std: {self.df[col].std():.2f}")
                
        for col, typ in self.schema.items():
            if typ == "categorical":
                report.append(f"📂 {col} (Categorical) - Unique Values: {self.df[col].nunique()}\n,Top 5: {self.df[col].value_counts().head().to_dict()}")
        
        return "\n".join(report)

    
    def smart_query(self, question, llm_func):

            schema_desc = "\n".join(
                [f"{k}: {v}" for k, v in self.schema.items()]
            )

            prompt = f"""
    You are a data analyst.

    DataFrame name: df

    Schema:
    {schema_desc}

    IMPORTANT:
    - Return ONLY valid Python pandas code
    - No explanation
    - Handle missing values safely

    Question:
    {question}
    """

            code = llm_func(prompt)

            try:
                # ✅ safe eval (restricted scope)
                result = eval(
                    code,
                    {"__builtins__": {}},
                    {"df": self.df, "pd": pd, "np": np}
                )
                return str(result)

            except Exception as e:
                return f"Execution failed: {e}"

    # ----------------------------------
    # ✅ QUERY SUGGESTIONS
    # ----------------------------------
    def suggest_questions(self):
        suggestions = []

        numeric_cols = [c for c, t in self.schema.items() if t == "numeric"]
        cat_cols = [c for c, t in self.schema.items() if t == "categorical"]

        if numeric_cols:
            suggestions.append(f"average of {numeric_cols[0]}")
            suggestions.append(f"top values in {numeric_cols[0]}")

        if len(numeric_cols) >= 2:
            suggestions.append(
                f"correlation between {numeric_cols[0]} and {numeric_cols[1]}"
            )

        if cat_cols and numeric_cols:
            suggestions.append(
                f"average {numeric_cols[0]} by {cat_cols[0]}"
            )

        return suggestions
