import dash
from dash import Dash, html, dcc, Input, Output

# Temporary Dash app to generate asset URL
_tmp = Dash(__name__)
CUSTOM_CSS = _tmp.get_asset_url("custom.css")

# Main Dash app with external stylesheet
app = Dash(__name__, external_stylesheets=[CUSTOM_CSS], suppress_callback_exceptions=True)


def overview_layout():
    return html.Div(
        id="overview-content",
        children=[
            html.Div(
                id="stats-panels-container",
                children=[
                    html.Div(
                        id="card-access",
                        className="stat-card",
                        children=[
                            html.H3("Access Events", className="card-title"),
                            html.H4("2,161", className="card-value"),
                            html.Div("21.01.2025 – 21.01.2025", className="card-subtext"),
                        ],
                    ),
                    html.Div(
                        id="card-device",
                        className="stat-card",
                        children=[
                            html.H3("Device Analytics", className="card-title"),
                            html.H4("Total: 4 devices", className="card-value"),
                            html.Div("Access Granted: 432", className="card-subtext"),
                        ],
                    ),
                    html.Div(
                        id="card-peak",
                        className="stat-card",
                        children=[
                            html.H3("Peak Activity", className="card-title"),
                            html.H4("Peak: 9:00", className="card-value"),
                            html.Div("Busiest: Tuesday", className="card-subtext"),
                        ],
                    ),
                ],
            )
        ],
    )


def advanced_layout():
    return html.Div(
        id="advanced-content",
        children=[
            html.Div(
                id="stats-panels-container",
                children=[
                    html.Div(
                        id="card-traffic",
                        className="stat-card",
                        children=[
                            html.H3("Traffic Pattern", className="card-title"),
                            dcc.Graph(id="graph-traffic"),
                        ],
                    ),
                    html.Div(
                        id="card-security-score",
                        className="stat-card",
                        children=[
                            html.H3("Security Score", className="card-title"),
                            dcc.Graph(id="graph-security-score"),
                        ],
                    ),
                    html.Div(
                        id="card-usage",
                        className="stat-card",
                        children=[
                            html.H3("Usage Efficiency", className="card-title"),
                            dcc.Graph(id="graph-usage"),
                        ],
                    ),
                    html.Div(
                        id="card-anomaly",
                        className="stat-card",
                        children=[
                            html.H3("Anomaly Detection", className="card-title"),
                            dcc.Graph(id="graph-anomaly"),
                        ],
                    ),
                ],
            )
        ],
    )


def export_layout():
    return html.Div(
        id="export-content",
        children=[
            html.Div(
                id="export-buttons",
                children=[
                    html.Button("\ud83d\udcca Export Stats CSV", id="export-csv", className="dash-button"),
                    html.Button("\ud83d\udcc9 Download Charts", id="download-charts", className="dash-button"),
                    html.Button("\ud83e\uddfe Generate Report", id="generate-report", className="dash-button"),
                    html.Button("\ud83d\udd04 Refresh Data", id="refresh-data", className="dash-button"),
                ],
            )
        ],
    )


def create_main_layout(app_instance: Dash) -> html.Div:
    return html.Div(
        id="app-container",
        children=[
            # ─────── Dashboard Header ───────
            html.Div(
                id="dashboard-header",
                children=[
                    html.Div(
                        children=[
                            html.Img(src=app_instance.get_asset_url("logo.png"), style={"height": "40px"}),
                            html.Span(" Enhanced Analytics Dashboard", style={"fontSize": "24px", "fontWeight": "700", "marginLeft": "10px"}),
                        ],
                        style={"display": "flex", "alignItems": "center"},
                    ),
                    html.Button("Advanced View \u23F7", id="advanced-view-button", n_clicks=0),
                ],
            ),

            # ─────── Top Row: Upload + Chart Controls ───────
            html.Div(
                id="top-row",
                children=[
                    html.Div(
                        id="upload-section",
                        className="card",
                        children=[
                            html.Div(
                                className="upload-box",
                                children=[
                                    html.I(className="fa fa-upload fa-2x", style={"marginBottom": "10px", "color": "var(--color-text-secondary)"}),
                                    html.Div("Drop your CSV or JSON file here", style={"fontSize": "18px", "fontWeight": "500", "marginBottom": "5px"}),
                                    html.Div("or click to browse", style={"fontSize": "14px", "color": "var(--color-text-tertiary)"}),
                                ],
                            )
                        ],
                    ),
                    html.Div(
                        id="chart-controls",
                        className="card",
                        children=[
                            html.Div("Chart Type:", style={"fontWeight": "600", "marginBottom": "5px"}),
                            dcc.Dropdown(
                                id="chart-type-dropdown",
                                options=[
                                    {"label": "Hourly Activity", "value": "hourly"},
                                    {"label": "Daily Trends", "value": "daily"},
                                    {"label": "Device Summary", "value": "device"},
                                ],
                                value="hourly",
                                clearable=False,
                                style={"marginBottom": "15px"},
                            ),
                            html.Div(
                                children=[
                                    html.Button("\ud83d\udd0d Filter", id="filter-button", className="dash-button"),
                                    html.Button("\ud83d\uddbd Time Range", id="timerange-button", className="dash-button", style={"marginLeft": "10px"}),
                                ],
                                style={"display": "flex"},
                            ),
                        ],
                    ),
                ],
                style={"display": "grid", "gridTemplateColumns": "repeat(auto-fit, minmax(320px, 1fr))", "gap": "20px", "padding": "0 20px"},
            ),

            # ─────── Tabs ───────
            html.Div(
                id="tabs-container",
                children=[
                    html.Div("Overview", id="tab-overview", className="tab active"),
                    html.Div("Advanced", id="tab-advanced", className="tab"),
                    html.Div("Export", id="tab-export", className="tab"),
                ],
            ),

            # ─────── Tab Content (filled by callback) ───────
            html.Div(id="tab-content"),
        ],
    )


def register_callbacks(app_instance: Dash):
    @app_instance.callback(
        Output("tab-content", "children"),
        [
            Input("tab-overview", "n_clicks_timestamp"),
            Input("tab-advanced", "n_clicks_timestamp"),
            Input("tab-export", "n_clicks_timestamp"),
        ],
    )
    def render_tab_content(ts_overview, ts_advanced, ts_export):
        timestamps = {
            "overview": ts_overview or 0,
            "advanced": ts_advanced or 0,
            "export": ts_export or 0,
        }
        active_tab = max(timestamps, key=timestamps.get)
        if active_tab == "overview":
            return overview_layout()
        elif active_tab == "advanced":
            return advanced_layout()
        else:
            return export_layout()

    @app_instance.callback(
        [
            Output("tab-overview", "className"),
            Output("tab-advanced", "className"),
            Output("tab-export", "className"),
        ],
        [
            Input("tab-overview", "n_clicks_timestamp"),
            Input("tab-advanced", "n_clicks_timestamp"),
            Input("tab-export", "n_clicks_timestamp"),
        ],
    )
    def update_tab_active(ts_overview, ts_advanced, ts_export):
        timestamps = {
            "overview": ts_overview or 0,
            "advanced": ts_advanced or 0,
            "export": ts_export or 0,
        }
        active = max(timestamps, key=timestamps.get)
        return [
            "tab active" if active == "overview" else "tab",
            "tab active" if active == "advanced" else "tab",
            "tab active" if active == "export" else "tab",
        ]


if __name__ == "__main__":
    app.layout = create_main_layout(app)
    register_callbacks(app)
    app.run_server(debug=True)
