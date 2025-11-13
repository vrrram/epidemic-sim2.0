"""
Reusable UI widgets for the epidemic simulation interface

This module contains custom PyQt5 widgets used throughout the simulation UI:
- CollapsibleBox: A collapsible container for organizing control panels
- PieChartWidget: A matplotlib-based pie chart for displaying population statistics
"""

from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from epidemic_sim.view.theme import NEON_GREEN, DARK_GREEN, BG_BLACK, PANEL_BLACK, BORDER_GREEN, get_color


class CollapsibleBox(QWidget):
    """
    A collapsible container widget with a toggle button header.

    This widget provides a space-saving UI element that can expand/collapse to show/hide
    its contents. Used extensively in the control panel to organize related parameters
    into logical groups that can be collapsed when not needed.

    Features:
    - Click-to-toggle functionality with visual feedback
    - Animated arrow indicator (▼/▶) showing state
    - Theme-aware styling with neon green accents
    - Automatic layout recalculation on state change

    Attributes:
        toggle_button (QPushButton): The clickable header button
        content_area (QWidget): Container for child widgets
        content_layout (QVBoxLayout): Layout manager for content area

    Example:
        box = CollapsibleBox("Advanced Options")
        box.addWidget(QLabel("Setting 1"))
        box.addWidget(QSlider())
    """

    def __init__(self, title, parent=None):
        """
        Initialize a collapsible box with a title.

        Args:
            title (str): The text to display in the header button
            parent (QWidget, optional): Parent widget. Defaults to None.
        """
        super().__init__(parent)
        self.toggle_button = QPushButton(f"▼ {title}")
        self.toggle_button.setCheckable(True)
        self.toggle_button.setChecked(True)
        self.toggle_button.setStyleSheet(f"""
            QPushButton {{
                text-align: left;
                padding: 8px;
                font-weight: bold;
                border: 2px solid {BORDER_GREEN};
                background-color: {PANEL_BLACK};
                color: {NEON_GREEN};
                font-family: 'Courier New', monospace;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background-color: {get_color('HOVER_BG')};
                border-color: {NEON_GREEN};
            }}
        """)
        self.toggle_button.clicked.connect(self.toggle)

        self.content_area = QWidget()
        self.content_layout = QVBoxLayout()
        self.content_layout.setContentsMargins(5, 5, 5, 5)
        self.content_layout.setSpacing(3)
        self.content_area.setLayout(self.content_layout)

        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 3)
        layout.addWidget(self.toggle_button)
        layout.addWidget(self.content_area)

    def toggle(self):
        """
        Toggle the visibility of the content area.

        Called automatically when the user clicks the header button. Updates the
        arrow indicator, shows/hides content, and forces the parent layout to
        recalculate to accommodate the size change.
        """
        checked = self.toggle_button.isChecked()
        self.content_area.setVisible(checked)
        icon = "▼" if checked else "▶"
        current_text = self.toggle_button.text()
        self.toggle_button.setText(f"{icon} {current_text[2:]}")

        # Force the parent to recalculate its size
        if checked:
            self.content_area.setMaximumHeight(16777215)  # QWIDGETSIZE_MAX
        else:
            self.content_area.setMaximumHeight(0)

        # Trigger layout update
        self.updateGeometry()
        if self.parent():
            self.parent().updateGeometry()

    def update_theme(self):
        """
        Update the collapsible box styling to match the current theme.

        This method should be called when the application theme changes to ensure
        the widget's colors remain consistent with the selected theme.
        """
        self.toggle_button.setStyleSheet(f"""
            QPushButton {{
                text-align: left;
                padding: 8px;
                font-weight: bold;
                border: 2px solid {BORDER_GREEN};
                background-color: {PANEL_BLACK};
                color: {NEON_GREEN};
                font-family: 'Courier New', monospace;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background-color: {get_color('HOVER_BG')};
                border-color: {NEON_GREEN};
            }}
        """)

    def addWidget(self, widget):
        """
        Add a widget to the collapsible content area.

        Args:
            widget (QWidget): The widget to add to the content area
        """
        self.content_layout.addWidget(widget)

    def addLayout(self, layout):
        """
        Add a layout to the collapsible content area.

        Args:
            layout (QLayout): The layout to add to the content area
        """
        self.content_layout.addLayout(layout)


class PieChartWidget(FigureCanvasQTAgg):
    """
    A matplotlib-based pie chart widget for displaying population statistics.

    This widget renders a pie chart showing the breakdown of the population by
    infection state, including separate segments for symptomatic and asymptomatic
    infected individuals, and dead individuals as a separate category.

    Features:
    - Automatic color coding by state (blue=susceptible, red=symptomatic, etc.)
    - Percentage labels on each slice
    - Legend with clear state labels
    - Theme-aware background and text colors
    - Handles zero-population cases gracefully

    The chart updates dynamically as the simulation progresses, providing a clear
    visual representation of the epidemic's impact on the population.

    Attributes:
        fig (Figure): Matplotlib figure object
        axes (Axes): Matplotlib axes for the pie chart

    Example:
        chart = PieChartWidget(parent=control_panel)
        chart.update_chart({'susceptible': 970, 'infected': 20, 'removed': 10, 'dead': 0})
    """

    def __init__(self, parent=None, width=4, height=4, dpi=100):
        """
        Initialize the pie chart widget.

        Args:
            parent (QWidget, optional): Parent widget. Defaults to None.
            width (float, optional): Figure width in inches. Defaults to 4.
            height (float, optional): Figure height in inches. Defaults to 4.
            dpi (int, optional): Dots per inch for rendering. Defaults to 100.
        """
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.fig.patch.set_facecolor(BG_BLACK)
        self.axes = self.fig.add_subplot(111)
        super().__init__(self.fig)
        self.setParent(parent)
        self.setStyleSheet(f"background-color: {BG_BLACK};")

    def update_chart(self, counts):
        """
        Update the pie chart with current population counts.

        Renders a new pie chart based on the provided state counts. Automatically
        separates infected individuals into symptomatic and asymptomatic categories
        based on the simulation's probability parameters. Includes dead individuals
        as a separate category.

        Args:
            counts (dict): Dictionary with keys 'susceptible', 'infected', 'removed', 'dead'
                          and integer values representing population in each state.
                          Example: {'susceptible': 970, 'infected': 20, 'removed': 10, 'dead': 0}

        Note:
            The chart will not render if the total population is zero or if all
            categories have zero individuals.
        """
        # Local import to avoid circular dependency
        import epidemic_sim3
        params = epidemic_sim3.params
        self.axes.clear()

        total = sum(counts.values())
        if total == 0:
            return

        # Separate infected into symptomatic and asymptomatic
        infected_total = counts['infected']
        asymptomatic = infected_total * params.prob_no_symptoms
        symptomatic = infected_total * (1 - params.prob_no_symptoms)

        # Prepare data
        labels = []
        sizes = []
        colors = []

        if counts['susceptible'] > 0:
            labels.append('Susceptible')
            sizes.append(counts['susceptible'])
            colors.append(get_color('PIE_SUSCEPTIBLE'))

        if symptomatic > 0.5:
            labels.append('Infected (Symp.)')
            sizes.append(symptomatic)
            colors.append(get_color('PIE_INFECTED_SYMP'))

        if asymptomatic > 0.5:
            labels.append('Infected (Asymp.)')
            sizes.append(asymptomatic)
            colors.append(get_color('PIE_INFECTED_ASYMP'))

        if counts['removed'] > 0:
            labels.append('Removed')
            sizes.append(counts['removed'])
            colors.append(get_color('PIE_REMOVED'))

        if counts['dead'] > 0:
            labels.append('Dead')
            sizes.append(counts['dead'])
            colors.append(get_color('PIE_DEAD'))

        if not sizes:
            return

        # Create pie chart with percentages only (no labels on slices)
        wedges, texts, autotexts = self.axes.pie(
            sizes,
            colors=colors,
            autopct='%1.1f%%',
            startangle=90,
            pctdistance=0.85,
            textprops={'fontsize': 9, 'weight': 'bold'}
        )

        # Style percentage text to be readable
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(9)

        # Add legend outside the pie to avoid overlap
        self.axes.legend(
            wedges, labels,
            loc="center left",
            bbox_to_anchor=(0.85, 0, 0.5, 1),
            fontsize=9,
            frameon=True,
            facecolor=BG_BLACK,
            edgecolor=NEON_GREEN,
            labelcolor=NEON_GREEN
        )

        self.axes.set_facecolor(BG_BLACK)
        self.fig.tight_layout()
        self.draw()
