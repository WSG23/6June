# app_production.py - Production-ready Yōsai Intel Dashboard
import dash
import sys
import os
from waitress import serve

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import dash_bootstrap_components as dbc

# Import UI components and handlers
from ui.components.upload import create_enhanced_upload_component
from ui.components.mapping import create_mapping_component
from ui.components.classification import create_classification_component
from ui.components.upload_handlers import create_upload_handlers
from ui.components.mapping_handlers import create_mapping_handlers
from ui.components.classification_handlers import create_classification_handlers

# Import layout
from ui.pages.main_page import create_main_layout

# Logging setup
from utils.logging_config import setup_application_logging, get_logger

def create_production_app():
    """Create and configure the production Dash application"""
    
    # Setup logging for production
    setup_application_logging()
    logger = get_logger(__name__)
    
    logger.info("🚀 Initializing Yōsai Intel Dashboard (Production Mode)")
    
    # Create Dash app with production settings
    app = dash.Dash(
        __name__,
        suppress_callback_exceptions=True,
        assets_folder="assets",
        external_stylesheets=[dbc.themes.DARKLY]
    )
    
    # Asset URLs
    ICON_UPLOAD_DEFAULT = app.get_asset_url('upload_file_csv_icon.png')
    ICON_UPLOAD_SUCCESS = app.get_asset_url('upload_file_csv_icon_success.png') 
    ICON_UPLOAD_FAIL = app.get_asset_url('upload_file_csv_icon_fail.png')
    
    # Create UI components
    upload_component = create_enhanced_upload_component(
        ICON_UPLOAD_DEFAULT,
        ICON_UPLOAD_SUCCESS,
        ICON_UPLOAD_FAIL
    )
    mapping_component = create_mapping_component()
    classification_component = create_classification_component()

    # Register callbacks using handler factories
    icons = {
        'default': ICON_UPLOAD_DEFAULT,
        'success': ICON_UPLOAD_SUCCESS,
        'fail': ICON_UPLOAD_FAIL,
    }
    create_upload_handlers(app, upload_component, icons).register_callbacks()
    create_mapping_handlers(app, mapping_component).register_callbacks()
    create_classification_handlers(app, classification_component).register_callbacks()

    # Create main layout
    app.layout = create_main_layout(app)

    logger.info("✅ Production app created successfully")
    return app

if __name__ == "__main__":
    app = create_production_app()
    serve(app.server, host='0.0.0.0', port=8050)
