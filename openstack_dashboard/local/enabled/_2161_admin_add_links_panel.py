# The slug of the panel to be added to HORIZON_CONFIG. Required.
PANEL = 'Links'
# The slug of the dashboard the PANEL associated with. Required.
PANEL_DASHBOARD = 'admin'
# The slug of the panel group the PANEL is associated with.
PANEL_GROUP = 'link_panel_group'

# Python panel class of the PANEL to be added.
ADD_PANEL = \
    'nec_portal.dashboards.admin.links.panel.LinksPanel'
