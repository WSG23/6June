import dash
from dash import html, dcc, callback, Output, Input

# Create temporary Dash instance to build asset URL
_tmp = dash.Dash(__name__)
CUSTOM_CSS = _tmp.get_asset_url("custom.css")

# Main Dash app with external stylesheet
app = dash.Dash(
    __name__,
    external_stylesheets=[CUSTOM_CSS],
    suppress_callback_exceptions=True,
)


def overview_content():
    return html.Div(
        id="stats-panels-container",
        children=[
            html.Div([html.H3("Access Events")], id="card-access"),
            html.Div([html.H3("Device Analytics")], id="card-device"),
            html.Div([html.H3("Peak Activity")], id="card-peak"),
        ],
    )


def advanced_content():
    return html.Div(
        id="stats-panels-container",
        children=[
            html.Div([html.H3("Traffic Pattern")], id="card-traffic"),
            html.Div([html.H3("Anomaly Detection")], id="card-anomaly"),
            html.Div([html.H3("Usage Efficiency")], id="card-usage"),
            html.Div([html.H3("Security Score")], id="card-security"),
        ],
    )


def export_content():
    return html.Div(
        id="export-buttons",
        children=[
            html.Button("\ud83d\udcca Export CSV", className="dash-button"),
            html.Button("\ud83d\udcc9 Download Charts", className="dash-button"),
            html.Button("\ud83e\uddfe Generate Report", className="dash-button"),
            html.Button("\ud83d\udd04 Refresh Data", className="dash-button"),
        ],
    )


def create_main_layout(app_instance: dash.Dash) -> html.Div:
    return html.Div(
        children=[
            html.Div(
                id="dashboard-title",
                children=[
                    html.Div(
                        [
                            html.Img(
                                src=app_instance.get_asset_url("logo.png"),
                                style={"height": "40px"},
                            ),
                            html.H1("Enhanced Analytics Dashboard", className="ml-2"),
                        ],
                        style={"display": "flex", "alignItems": "center"},
                    ),
                    html.Button("Advanced View \u23f7", id="advanced-view-button"),
                ],
            ),
            html.Div(
                style={"display": "flex", "gap": "20px"},
                children=[
                    html.Div(
                        id="upload-section",
                        children=[
                            dcc.Upload(
                                id="upload-data",
                                className="upload-box",
                                children=[
                                    html.P("Drop CSV or JSON file here"),
                                    html.Img(
                                        src=app_instance.get_asset_url("upload_file_csv_icon.png"),
                                        style={"height": "60px", "marginTop": "10px"},
                                    ),
                                ],
                            )
                        ],
                    ),
                    html.Div(
                        id="chart-controls",
                        children=[
                            dcc.Dropdown(
                                id="chart-type",
                                options=[{"label": "Hourly Activity", "value": "hourly"}],
                                value="hourly",
                            ),
                            html.Button("\ud83d\udd0d Filter", id="filter-button", className="dash-button"),
                            html.Button("\ud83d\uddbd Time Range", id="timerange-button", className="dash-button"),
                        ],
                    ),
                ],
            ),
            html.Div(
                id="tabs-container",
                children=[
                    html.Div("Overview", className="tab active", id="tab-overview"),
                    html.Div("Advanced", className="tab", id="tab-advanced"),
                    html.Div("Export", className="tab", id="tab-export"),
                ],
            ),
            html.Div(id="tab-content", children=overview_content()),
        ],
    )


def register_callbacks(app_instance: dash.Dash):
    @app_instance.callback(
        [
            Output("tab-overview", "className"),
            Output("tab-advanced", "className"),
            Output("tab-export", "className"),
            Output("tab-content", "children"),
        ],
        [
            Input("tab-overview", "n_clicks"),
            Input("tab-advanced", "n_clicks"),
            Input("tab-export", "n_clicks"),
        ],
        prevent_initial_call=False,
    )
    def switch_tabs(n_over, n_adv, n_exp):
        ctx = dash.callback_context
        tab = "tab-overview"
        if ctx.triggered:
            tab = ctx.triggered[0]["prop_id"].split(".")[0]
        if tab == "tab-advanced":
            content = advanced_content()
        elif tab == "tab-export":
            content = export_content()
        else:
            content = overview_content()
            tab = "tab-overview"
        return (
            "tab active" if tab == "tab-overview" else "tab",
            "tab active" if tab == "tab-advanced" else "tab",
            "tab active" if tab == "tab-export" else "tab",
            content,
        )


if __name__ == "__main__":
    app.layout = create_main_layout(app)
    register_callbacks(app)
    app.run_server(debug=True)
