import dash
from dash import Dash, html, dcc, Input, Output
from ui.components.upload import create_enhanced_upload_component
from ui.components.classification import create_classification_component
from ui.components.graph import create_graph_component

# Temporary Dash app to get the asset URL for custom.css
_tmp = Dash(__name__)
CUSTOM_CSS = _tmp.get_asset_url("custom.css")

# Main Dash app with external stylesheet
app = Dash(__name__, external_stylesheets=[CUSTOM_CSS])


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

                        id="card-security",
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

                    html.Button("📊 Export Stats CSV", id="export-csv", className="dash-button"),
                    html.Button("📉 Download Charts", id="download-charts", className="dash-button"),
                    html.Button("🧾 Generate Report", id="generate-report", className="dash-button"),
                    html.Button("🔄 Refresh Data", id="refresh-data", className="dash-button"),

                ],
            )
        ],
    )


def create_main_layout(app_instance: Dash) -> html.Div:
    upload_component = create_enhanced_upload_component(
        app_instance.get_asset_url("upload_file_csv_icon.png"),
        app_instance.get_asset_url("upload_file_csv_icon_success.png"),
        app_instance.get_asset_url("upload_file_csv_icon_fail.png"),
    )
    classification_component = create_classification_component()
    graph_component = create_graph_component()

    return html.Div(
        id="app-container",
        children=[
            html.Div(upload_component.create_upload_area(), style={"width": "100%"}),
            classification_component.create_facility_setup_card(),
            graph_component.create_graph_container(),
            html.Div(
                className="flex-row",
                children=[
                    html.Div(
                        id="access-events-card",
                        className="card",
                        children=[
                            html.H3("Access Events"),
                            html.Div(id="total-access-events-H1"),
                            html.Div(id="event-date-range-P"),
                        ],
                    ),
                    html.Div(
                        id="user-analytics-card",
                        className="card",
                        children=[
                            html.H3("User Analytics"),
                            html.Div(id="stats-unique-users"),
                            html.Div(id="stats-avg-events-per-user"),
                            html.Div(id="stats-most-active-user"),
                            html.Div(id="stats-devices-per-user"),
                            html.Div(id="stats-peak-hour"),
                        ],
                    ),
                    html.Div(
                        id="device-analytics-card",
                        className="card",
                        children=[
                            html.H3("Device Analytics"),
                            html.Table([
                                html.Thead(html.Tr([html.Th("DEVICE"), html.Th("EVENTS")])),
                                html.Tbody(id="most-active-devices-table-body"),
                            ]),
                            html.Div(id="total-devices-count"),
                            html.Div(id="entrance-devices-count"),
                            html.Div(id="high-security-devices"),
                        ],
                    ),
                    html.Div(
                        id="peak-activity-card",
                        className="card",
                        children=[
                            html.H3("Peak Activity"),
                            html.Div(id="peak-hour-display"),
                            html.Div(id="peak-day-display"),
                            html.Div(id="weekday-percent"),
                            html.Div(id="weekend-percent"),
                        ],
                    ),
                    html.Div(
                        id="security-overview-card",
                        className="card",
                        children=[
                            html.H3("Security Overview"),
                            html.Div(["🟢 ", html.Span(id="security-green-count")]),
                            html.Div(["🔴 ", html.Span(id="security-red-count")]),
                            html.Div(["🟡 ", html.Span(id="security-yellow-count")]),
                            html.Div(id="security-compliance"),
                            html.Div(id="security-alerts"),
                        ],
                    ),
                    html.Div(
                        id="advanced-analytics-card",
                        className="card",
                        children=[
                            html.H3("Advanced Analytics"),
                            html.Div("Traffic Pattern", id="toggle-traffic-pattern", className="toggle-btn blue"),
                            html.Div("Security Score", id="toggle-security-score", className="toggle-btn green"),
                            html.Div("Usage Efficiency", id="toggle-usage-efficiency", className="toggle-btn yellow"),
                            html.Div("Anomaly Detection", id="toggle-anomaly-detection", className="toggle-btn red"),
                        ],
                    ),
                    html.Div(
                        id="data-visualization-card",
                        className="card",
                        style={"flex": "1"},
                        children=[
                            html.H3("Data Visualization"),
                            html.Label("Chart Type:", htmlFor="chart-type-dropdown"),
                            dcc.Dropdown(
                                id="chart-type-dropdown",
                                options=[
                                    {"label": "Hourly Activity", "value": "hourly"},
                                    {"label": "Security Distribution", "value": "security"},
                                    {"label": "Heatmap (Day vs Hour)", "value": "heatmap"},
                                ],
                                value="hourly",
                                style={"width": "200px", "marginBottom": "10px"},
                            ),
                            dcc.Graph(id="main-chart", config={"displayModeBar": True}, style={"height": "400px"}),
                        ],
                    ),
                    html.Div(
                        id="export-reports-card",
                        className="card",
                        style={"minWidth": "200px"},
                        children=[
                            html.H3("Export & Reports"),
                            html.Button("📊 Export Stats CSV", id="export-csv-btn", className="btn btn-light", style={"marginBottom": "10px", "width": "100%"}),
                            html.Button("💾 Download Charts", id="download-charts-btn", className="btn btn-light", style={"marginBottom": "10px", "width": "100%"}),
                            html.Button("Generate Report", id="generate-report-btn", className="btn btn-primary", style={"marginBottom": "10px", "width": "100%"}),
                            html.Button("🔄 Refresh Data", id="refresh-data-btn", className="btn btn-light", style={"width": "100%"}),
                        ],
                    ),
                ],
            ),

            dcc.Store(id="uploaded-file-store"),
            dcc.Store(id="csv-headers-store", storage_type="session"),
            dcc.Store(id="processed-data-store", storage_type="session"),
            dcc.Store(id="enhanced-metrics-store", storage_type="session"),
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
        active_tab = max(timestamps, key=lambda k: timestamps[k])
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
        active = max(timestamps, key=lambda k: timestamps[k])
        return [
            "tab active" if active == "overview" else "tab",
            "tab active" if active == "advanced" else "tab",
            "tab active" if active == "export" else "tab",
        ]


if __name__ == "__main__":
    app.layout = create_main_layout(app)
    register_callbacks(app)
    app.run_server(debug=True)
