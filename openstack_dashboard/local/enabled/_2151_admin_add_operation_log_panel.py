# The slug of the panel to be added to HORIZON_CONFIG. Required.
PANEL = 'Operation Log'
# The slug of the dashboard the PANEL associated with. Required.
PANEL_DASHBOARD = 'admin'
# The slug of the panel group the PANEL is associated with.
PANEL_GROUP = 'log_anagement_panel_group'

# Python panel class of the PANEL to be added.
ADD_PANEL = \
    'nec_portal.dashboards.admin.history.panel.HistoryPanel'
