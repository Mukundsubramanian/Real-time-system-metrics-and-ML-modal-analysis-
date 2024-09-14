from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

# Load CSV data
df = pd.read_csv("dataset.csv")

@app.route('/')
def index():
    # Convert DataFrame to HTML table
    return render_template('index1.html', tables=[df.to_html(classes='data', index=False)], titles=df.columns.values)

if __name__ == '__main__':
    app.run(debug=True)
