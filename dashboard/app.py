import sqlite3
import dash
import dash_table
import dash_html_components as html

app = dash.Dash(__name__)

def fetch_logs():
    conn = sqlite3.connect("../honeypot_logs.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM attack_logs ORDER BY timestamp DESC LIMIT 50")
    data = cur.fetchall()
    conn.close()
    return data

app.layout = html.Div([
    html.H1("SSH Honeypot Attack Logs"),
    dash_table.DataTable(
        columns=[
            {"name": "ID", "id": 0},
            {"name": "IP Address", "id": 1},
            {"name": "Username", "id": 2},
            {"name": "Password", "id": 3},
            {"name": "Timestamp", "id": 4}
        ],
        data=[{i: row[i] for i in range(len(row))} for row in fetch_logs()]
    )
])

if __name__ == "__main__":
    app.run_server(debug=True)
