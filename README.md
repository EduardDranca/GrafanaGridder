Grafana Gridder
---

The Grafana Gridder is a grafanalib wrapper designed to simplify the organization and layout of panels within Grafana dashboards.
It provides an intuitive way to define and position groups of panels in a grid layout, making it easier to create visually appealing and organized dashboards.

### Features
* Panel Grouping: Define groups of panels that can be positioned together within a dashboard.
* Flexible Layout: Supports flexible grid layouts, allowing panels to be arranged in rows with customizable widths and heights.
* Vertical Positioning: Easily position panel groups vertically within a dashboard.
* Intuitive API: Simple and easy-to-use API for defining panel layouts and positioning.

### Example
```python
from grafanalib.core import Dashboard, TimeSeries, BarGauge, RowPanel
from grafana_gridder import PanelGroup, PanelPositioning, PanelSize

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
```

### Installation
You can install the Grafana Panel Layout Wrapper using pip:

```shell
pip install grafana_gridder
```