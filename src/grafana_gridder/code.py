from grafanalib.core import Dashboard, TimeSeries, BarGauge, RowPanel
from grafana_gridder import PanelGroup, PanelPositioning, PanelSize

from grafanalib._gen import print_alertgroup

# Define panel groups
panel_group1 = PanelGroup(
    layout=[[PanelSize.LARGE, PanelSize.MEDIUM], [PanelSize.SMALL, PanelSize.SMALL]],
    panels=[TimeSeries(), TimeSeries(), BarGauge(), BarGauge()])
panel_group2 = PanelGroup(
    layout=[PanelSize.SMALL, PanelSize.MEDIUM, PanelSize.MEDIUM],
    panels=[TimeSeries(), TimeSeries(), TimeSeries()],
    row=RowPanel(title="RowTitle"))

# Create panel positioning
positioning = PanelPositioning(panel_groups=[panel_group1, panel_group2])

# Generate dashboard
dashboard = Dashboard(
    title='My Dashboard',
    panels=positioning.panels
)

print_alertgroup(dashboard)