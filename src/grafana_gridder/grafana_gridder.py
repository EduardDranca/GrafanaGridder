from enum import Enum
from grafanalib.core import GridPos

_MAX_WIDTH = 24


class PanelSize(Enum):
    """
    The relative width of a panel.
    The widths of the panels on a row are computed relative to the widths of the other panels on the same row.
    Therefore:

    * an XLARGE panel will be 4 times as wide as a SMALL panel.
    * a LARGE panel will be 3 times as wide as a SMALL panel.
    * a MEDIUM panel will be 2 times as wide as a SMALL panel.
    """
    SMALL = 1
    MEDIUM = 2
    LARGE = 3
    XLARGE = 4


class PanelGroup:
    """
    A group of panels that can be placed in a grid layout.
    The layout can be either:

    * a list of lists of relative sizes, where each inner list represents
      the relative widths of the panels on a row in the grid

    * a list of relative sizes, where each element represents the relative widths of the panels
      and each row of the grid will use the same relative widths

    Each row in the grid will use the entire width of the dashboard and the width of each panel in a row
    will be computed relative to the others' widths. For example, a layout of [[1, 2], [1]] will create two rows.
    The first row will have two panels, where the first panel will take up 1/3 of the width of the dashboard
    and the second panel will take up 2/3 of the width of the dashboard. The second row will have one panel,
    where the panel will take up the entire width of the dashboard.

    :param layout: a list representing the layout of the panels in the grid
    :param panels: the panels to be placed in the grid
    :param panel_height: the height of each panel in the grid
    :param y: the y-coordinate of the top of the grid
    :param row_heights: a list of the heights of each row in the grid;
           if provided, it takes priority over the panel_height
    :param row: a Row panel that will be placed at the top of the grid, optional
    """
    def __init__(self, layout, panels, panel_height=8, y=0, row_heights=None, row=None):
        assert layout is not None, 'layout cannot be None'
        self._layout = layout
        if not isinstance(layout[0], list):
            assert len(panels) % len(layout) == 0, 'Panel count does not match layout'
            self._layout = [layout] * int(len(panels) / len(layout))
        assert sum(len(row) for row in self._layout) == len(panels), 'Panel count does not match layout'

        if row_heights is None:
            self.row_heights = [panel_height] * len(self._layout)
        else:
            assert len(row_heights) == len(self._layout), 'Row height count does not match layout'
            self.row_heights = row_heights

        self.row = row
        self._y = y
        self.height = sum(self.row_heights) + len(self.row_heights) + (2 if self.row is not None else 0)
        self.panels = panels
        self._compute_grid_pos()

    def _compute_grid_pos(self):
        """Compute GridPos for all panels"""
        panel_index = 0
        current_y = self._y
        if self.row is not None:
            self.row.gridPos = GridPos(x=0, y=self._y, w=_MAX_WIDTH, h=1)
            current_y += 2
        for row_index, panel_sizes in enumerate(self._layout):
            current_x = 0
            panel_sizes_sum = sum(list(map(lambda size: size.value, [size for size in panel_sizes])))
            panel_sizes_units = [size.value / panel_sizes_sum * _MAX_WIDTH for size in panel_sizes]
            panel_sizes_units = [round(unit) for unit in panel_sizes_units[:-1]]
            panel_sizes_units[-1] = _MAX_WIDTH - sum(panel_sizes_units[:-1])
            for width in panel_sizes_units:
                panel = self.panels[panel_index]
                panel.gridPos = GridPos(x=current_x, y=current_y, w=width, h=self.row_heights[row_index])
                current_x += width
                panel_index += 1
            current_y += self.row_heights[row_index] + 1

    def set_y(self, y):
        """Sets the position of the PanelGroup on the y-axis"""
        assert y >= 0, 'y-axis position must be at least 0'
        delta = y - self._y
        if self.row is not None:
            self.row.gridPos.y += delta
        for panel in self.panels:
            panel.gridPos.y += delta
        self._y = y

    def get_height(self):
        """Returns the height of the PanelGroup"""
        return self.height


class PanelPositioning:
    """
    A container for PanelGroups and PanelPositioning.
    Used for positioning groups of panels vertically.
    The panel groups are placed in vertical order according to their order in the panel_groups param.

    :param panel_groups: a list of PanelGroups or PanelPositioning objects
    """
    def __init__(self, panel_groups=None):
        if panel_groups is None:
            panel_groups = []
        self.panel_groups = panel_groups
        self.y = 0
        self.height = 0

    def add_panel_group(self, panel_group):
        """Adds a PanelGroup or a PanelPositioning to the PanelPositioning"""
        self.panel_groups.append(panel_group)

    def get_height(self):
        """Returns the height of the PanelPositioning"""
        return sum([panel_group.get_height() for panel_group in self.panel_groups])

    def set_y(self, y):
        """Sets the position of the PanelPositioning on the y-axis"""
        assert y >= 0, 'y-axis position must be at least 0'
        self.y = y

    @property
    def panels(self):
        current_y = self.y
        for group in self.panel_groups:
            group.set_y(current_y)
            current_y += group.get_height()
        panels = []
        for group in self.panel_groups:
            if hasattr(group, 'row') and group.row is not None:
                panels.append(group.row)
            panels.extend(group.panels)
        return panels

