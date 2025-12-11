"""
Main Application Window Module

This module contains the EpidemicApp class which is the main application window
for the epidemic simulation. It provides the complete user interface including:
- Left panel: Parameter controls with sliders and presets
- Center: Simulation canvas for visual display
- Right panel: Controls, statistics, graphs, and visualizations

The window supports:
- Theme switching (dark/light modes)
- Keyboard shortcuts for quick access
- Preset scenarios for educational use
- Real-time statistics and visualization
- Fullscreen mode
- Font size adjustment
"""

import sys
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QLabel, QSlider, QComboBox, QCheckBox, QSpinBox,
    QDoubleSpinBox, QScrollArea, QTabWidget, QButtonGroup, QTextEdit,
    QDialog, QApplication
)
from PyQt5.QtCore import Qt, QTimer, QSettings
from PyQt5.QtGui import QFont
import pyqtgraph as pg

from epidemic_sim.config.parameters import params
from epidemic_sim.config.presets import PRESETS
from epidemic_sim.model.simulation import EpidemicSimulation
from epidemic_sim.view.canvas import SimulationCanvas
from epidemic_sim.view.widgets import CollapsibleBox, PieChartWidget
from epidemic_sim.view import theme as theme_module
from epidemic_sim.view.theme import (
    DARK_THEME, LIGHT_THEME, get_color,
    update_legacy_colors, NEON_GREEN, BG_BLACK, PANEL_BLACK, BORDER_GREEN
)


class EpidemicApp(QMainWindow):
    """
    Main application window for the Epidemic Simulation.

    This class manages the entire UI including parameter controls, simulation canvas,
    statistics display, and visualization graphs. It handles user interactions,
    theme switching, and coordinates the simulation engine.

    Features:
        - Three-panel layout (parameters | canvas | controls)
        - Dark/light theme support with saved preferences
        - Keyboard shortcuts for common actions
        - Preset scenarios for quick configuration
        - Real-time graphs and pie charts
        - Adjustable font size
        - Fullscreen mode
        - Tooltip system with toggle

    Attributes:
        sim (EpidemicSimulation): The simulation engine instance
        canvas (SimulationCanvas): The visual display widget
        speed (float): Simulation speed multiplier (0.5x to 5x)
        paused (bool): Whether simulation is paused
        collapsible_boxes (list): All collapsible UI sections for theme updates
    """

    def __init__(self):
        """Initialize the main application window and set up all UI components."""
        super().__init__()
        self.setWindowTitle("EPIDEMIC SIMULATION v3.0 - Enhanced Edition")
        self.setGeometry(50, 50, 1800, 1000)

        # Load saved theme preference
        self.settings = QSettings("EpidemicSimulator", "Theme")
        saved_theme = self.settings.value("theme", "dark")  # Default to dark
        self.load_theme(saved_theme)

        # Load saved font size preference
        self.base_font_size = int(self.settings.value("font_size", 10))

        # Initialize simulation engine
        self.sim = EpidemicSimulation('simple')
        self.sim.stats_updated.connect(self.update_stats_display)
        self.sim.log_message.connect(self.add_log)

        # Simulation control
        self.speed = 1.0
        self.paused = True  # Start paused to allow parameter configuration
        self.speed_accumulator = 0.0  # For smooth fractional speed

        # Mode control (BASIC or ADVANCED)
        self.mode = "BASIC"  # Start in BASIC mode

        # Track collapsible boxes for theme updates
        self.collapsible_boxes = []

        # Performance optimization: frame skipping
        self.frame_count = 0
        self.skip_frames = 1  # Render every Nth frame (adjusted dynamically)

        # Tooltip state (enabled by default)
        self.tooltips_enabled = True

        self.setup_ui()
        self.sim.initialize()

        # Simple tooltip configuration - no flicker
        self._configure_tooltips_simple()

        # Start simulation timer (60 FPS target)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_simulation)
        self.timer.start(16)

    def setup_ui(self):
        """
        Set up the complete user interface with three panels:
        - Left: Parameter controls (collapsible)
        - Center: Simulation canvas
        - Right: Controls, stats, and visualizations
        """
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # === LEFT PANEL: PARAMETERS (COLLAPSIBLE) ===
        self.left_panel = QWidget()
        self.left_panel.setStyleSheet(f"background-color: {BG_BLACK};")
        self.left_panel.setMaximumWidth(350)
        self.left_panel.setMinimumWidth(300)

        left_scroll = QScrollArea()
        left_scroll.setWidgetResizable(True)
        left_scroll.setWidget(self.left_panel)
        left_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        left_scroll.setStyleSheet(f"""
            QScrollArea {{ border: none; background-color: {BG_BLACK}; border-right: 2px solid {BORDER_GREEN}; }}
            QScrollBar:vertical {{
                background-color: {PANEL_BLACK}; width: 12px;
                border: 1px solid {BORDER_GREEN};
            }}
            QScrollBar::handle:vertical {{
                background-color: {BORDER_GREEN}; min-height: 20px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """)

        left_layout = QVBoxLayout(self.left_panel)
        left_layout.setSpacing(10)
        left_layout.setContentsMargins(10, 10, 10, 10)

        # Collapse button
        collapse_btn = QPushButton("COLLAPSE PARAMETERS <<")
        collapse_btn.clicked.connect(self.toggle_left_panel)
        collapse_btn.setMinimumHeight(30)
        left_layout.addWidget(collapse_btn)
        self.left_collapse_btn = collapse_btn

        # === LEFT PANEL: ALL PARAMETERS ===
        self.sliders = {}

        # DISEASE PARAMETERS
        self.disease_box = CollapsibleBox("DISEASE PARAMETERS")
        self.collapsible_boxes.append(self.disease_box)

        # Define tooltips for disease parameters
        disease_tooltips = {
            'infection_radius': """Infection Radius: How far the disease can spread between particles

Recommended: 0.10-0.20
• Smaller (0.05-0.10): Localized outbreaks, slow spread
• Medium (0.10-0.20): Realistic epidemic behavior
• Larger (0.20-0.40): Rapid, aggressive spread

Tip: Combine with infection probability for fine control""",

            'prob_infection': """Infection Probability: Chance of transmission when particles are within infection radius

Recommended: 0.10-0.30
• Low (0.05-0.15): Slow spread, allows time for interventions
• Medium (0.15-0.50): Realistic epidemic dynamics
• High (0.50-1.00): Extremely contagious disease

Tip: Modified by individual susceptibility (Normal distribution)""",

            'infection_duration': """Infection Duration: How many days a particle remains infected

Recommended: 14-28 days
• Short (1-7 days): Quick recovery, rapid turnover
• Medium (7-21 days): Typical viral infection
• Long (21-100 days): Chronic infection

Tip: Modified by recovery time variation (Exponential distribution)""",

            'mortality_rate': """Mortality Rate: Probability that an infected particle dies instead of recovering

Recommended: 0.00-0.05
• 0%: No deaths, pure SIR model
• 1-5%: Realistic mortality for serious diseases
• 5-20%: High-mortality outbreak
• >20%: Extreme scenario

Tip: Deaths remove particles permanently from simulation""",

            'fraction_infected_init': """Initial Infected %: Percentage of population starting as infected (Patient Zero)

Recommended: 0.005-0.02 (0.5%-2%)
• Very Low (0.001-0.005): Single patient zero scenario
• Low (0.005-0.02): Few initial cases
• Medium (0.02-0.05): Multiple outbreak sources

Tip: Lower values show clearer epidemic curve development"""
        }

        disease_params = [
            ('infection_radius', 'Infection Radius', 0.01, 0.4, 0.15),
            ('prob_infection', 'Infection Probability', 0, 1.0, 0.15),
            ('infection_duration', 'Infection Duration (days)', 1, 100, 25),
            ('mortality_rate', 'Mortality Rate', 0, 1.0, 0.0),
            ('fraction_infected_init', 'Initial Infected %', 0, 0.05, 0.01),
        ]
        for param, label, min_val, max_val, default in disease_params:
            lbl = QLabel(f"{label}: {default:.3g}")
            lbl.setStyleSheet(f"color: {NEON_GREEN}; font-size: 13px; margin-top: 4px;")
            lbl.setToolTip(disease_tooltips.get(param, label))
            self.disease_box.addWidget(lbl)
            slider = QSlider(Qt.Horizontal)
            slider.setMinimum(int(min_val * 100))
            slider.setMaximum(int(max_val * 100))
            slider.setValue(int(default * 100))
            slider.setMinimumHeight(22)
            slider.setToolTip(disease_tooltips.get(param, label))
            slider.valueChanged.connect(
                lambda val, p=param, l=lbl, label=label: self.update_param(p, val/100, l, label)
            )
            self.disease_box.addWidget(slider)
            self.sliders[param] = (slider, lbl, label)
        left_layout.addWidget(self.disease_box)

        # POPULATION PARAMETERS
        self.pop_box = CollapsibleBox("POPULATION PARAMETERS")
        self.collapsible_boxes.append(self.pop_box)

        # Define tooltips for population parameters
        pop_tooltips = {
            'num_particles': """Population Size: Number of particles (people) in the simulation

Recommended: 200-500 for balance of detail and performance
• Small (50-200): Fast, good for testing, less realistic statistics
• Medium (200-500): Balanced performance and statistical validity
• Large (500-1000): More realistic, slower performance

Tip: Requires RESET to apply. Larger populations need more time to show trends""",

            'social_distance_factor': """Social Distancing Strength: Repulsive force between nearby particles

Recommended: 0.5-1.5
• 0: No social distancing, normal behavior
• 0.5-1.0: Moderate distancing, maintaining personal space
• 1.0-2.0: Strong distancing, active avoidance

Tip: Simulates behavior changes during epidemic awareness""",

            'social_distance_obedient': """Social Distance Compliance: Percentage of population following distancing rules

Recommended: 0.5-0.9
• Low (0-0.5): Poor compliance, many ignore rules
• Medium (0.5-0.8): Realistic mixed compliance
• High (0.8-1.0): Excellent public cooperation

Tip: Combine with distance strength to model intervention effectiveness"""
        }

        # Population size slider (integer, requires reset)
        pop_lbl = QLabel(f"Population Size: {params.num_particles} (reset to apply)")
        pop_lbl.setStyleSheet(f"color: {NEON_GREEN}; font-size: 13px; margin-top: 4px;")
        pop_lbl.setToolTip(pop_tooltips['num_particles'])
        self.pop_box.addWidget(pop_lbl)
        pop_slider = QSlider(Qt.Horizontal)
        pop_slider.setMinimum(50)
        pop_slider.setMaximum(1000)
        pop_slider.setValue(params.num_particles)
        pop_slider.setMinimumHeight(22)
        pop_slider.setToolTip(pop_tooltips['num_particles'])
        pop_slider.valueChanged.connect(
            lambda val: self.update_param('num_particles', val, pop_lbl, 'Population Size', is_int=True)
        )
        self.pop_box.addWidget(pop_slider)
        self.sliders['num_particles'] = (pop_slider, pop_lbl, 'Population Size')

        # Other population parameters (floats)
        pop_params = [
            ('social_distance_factor', 'Social Distancing Strength', 0, 2, 0),
            ('social_distance_obedient', 'Social Distance Compliance', 0, 1, 1.0),
        ]
        for param, label, min_val, max_val, default in pop_params:
            lbl = QLabel(f"{label}: {default:.3g}")
            lbl.setStyleSheet(f"color: {NEON_GREEN}; font-size: 13px; margin-top: 4px;")
            lbl.setToolTip(pop_tooltips.get(param, label))
            self.pop_box.addWidget(lbl)
            slider = QSlider(Qt.Horizontal)
            slider.setMinimum(int(min_val * 100))
            slider.setMaximum(int(max_val * 100))
            slider.setValue(int(default * 100))
            slider.setMinimumHeight(22)
            slider.setToolTip(pop_tooltips.get(param, label))
            slider.valueChanged.connect(
                lambda val, p=param, l=lbl, label=label: self.update_param(p, val/100, l, label)
            )
            self.pop_box.addWidget(slider)
            self.sliders[param] = (slider, lbl, label)
        left_layout.addWidget(self.pop_box)

        # INTERVENTION PARAMETERS
        self.interv_box = CollapsibleBox("INTERVENTION PARAMETERS")
        self.collapsible_boxes.append(self.interv_box)

        # Define tooltips for intervention parameters
        interv_tooltips = {
            'boxes_to_consider': """Social Distance Range: How many grid cells away particles check for crowding

Recommended: 1-3
• 1: Only immediate neighbors affect distancing
• 2-3: Moderate awareness of surrounding density
• 4-10: Wide-area crowd avoidance

Tip: Higher values increase computation but more realistic behavior""",

            'quarantine_after': """Quarantine After (days): Days infected before symptomatic particles quarantine

Recommended: 3-7 days
• Short (1-3): Quick isolation, unrealistic early detection
• Medium (3-7): Realistic symptom onset timing
• Long (7-20): Delayed response, more spread before isolation

Tip: Only applies to symptomatic cases (see Asymptomatic Rate)""",

            'start_quarantine': """Quarantine Start Day: Simulation day when quarantine policy begins

Recommended: 10-20 days
• Early (0-10): Proactive intervention before major spread
• Medium (10-20): Reactive after outbreak detected
• Late (20-30): Delayed response, epidemic already advanced

Tip: Set to 0 for immediate quarantine from start""",

            'prob_no_symptoms': """Asymptomatic Rate: Proportion of infected who never show symptoms

Recommended: 0.15-0.30 (15-30%)
• Low (0-0.15): Most infections detectable
• Medium (0.15-0.30): Realistic for many diseases (e.g., COVID-19)
• High (0.30-0.50): Many hidden spreaders

Tip: Asymptomatic particles never quarantine, continuing to spread disease"""
        }

        # Only keep general intervention parameter (Social Distance Range)
        interv_params = [
            ('boxes_to_consider', 'Social Distance Range', 1, 10, 2),
        ]
        for param, label, min_val, max_val, default in interv_params:
            lbl = QLabel(f"{label}: {default:.3g}")
            lbl.setStyleSheet(f"color: {NEON_GREEN}; font-size: 13px; margin-top: 4px;")
            lbl.setToolTip(interv_tooltips.get(param, label))
            interv_box.addWidget(lbl)
            slider = QSlider(Qt.Horizontal)
            slider.setMinimum(int(min_val * 100))
            slider.setMaximum(int(max_val * 100))
            slider.setValue(int(default * 100))
            slider.setMinimumHeight(22)
            slider.setToolTip(interv_tooltips.get(param, label))
            slider.valueChanged.connect(
                lambda val, p=param, l=lbl, label=label: self.update_param(p, val/100, l, label)
            )
            interv_box.addWidget(slider)
            self.sliders[param] = (slider, lbl, label)
        left_layout.addWidget(interv_box)

        # === COMMUNITY PARAMETERS (Contextual - only shown in Communities mode) ===
        self.community_box = CollapsibleBox("COMMUNITY PARAMETERS")
        self.collapsible_boxes.append(self.community_box)

        community_tooltips = {
            'num_per_community': """Particles Per Community: Population size in each community tile

Recommended: 50-100
• Lower (20-50): Small isolated groups
• Medium (50-100): Realistic community sizes
• Higher (100-200): Large population centers

Tip: Total population = 9 communities × this value""",

            'travel_probability': """Travel Probability: Daily chance for particle to travel between communities

Recommended: 1-5%
• Low (0-1%): Rare travel, strong isolation
• Medium (1-5%): Occasional inter-community mixing
• High (5-20%): Frequent travel, weak isolation
• Very High (20-100%): Constant mixing

Tip: Controls speed of geographic spread""",

            'communities_to_infect': """Initially Infected Communities: Number of communities with patient zero

Recommended: 1-3
• 1: Single outbreak origin
• 2-3: Multiple simultaneous outbreaks
• 4-9: Widespread initial infection

Tip: Models multiple introduction events"""
        }

        # Particles Per Community - INTEGER slider
        num_lbl = QLabel(f"Particles Per Community: {params.num_per_community}")
        num_lbl.setStyleSheet(f"color: {NEON_GREEN}; font-size: 13px; margin-top: 4px;")
        num_lbl.setToolTip(community_tooltips['num_per_community'])
        self.community_box.addWidget(num_lbl)
        num_slider = QSlider(Qt.Horizontal)
        num_slider.setMinimum(20)
        num_slider.setMaximum(200)
        num_slider.setValue(params.num_per_community)
        num_slider.setMinimumHeight(22)
        num_slider.setToolTip(community_tooltips['num_per_community'])
        num_slider.valueChanged.connect(
            lambda val, l=num_lbl: self.update_param('num_per_community', val, l, 'Particles Per Community', is_int=True)
        )
        self.community_box.addWidget(num_slider)
        self.sliders['num_per_community'] = (num_slider, num_lbl, 'Particles Per Community')

        # Travel Probability - PERCENTAGE slider (0-100%)
        travel_lbl = QLabel(f"Travel Probability: {params.travel_probability*100:.1f}%")
        travel_lbl.setStyleSheet(f"color: {NEON_GREEN}; font-size: 13px; margin-top: 4px;")
        travel_lbl.setToolTip(community_tooltips['travel_probability'])
        self.community_box.addWidget(travel_lbl)
        travel_slider = QSlider(Qt.Horizontal)
        travel_slider.setMinimum(0)
        travel_slider.setMaximum(100)
        travel_slider.setValue(int(params.travel_probability * 100))
        travel_slider.setMinimumHeight(22)
        travel_slider.setToolTip(community_tooltips['travel_probability'])
        travel_slider.valueChanged.connect(
            lambda val, l=travel_lbl: self.update_param('travel_probability', val/100, l, 'Travel Probability')
        )
        self.community_box.addWidget(travel_slider)
        self.sliders['travel_probability'] = (travel_slider, travel_lbl, 'Travel Probability')

        # Initially Infected Communities - INTEGER slider
        infect_lbl = QLabel(f"Initially Infected Communities: {params.communities_to_infect}")
        infect_lbl.setStyleSheet(f"color: {NEON_GREEN}; font-size: 13px; margin-top: 4px;")
        infect_lbl.setToolTip(community_tooltips['communities_to_infect'])
        self.community_box.addWidget(infect_lbl)
        infect_slider = QSlider(Qt.Horizontal)
        infect_slider.setMinimum(1)
        infect_slider.setMaximum(9)
        infect_slider.setValue(params.communities_to_infect)
        infect_slider.setMinimumHeight(22)
        infect_slider.setToolTip(community_tooltips['communities_to_infect'])
        infect_slider.valueChanged.connect(
            lambda val, l=infect_lbl: self.update_param('communities_to_infect', val, l, 'Initially Infected Communities', is_int=True)
        )
        self.community_box.addWidget(infect_slider)
        self.sliders['communities_to_infect'] = (infect_slider, infect_lbl, 'Initially Infected Communities')

        left_layout.addWidget(self.community_box)
        self.community_box.hide()  # Hidden by default, shown only in communities mode

        # === QUARANTINE PARAMETERS (Contextual - only shown when quarantine enabled) ===
        self.quarantine_params_box = CollapsibleBox("QUARANTINE PARAMETERS")
        self.collapsible_boxes.append(self.quarantine_params_box)

        quarantine_params = [
            ('quarantine_after', 'Quarantine After (days)', 1, 20, 5),
            ('start_quarantine', 'Quarantine Start Day', 0, 30, 10),
            ('quarantine_duration', 'Quarantine Duration (days)', 0, 50, 14),
            ('prob_no_symptoms', 'Asymptomatic Rate', 0, 0.5, 0.20),
        ]
        for param, label, min_val, max_val, default in quarantine_params:
            lbl = QLabel(f"{label}: {default:.3g}")
            lbl.setStyleSheet(f"color: {NEON_GREEN}; font-size: 13px; margin-top: 4px;")
            lbl.setToolTip(interv_tooltips.get(param, label))
            self.quarantine_params_box.addWidget(lbl)
            slider = QSlider(Qt.Horizontal)
            slider.setMinimum(int(min_val * 100))
            slider.setMaximum(int(max_val * 100))
            slider.setValue(int(default * 100))
            slider.setMinimumHeight(22)
            slider.setToolTip(interv_tooltips.get(param, label))
            slider.valueChanged.connect(
                lambda val, p=param, l=lbl, label=label: self.update_param(p, val/100, l, label)
            )
            self.quarantine_params_box.addWidget(slider)
            self.sliders[param] = (slider, lbl, label)
        left_layout.addWidget(self.quarantine_params_box)
        self.quarantine_params_box.hide()  # Hidden by default, shown when quarantine enabled

        # === MARKETPLACE PARAMETERS (Contextual - only shown when marketplace enabled) ===
        self.marketplace_params_box = CollapsibleBox("MARKETPLACE PARAMETERS")
        self.collapsible_boxes.append(self.marketplace_params_box)

        marketplace_tooltips = {
            'marketplace_interval': """Marketplace Interval: Days between gathering events

Recommended: 7-14
• Frequent (1-7): Daily to weekly gatherings
• Medium (7-14): Weekly to biweekly events
• Rare (14-30): Monthly gatherings

Tip: More frequent = higher impact on spread""",

            'marketplace_duration': """Marketplace Duration: Time steps particles stay at gathering

Recommended: 1-5
• Short (1-2): Brief encounters
• Medium (2-5): Extended mixing
• Long (5-10): Prolonged contact

Tip: Longer duration = more infections per event""",

            'marketplace_attendance': """Marketplace Attendance: Fraction of population attending

Recommended: 0.3-0.7
• Low (0.1-0.3): Small gatherings
• Medium (0.3-0.7): Moderate attendance
• High (0.7-1.0): Mass gathering events

Tip: Higher attendance = superspreader potential""",

            'marketplace_x': """Marketplace X Coordinate: Horizontal location of gathering point

Range: -1.0 to 1.0
• -1.0: Left side of canvas
• 0.0: Center (default)
• 1.0: Right side

Tip: (0, 0) places marketplace at canvas center""",

            'marketplace_y': """Marketplace Y Coordinate: Vertical location of gathering point

Range: -1.0 to 1.0
• -1.0: Bottom of canvas
• 0.0: Center (default)
• 1.0: Top

Tip: (0, 0) places marketplace at canvas center"""
        }

        # Marketplace interval (integer spinbox)
        interval_lbl = QLabel(f"Marketplace Interval: {params.marketplace_interval}")
        interval_lbl.setStyleSheet(f"color: {NEON_GREEN}; font-size: 13px; margin-top: 4px;")
        interval_lbl.setToolTip(marketplace_tooltips['marketplace_interval'])
        self.marketplace_params_box.addWidget(interval_lbl)
        interval_slider = QSlider(Qt.Horizontal)
        interval_slider.setMinimum(1)
        interval_slider.setMaximum(30)
        interval_slider.setValue(params.marketplace_interval)
        interval_slider.setMinimumHeight(22)
        interval_slider.setToolTip(marketplace_tooltips['marketplace_interval'])
        interval_slider.valueChanged.connect(
            lambda val, l=interval_lbl: self.update_param('marketplace_interval', val, l, 'Marketplace Interval', is_int=True)
        )
        self.marketplace_params_box.addWidget(interval_slider)
        self.sliders['marketplace_interval'] = (interval_slider, interval_lbl, 'Marketplace Interval')

        # Marketplace duration (integer slider)
        duration_lbl = QLabel(f"Marketplace Duration: {params.marketplace_duration}")
        duration_lbl.setStyleSheet(f"color: {NEON_GREEN}; font-size: 13px; margin-top: 4px;")
        duration_lbl.setToolTip(marketplace_tooltips['marketplace_duration'])
        self.marketplace_params_box.addWidget(duration_lbl)
        duration_slider = QSlider(Qt.Horizontal)
        duration_slider.setMinimum(1)
        duration_slider.setMaximum(10)
        duration_slider.setValue(params.marketplace_duration)
        duration_slider.setMinimumHeight(22)
        duration_slider.setToolTip(marketplace_tooltips['marketplace_duration'])
        duration_slider.valueChanged.connect(
            lambda val, l=duration_lbl: self.update_param('marketplace_duration', val, l, 'Marketplace Duration', is_int=True)
        )
        self.marketplace_params_box.addWidget(duration_slider)
        self.sliders['marketplace_duration'] = (duration_slider, duration_lbl, 'Marketplace Duration')

        # Marketplace attendance (float slider)
        attendance_lbl = QLabel(f"Marketplace Attendance: {params.marketplace_attendance:.2f}")
        attendance_lbl.setStyleSheet(f"color: {NEON_GREEN}; font-size: 13px; margin-top: 4px;")
        attendance_lbl.setToolTip(marketplace_tooltips['marketplace_attendance'])
        self.marketplace_params_box.addWidget(attendance_lbl)
        attendance_slider = QSlider(Qt.Horizontal)
        attendance_slider.setMinimum(10)
        attendance_slider.setMaximum(100)
        attendance_slider.setValue(int(params.marketplace_attendance * 100))
        attendance_slider.setMinimumHeight(22)
        attendance_slider.setToolTip(marketplace_tooltips['marketplace_attendance'])
        attendance_slider.valueChanged.connect(
            lambda val, l=attendance_lbl: self.update_param('marketplace_attendance', val/100, l, 'Marketplace Attendance')
        )
        self.marketplace_params_box.addWidget(attendance_slider)
        self.sliders['marketplace_attendance'] = (attendance_slider, attendance_lbl, 'Marketplace Attendance')

        # Marketplace X coordinate (float slider)
        x_lbl = QLabel(f"Marketplace X: {params.marketplace_x:.2f}")
        x_lbl.setStyleSheet(f"color: {NEON_GREEN}; font-size: 13px; margin-top: 4px;")
        x_lbl.setToolTip(marketplace_tooltips['marketplace_x'])
        self.marketplace_params_box.addWidget(x_lbl)
        x_slider = QSlider(Qt.Horizontal)
        x_slider.setMinimum(-100)
        x_slider.setMaximum(100)
        x_slider.setValue(int(params.marketplace_x * 100))
        x_slider.setMinimumHeight(22)
        x_slider.setToolTip(marketplace_tooltips['marketplace_x'])
        x_slider.valueChanged.connect(
            lambda val, l=x_lbl: self.update_param('marketplace_x', val/100, l, 'Marketplace X')
        )
        self.marketplace_params_box.addWidget(x_slider)
        self.sliders['marketplace_x'] = (x_slider, x_lbl, 'Marketplace X')

        # Marketplace Y coordinate (float slider)
        y_lbl = QLabel(f"Marketplace Y: {params.marketplace_y:.2f}")
        y_lbl.setStyleSheet(f"color: {NEON_GREEN}; font-size: 13px; margin-top: 4px;")
        y_lbl.setToolTip(marketplace_tooltips['marketplace_y'])
        self.marketplace_params_box.addWidget(y_lbl)
        y_slider = QSlider(Qt.Horizontal)
        y_slider.setMinimum(-100)
        y_slider.setMaximum(100)
        y_slider.setValue(int(params.marketplace_y * 100))
        y_slider.setMinimumHeight(22)
        y_slider.setToolTip(marketplace_tooltips['marketplace_y'])
        y_slider.valueChanged.connect(
            lambda val, l=y_lbl: self.update_param('marketplace_y', val/100, l, 'Marketplace Y')
        )
        self.marketplace_params_box.addWidget(y_slider)
        self.sliders['marketplace_y'] = (y_slider, y_lbl, 'Marketplace Y')

        left_layout.addWidget(self.marketplace_params_box)
        self.marketplace_params_box.hide()  # Hidden by default, shown when marketplace enabled

        # PRESETS
        self.presets_box = CollapsibleBox("PRESETS")
        self.collapsible_boxes.append(self.presets_box)
        self.preset_combo = QComboBox()
        self.preset_combo.addItem("-- Select Preset --")
        for preset_name in PRESETS.keys():
            self.preset_combo.addItem(preset_name)
        self.preset_combo.currentTextChanged.connect(self.load_preset)
        self.preset_combo.setToolTip("""Preset Scenarios: Pre-configured parameter sets for common epidemic scenarios

Available presets:
• Baseline: No interventions, natural spread
• Lockdown: Strict quarantine measures
• Social Distance: Population-wide distancing
• High Mortality: Severe disease scenario
• Fast Spread: Highly contagious disease
• Communities: Isolated population groups

Tip: Use keyboard shortcuts 1-9 to quickly load presets""")
        self.presets_box.addWidget(self.preset_combo)
        left_layout.addWidget(self.presets_box)

        left_layout.addStretch()

        main_layout.addWidget(left_scroll)

        # === CENTER: CANVAS ===
        self.canvas = SimulationCanvas(self.sim)
        # Disable tooltips on canvas to prevent flickering from 60 FPS repaints
        self.canvas.setAttribute(Qt.WA_AlwaysShowToolTips, False)
        main_layout.addWidget(self.canvas, 5)

        # === RIGHT PANEL: CONTROLS ===
        self.right_panel = QWidget()
        self.right_panel.setStyleSheet(f"background-color: {BG_BLACK};")
        self.right_panel.setMaximumWidth(400)
        self.right_panel.setMinimumWidth(350)

        right_scroll = QScrollArea()
        right_scroll.setWidgetResizable(True)
        right_scroll.setWidget(self.right_panel)
        right_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        right_scroll.setStyleSheet(f"""
            QScrollArea {{ border: none; background-color: {BG_BLACK}; border-left: 2px solid {BORDER_GREEN}; }}
            QScrollBar:vertical {{
                background-color: {PANEL_BLACK}; width: 12px;
                border: 1px solid {BORDER_GREEN};
            }}
            QScrollBar::handle:vertical {{
                background-color: {BORDER_GREEN}; min-height: 20px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """)

        right_layout = QVBoxLayout(self.right_panel)
        right_layout.setSpacing(10)
        right_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.addWidget(right_scroll, 2)

        # === TITLE & THEME TOGGLE ===
        title_container = QWidget()
        title_container.setStyleSheet(f"background-color: {PANEL_BLACK}; border: 2px solid {BORDER_GREEN};")
        title_layout = QHBoxLayout(title_container)
        title_layout.setContentsMargins(8, 8, 8, 8)
        title_layout.setSpacing(10)

        title = QLabel("EPIDEMIC SIMULATOR v3.0")
        title.setStyleSheet(f"""
            font-size: 16px; font-weight: bold; color: {NEON_GREEN};
            font-family: 'Courier New', monospace;
            background-color: transparent; border: none;
        """)
        title.setAlignment(Qt.AlignCenter)
        title.setMinimumWidth(300)  # Ensure title has enough width to display fully
        title_layout.addWidget(title, 1)

        # Removed: Theme toggle and font size buttons (not working properly)

        right_layout.addWidget(title_container)

        # === CONTROLS ===
        self.ctrl_group = QWidget()
        self.ctrl_group.setStyleSheet(f"background-color: {PANEL_BLACK}; border: 2px solid {BORDER_GREEN}; padding: 8px;")
        ctrl_layout = QVBoxLayout(self.ctrl_group)
        ctrl_layout.setSpacing(8)

        # Control buttons
        btn_row = QHBoxLayout()
        btn_row.setSpacing(4)

        self.pause_btn = QPushButton("START")
        self.pause_btn.clicked.connect(self.toggle_pause)
        self.pause_btn.setMinimumHeight(32)
        self.pause_btn.setToolTip("Start/Pause simulation (Keyboard: SPACE)\n\nStarts or pauses the simulation.\nUse to configure parameters before starting or examine current situation.")
        btn_row.addWidget(self.pause_btn)

        reset_btn = QPushButton("RESET")
        reset_btn.clicked.connect(self.reset_sim)
        reset_btn.setMinimumHeight(32)
        reset_btn.setToolTip("Reset simulation (Keyboard: R)\n\nResets simulation to day 0 with current parameters.\nCreates new particle population with random positions.")
        btn_row.addWidget(reset_btn)

        self.mode_btn = QPushButton("ADVANCED")
        self.mode_btn.setToolTip("Toggle BASIC/ADVANCED mode (Keyboard: B)\n\nBASIC: Simple controls, visible infection radius\nADVANCED: All parameters and features")
        self.mode_btn.clicked.connect(self.toggle_mode)
        self.mode_btn.setMinimumHeight(32)
        self.mode_btn.setMaximumWidth(90)
        btn_row.addWidget(self.mode_btn)

        ctrl_layout.addLayout(btn_row)

        # Speed buttons
        self.speed_label = QLabel("Speed:")
        self.speed_label.setStyleSheet(f"color: {NEON_GREEN}; font-size: 13px; margin-top: 5px;")
        self.speed_label.setToolTip("Simulation speed multiplier\n\nControls how fast time progresses.\nDoes not affect physics or disease mechanics.")
        ctrl_layout.addWidget(self.speed_label)

        speed_row = QHBoxLayout()
        speed_row.setSpacing(4)
        self.speed_btns = QButtonGroup()
        self.speed_btns.setExclusive(True)
        speed_tooltips = {
            0.5: "Half speed (0.5x)\n\nSlow motion for detailed observation.\nIdeal for studying individual interactions.",
            1.0: "Normal speed (1.0x)\n\nDefault simulation speed.\nBalanced between detail and progress.",
            2.0: "Double speed (2.0x)\n\nFaster progression through epidemic stages.\nGood for long-term trend observation.",
            5.0: "5x speed (5.0x)\n\nRapid progression to see full epidemic curve.\nSkips early stages quickly."
        }
        for i, speed in enumerate([0.5, 1.0, 2.0, 5.0]):
            btn = QPushButton(f"{speed}x")
            btn.setCheckable(True)
            btn.setStyleSheet(self.get_checkable_button_stylesheet())  # Apply checkable button style
            btn.clicked.connect(lambda checked, s=speed: self.set_speed(s))
            btn.setMinimumHeight(28)
            btn.setToolTip(speed_tooltips[speed])
            self.speed_btns.addButton(btn, i)
            speed_row.addWidget(btn)
            if speed == 1.0:
                btn.setChecked(True)
        ctrl_layout.addLayout(speed_row)

        # Population
        self.pop_label = QLabel("Population:")
        self.pop_label.setStyleSheet(f"color: {NEON_GREEN}; font-size: 13px; margin-top: 8px;")
        ctrl_layout.addWidget(self.pop_label)

        pop_row = QHBoxLayout()
        self.population_spin = QSpinBox()
        self.population_spin.setRange(50, 2000)
        self.population_spin.setValue(params.num_particles)
        self.population_spin.setSingleStep(50)
        self.population_spin.setMinimumHeight(28)
        self.population_spin.valueChanged.connect(self.on_population_changed)
        self.population_spin.setToolTip("""Population Size: Number of particles in simulation

Range: 50-2000 particles
• 50-200: Fast, good for testing
• 200-500: Balanced performance
• 500-1000: More realistic statistics
• 1000-2000: Highest detail (slower)

Requires clicking 'Apply' to take effect.""")
        pop_row.addWidget(self.population_spin)

        apply_pop_btn = QPushButton("Apply")
        apply_pop_btn.clicked.connect(self.apply_population)
        apply_pop_btn.setMinimumHeight(28)
        apply_pop_btn.setToolTip("Apply new population size\n\nResets the simulation with the new population.\nAll progress will be lost.")
        pop_row.addWidget(apply_pop_btn)
        ctrl_layout.addLayout(pop_row)

        right_layout.addWidget(self.ctrl_group)

        # === STATS ===
        self.stats_container = QWidget()
        self.stats_container.setStyleSheet(f"""
            background-color: {PANEL_BLACK}; border: 2px solid {NEON_GREEN}; padding: 10px;
        """)
        stats_layout = QVBoxLayout(self.stats_container)
        self.stats_label = QLabel("DAY: 0\nS: 100.0% | I: 0.0% | R: 0.0%")
        self.stats_label.setStyleSheet(f"""
            font-size: 16px; font-weight: bold; color: {NEON_GREEN};
            font-family: 'Courier New', monospace; background-color: transparent; border: none;
        """)
        self.stats_label.setAlignment(Qt.AlignCenter)
        self.stats_label.setToolTip("""Real-time epidemic statistics

DAY: Current simulation day
S (Susceptible): Healthy, can be infected
I (Infected): Currently infectious
R (Removed): Recovered or deceased

These percentages sum to 100% at all times (classic SIR model)""")
        stats_layout.addWidget(self.stats_label)
        right_layout.addWidget(self.stats_container)

        # === MODE ===
        mode_box = CollapsibleBox("SIMULATION MODE")
        self.collapsible_boxes.append(mode_box)
        self.mode_btns = QButtonGroup()

        mode_tooltips = {
            'simple': """Simple Mode: Single well-mixed population

All particles move freely in one shared space.
No barriers or separation between groups.
Fastest spread dynamics.

Use for: Baseline epidemic behavior, teaching basic SIR model""",

            'communities': """Communities Mode: Multiple isolated population groups

Population divided into separate communities.
Occasional travel between communities spreads disease.
Slower inter-community transmission.

Use for: Geographic spread modeling, travel restrictions"""
        }

        for i, mode in enumerate(['simple', 'communities']):
            btn = QPushButton(mode.upper())
            btn.setCheckable(True)
            btn.setStyleSheet(self.get_checkable_button_stylesheet())  # Apply checkable button style
            btn.clicked.connect(lambda checked, m=mode: self.change_mode(m))
            btn.setMinimumHeight(34)
            btn.setToolTip(mode_tooltips[mode])
            self.mode_btns.addButton(btn, i)
            mode_box.addWidget(btn)
        self.mode_btns.button(0).setChecked(True)
        right_layout.addWidget(mode_box)

        # === INTERVENTIONS ===
        interv_box = CollapsibleBox("INTERVENTIONS")
        self.collapsible_boxes.append(interv_box)

        self.quarantine_checkbox = QCheckBox("Quarantine Zone")
        self.quarantine_checkbox.setChecked(params.quarantine_enabled)
        self.quarantine_checkbox.stateChanged.connect(self.toggle_quarantine)
        self.quarantine_checkbox.setToolTip("""Quarantine Zone: Enable/disable quarantine isolation (Keyboard: Q)

When enabled:
• Symptomatic infected particles move to right side
• Quarantined particles cannot infect main population
• Asymptomatic cases remain in main population

Use for: Testing isolation effectiveness, intervention strategies""")
        self.interventions_box.addWidget(self.quarantine_checkbox)

        self.marketplace_checkbox = QCheckBox("Marketplace Gatherings")
        self.marketplace_checkbox.setChecked(params.marketplace_enabled)
        self.marketplace_checkbox.stateChanged.connect(self.toggle_marketplace)
        self.marketplace_checkbox.setToolTip("""Marketplace Gatherings: Periodic mass gathering events (Keyboard: M)

When enabled:
• Particles periodically gather at central marketplace
• Dramatically increases contact rate during event
• Models superspreader events (concerts, festivals, etc.)

Use for: Studying impact of mass gatherings on epidemic spread""")
        self.interventions_box.addWidget(self.marketplace_checkbox)

        # Note: Marketplace parameters (interval, attendance, location) are now in the left panel
        # under "MARKETPLACE PARAMETERS" section, shown only when marketplace is enabled.

        right_layout.addWidget(self.interventions_box)

        # === VISUALIZATIONS ===
        vis_box = CollapsibleBox("VISUALIZATIONS")
        self.collapsible_boxes.append(vis_box)
        # Start expanded (not collapsed) - graphs should be visible!

        # Infection radius visibility toggle
        self.show_radius_checkbox = QCheckBox("Show Infection Radius")
        self.show_radius_checkbox.setChecked(params.show_infection_radius)
        self.show_radius_checkbox.stateChanged.connect(self.toggle_infection_radius)
        self.show_radius_checkbox.setToolTip("Display red circles around infected particles showing infection range")
        vis_box.addWidget(self.show_radius_checkbox)

        vis_tabs = QTabWidget()
        vis_tabs.setMinimumHeight(300)  # Reasonable height for charts
        vis_tabs.setToolTip("Epidemic visualization graphs\n\nTIME SERIES: S/I/R percentages over time\nPIE CHART: Current population distribution")
        vis_tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 2px solid {BORDER_GREEN}; background-color: {BG_BLACK};
            }}
            QTabBar::tab {{
                background-color: {PANEL_BLACK}; color: {NEON_GREEN};
                border: 1px solid {BORDER_GREEN}; padding: 8px 15px;
                margin-right: 2px; font-family: 'Courier New', monospace; font-size: 13px;
            }}
            QTabBar::tab:selected {{
                background-color: {BORDER_GREEN}; color: {BG_BLACK}; font-weight: bold;
            }}
            QTabBar::tab:hover {{ background-color: {get_color('HOVER_BG')}; }}
        """)

        # Graph
        self.graph_widget = pg.PlotWidget()
        # DISABLE mouse interactions - prevent accidental zoom/pan that breaks the view
        self.graph_widget.setMouseEnabled(x=False, y=False)
        self.graph_widget.getViewBox().setMenuEnabled(False)  # Disable right-click menu

        self.graph_widget.setBackground(BG_BLACK)
        self.graph_widget.setLabel('left', '% Population', color=NEON_GREEN)
        self.graph_widget.setLabel('bottom', 'Day', color=NEON_GREEN)
        self.graph_widget.showGrid(x=True, y=True, alpha=0.15)
        self.graph_widget.setYRange(0, 100)
        self.graph_widget.setMinimumHeight(280)  # Reasonable height
        self.graph_widget.setToolTip("""Time Series Graph: Track epidemic progression over time

Shows percentage of population in each state:
• Blue (Cyan): Susceptible - healthy, can be infected
• Red: Infected - currently infectious
• Green: Removed - recovered or deceased

Watch for:
• Peak infection rate (epidemic peak)
• Final size (total affected)
• Curve shape (exponential growth, plateau, decline)""")

        for side in ['left', 'bottom', 'right', 'top']:
            axis = self.graph_widget.getAxis(side)
            axis.setPen(pg.mkPen(color=BORDER_GREEN, width=2))
            axis.setTextPen(NEON_GREEN)

        legend = self.graph_widget.addLegend(offset=(10, 10))
        legend.setBrush(pg.mkBrush(color=(10, 10, 10, 200)))
        legend.setPen(pg.mkPen(color=BORDER_GREEN, width=1))

        self.pie_chart = PieChartWidget(parent=self, width=3.8, height=3.8, dpi=80)
        self.pie_chart.setMinimumHeight(250)
        self.pie_chart.setToolTip("""Pie Chart: Current population distribution snapshot

Shows current state of entire population:
• Blue: Susceptible (healthy)
• Red: Infected (currently infectious)
• Green: Removed (recovered/deceased)

Updates in real-time as simulation progresses.""")

        vis_tabs.addTab(self.graph_widget, "TIME SERIES")
        vis_tabs.addTab(self.pie_chart, "PIE CHART")

        vis_box.addWidget(vis_tabs)
        right_layout.addWidget(vis_box)

        # === STATUS ===
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet(f"""
            font-size: 13px; padding: 8px; color: {NEON_GREEN};
            background-color: {PANEL_BLACK}; border: 1px solid {BORDER_GREEN};
            font-family: 'Courier New', monospace;
        """)
        self.status_label.setWordWrap(True)
        right_layout.addWidget(self.status_label)

        # === SHORTCUTS ===
        self.shortcuts_label = QLabel(
            "SHORTCUTS: SPACE=Pause | R=Reset | Ctrl+R=Docs | F=Fullscreen\n"
            "Q=Quarantine | M=Marketplace | Alt+T=Theme | 1-9=Presets"
        )
        self.shortcuts_label.setStyleSheet(f"""
            font-size: 11px; padding: 5px; color: {NEON_GREEN};
            background-color: {BG_BLACK}; border: 1px solid {BORDER_GREEN};
            font-family: 'Courier New', monospace;
        """)
        self.shortcuts_label.setWordWrap(True)
        right_layout.addWidget(self.shortcuts_label)

        # === HELP BUTTON ===
        help_btn = QPushButton("PARAMETER DOCUMENTATION (HELP)")
        help_btn.setToolTip("Click to view comprehensive documentation for ALL parameters\nIncludes: Distributions, Disease params, Interventions, and more")
        help_btn.clicked.connect(self.show_parameter_documentation)
        help_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {BORDER_GREEN};
                color: #000000;
                border: 2px solid {NEON_GREEN};
                padding: 12px;
                font-weight: bold;
                font-family: 'Courier New', monospace;
                font-size: 12px;
                margin-top: 5px;
            }}
            QPushButton:hover {{
                background-color: {NEON_GREEN};
                border: 2px solid #ffffff;
            }}
        """)
        right_layout.addWidget(help_btn)

        right_layout.addStretch()

        self.apply_theme()

        # Initialize contextual parameter visibility based on current state
        self._init_contextual_visibility()

        # Apply initial mode visibility
        self.update_mode_visibility()

    def get_checkable_button_stylesheet(self):
        """
        Generate stylesheet for checkable buttons with proper checked state colors.

        Returns:
            str: CSS stylesheet for checkable buttons adapted to current theme
        """
        if theme_module.current_theme == LIGHT_THEME:
            return f"""
                QPushButton {{
                    background-color: {get_color('BG_WHITE')};
                    color: {get_color('TEXT')};
                    border: 2px solid {get_color('BORDER_GRAY')};
                    padding: 8px;
                    font-weight: bold;
                    font-family: 'Courier New', monospace;
                }}
                QPushButton:hover {{
                    background-color: {get_color('HOVER_BG')};
                    border-color: {get_color('SECONDARY')};
                    color: {get_color('TEXT')};
                }}
                QPushButton:checked {{
                    background-color: {get_color('SECONDARY')} !important;
                    color: {get_color('TEXT')} !important;
                    border: 2px solid {get_color('PRIMARY')} !important;
                    font-weight: bold;
                }}
                QPushButton:checked:hover {{
                    background-color: {get_color('PRIMARY')} !important;
                    color: #ffffff !important;
                    border: 2px solid {get_color('PRIMARY')} !important;
                }}
            """
        else:  # Dark theme
            return f"""
                QPushButton {{
                    background-color: {BG_BLACK};
                    color: {NEON_GREEN};
                    border: 2px solid {BORDER_GREEN};
                    padding: 8px;
                    font-weight: bold;
                    font-family: 'Courier New', monospace;
                }}
                QPushButton:hover {{
                    background-color: #1a1a1a;
                    border-color: #ffffff;
                    color: #ffffff;
                }}
                QPushButton:checked {{
                    background-color: #00ff00 !important;
                    color: #000000 !important;
                    border: 2px solid #00ff00 !important;
                    font-weight: bold;
                }}
                QPushButton:checked:hover {{
                    background-color: #00dd00 !important;
                    color: #000000 !important;
                    border: 2px solid #00dd00 !important;
                }}
            """

    def toggle_left_panel(self):
        """Toggle left parameter panel visibility."""
        is_visible = self.left_panel.parent().isVisible()
        self.left_panel.parent().setVisible(not is_visible)
        if is_visible:
            self.left_collapse_btn.setText("SHOW PARAMETERS >>")
        else:
            self.left_collapse_btn.setText("COLLAPSE PARAMETERS <<")

    def on_population_changed(self, value):
        """Update status when population changes."""
        self.status_label.setText(f"Population set to {value}. Click 'Apply' to update.")

    def apply_population(self):
        """Apply new population size and reset simulation."""
        new_pop = self.population_spin.value()
        params.num_particles = new_pop
        self.reset_sim()
        self.status_label.setText(f"Population changed to {new_pop}")

    def apply_theme(self):
        """Apply current theme to all UI elements with appropriate colors and styles."""
        # Dynamic hover colors based on theme
        if theme_module.current_theme == LIGHT_THEME:
            hover_bg = get_color('HOVER_BG')  # Soft green-gray
            hover_border = get_color('SECONDARY')  # Soft green
            hover_text = get_color('TEXT')  # Dark green-gray text
            checked_bg = get_color('SECONDARY')  # Soft green when checked
            checked_text = get_color('TEXT')  # Dark text when checked
            checked_border = get_color('PRIMARY')  # Muted sage border when checked
            checked_hover_bg = get_color('PRIMARY')  # Darker sage on hover
            # Tooltip colors for light mode
            tooltip_bg = get_color('TOOLTIP_BG')  # Soft mint
            tooltip_text = get_color('TOOLTIP_TEXT')  # Dark green-gray
            tooltip_border = get_color('TOOLTIP_BORDER')  # Soft green
        else:  # Dark theme
            hover_bg = "#1a1a1a"  # Dark gray
            hover_border = "#ffffff"  # White
            hover_text = "#ffffff"  # White
            checked_bg = "#00ff00"  # Neon green background when checked
            checked_text = "#000000"  # Black text when checked (max contrast)
            checked_border = "#00ff00"  # Neon green border when checked
            checked_hover_bg = "#00dd00"  # Bright green on hover
            # Tooltip colors for dark mode
            tooltip_bg = "#1a1a1a"  # Dark gray background
            tooltip_text = "#00ff00"  # Neon green text
            tooltip_border = "#00aa00"  # Green border

        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {BG_BLACK};
            }}
            QWidget {{
                background-color: {PANEL_BLACK};
                color: {NEON_GREEN};
                font-family: 'Courier New', monospace;
            }}
            QToolTip {{
                background-color: {tooltip_bg};
                color: {tooltip_text};
                border: 2px solid {tooltip_border};
                padding: 8px;
                margin: 0px;
                font-family: 'Courier New', monospace;
                font-size: 13px;
                opacity: 255;
            }}
            QScrollArea {{
                border: 2px solid {BORDER_GREEN};
            }}
            QComboBox {{
                background-color: {BG_BLACK};
                color: {NEON_GREEN};
                border: 2px solid {BORDER_GREEN};
                padding: 5px;
                font-size: 12px;
            }}
            QComboBox::drop-down {{
                border: 0px;
            }}
            QComboBox::down-arrow {{
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid {NEON_GREEN};
            }}
            QComboBox QAbstractItemView {{
                background-color: {BG_BLACK};
                color: {NEON_GREEN};
                selection-background-color: {BORDER_GREEN};
                border: 2px solid {BORDER_GREEN};
            }}
            QGroupBox {{
                color: {NEON_GREEN};
                border: 2px solid {BORDER_GREEN};
                border-radius: 0px;
                margin-top: 10px;
                font-weight: bold;
                font-size: 14px;
                padding-top: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }}
            QPushButton {{
                background-color: {BG_BLACK};
                color: {NEON_GREEN};
                border: 2px solid {BORDER_GREEN};
                padding: 10px;
                font-weight: bold;
                font-family: 'Courier New', monospace;
                font-size: 13px;
                min-height: 20px;
            }}
            QPushButton:hover {{
                background-color: {hover_bg};
                border-color: {hover_border};
                border-width: 2px;
                color: {hover_text};
            }}
            QPushButton:pressed {{
                background-color: {BORDER_GREEN};
                border: 2px solid {NEON_GREEN};
                padding: 10px;
            }}
            QPushButton:checked {{
                background-color: {checked_bg};
                color: {checked_text};
                border: 2px solid {checked_border};
                font-weight: bold;
                padding: 10px;
            }}
            QPushButton:checked:hover {{
                background-color: {checked_hover_bg};
                border: 2px solid {hover_border};
                color: {checked_text};
                padding: 10px;
            }}
            QPushButton:checked:pressed {{
                background-color: {checked_bg};
                color: {checked_text};
                border: 2px solid {checked_border};
                padding: 10px;
            }}
            QLabel {{
                color: {NEON_GREEN};
                font-family: 'Courier New', monospace;
            }}
            QTextEdit {{
                background-color: {BG_BLACK};
                color: {NEON_GREEN};
                border: 2px solid {BORDER_GREEN};
                font-family: 'Courier New', monospace;
                font-size: 13px;
            }}
            QSlider::groove:horizontal {{
                border: 1px solid {BORDER_GREEN};
                height: 4px;
                background: {BG_BLACK};
            }}
            QSlider::handle:horizontal {{
                background: {NEON_GREEN};
                border: 1px solid {BORDER_GREEN};
                width: 14px;
                margin: -5px 0;
            }}
            QCheckBox {{
                color: {NEON_GREEN};
                font-family: 'Courier New', monospace;
                font-size: 13px;
                font-weight: bold;
                spacing: 8px;
            }}
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
                border: 2px solid {BORDER_GREEN};
                background-color: {BG_BLACK};
            }}
            QCheckBox::indicator:checked {{
                background-color: {NEON_GREEN};
                border: 2px solid {NEON_GREEN};
            }}
            QCheckBox::indicator:hover {{
                border: 2px solid {NEON_GREEN};
            }}
            QSpinBox, QDoubleSpinBox {{
                background-color: {BG_BLACK};
                color: {NEON_GREEN};
                border: 2px solid {BORDER_GREEN};
                padding: 3px;
                font-family: 'Courier New', monospace;
                font-size: 13px;
            }}
            QSpinBox::up-button, QDoubleSpinBox::up-button {{
                background-color: {PANEL_BLACK};
                border-left: 1px solid {BORDER_GREEN};
            }}
            QSpinBox::down-button, QDoubleSpinBox::down-button {{
                background-color: {PANEL_BLACK};
                border-left: 1px solid {BORDER_GREEN};
            }}
            QSpinBox::up-arrow, QDoubleSpinBox::up-arrow {{
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-bottom: 4px solid {NEON_GREEN};
            }}
            QSpinBox::down-arrow, QDoubleSpinBox::down-arrow {{
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 4px solid {NEON_GREEN};
            }}
        """)

    def load_preset(self, preset_name):
        """
        Load a preset configuration and update all parameters.

        Args:
            preset_name (str): Name of the preset to load
        """
        if preset_name == "-- Select Preset --":
            return

        if preset_name not in PRESETS:
            return

        preset = PRESETS[preset_name]

        # Update all parameters
        for param_name, value in preset.items():
            if param_name in self.sliders:
                slider, label, label_text = self.sliders[param_name]
                slider.setValue(int(value * 100))
                label.setText(f"{label_text}: {value:.2f}")
                setattr(params, param_name, value)

        # Reset simulation with new parameters
        self.reset_sim()
        self.sim.log(f"LOADED PRESET: {preset_name}")
        self.status_label.setText(f"✓ Loaded preset: {preset_name}. Simulation reset with new parameters.")

    def _init_contextual_visibility(self):
        """Initialize visibility of contextual parameter sections based on current state."""
        # Show/hide community parameters based on mode
        if self.sim.mode == 'communities':
            self.community_box.show()
        else:
            self.community_box.hide()

        # Show/hide quarantine parameters based on checkbox
        if params.quarantine_enabled:
            self.quarantine_params_box.show()
        else:
            self.quarantine_params_box.hide()

        # Show/hide marketplace parameters based on checkbox
        if params.marketplace_enabled:
            self.marketplace_params_box.show()
        else:
            self.marketplace_params_box.hide()

    def update_param(self, param, value, label, label_text, is_int=False):
        """
        Update a simulation parameter and its label.

        Args:
            param (str): Parameter name
            value (float): New parameter value
            label (QLabel): Label widget to update
            label_text (str): Label text prefix
            is_int (bool): Whether value should be displayed as integer
        """
        setattr(params, param, value)

        # Special handling for percentage parameters
        if param == 'travel_probability':
            label.setText(f"{label_text}: {value*100:.1f}%")
            self.status_label.setText(f"✓ {label_text} updated to {value*100:.1f}%")
        elif is_int:
            label.setText(f"{label_text}: {int(value)} (reset to apply)")
            self.status_label.setText(f"⚠ {label_text} changed to {int(value)}. Click RESET to apply.")
        else:
            label.setText(f"{label_text}: {value:.2f}")
            self.status_label.setText(f"✓ {label_text} updated to {value:.2f}")

    def change_mode(self, mode):
        """
        Change simulation mode and reset.
        Also show/hide contextual community parameters based on mode.

        Args:
            mode (str): New simulation mode ('simple', 'quarantine', or 'communities')
        """
        self.sim.mode = mode
        self.reset_sim()
        mode_names = {'simple': 'Simple', 'quarantine': 'Quarantine', 'communities': 'Communities'}
        self.status_label.setText(f"✓ Mode changed to: {mode_names.get(mode, mode)}")

        # Show/hide community parameters based on mode
        if mode == 'communities':
            self.community_box.show()
        else:
            self.community_box.hide()

    def toggle_quarantine(self, state):
        """
        Toggle quarantine on/off.
        Also show/hide contextual quarantine parameters and manage quarantine zone.

        Args:
            state (int): Qt checkbox state (0=unchecked, 2=checked)
        """
        params.quarantine_enabled = bool(state)

        # Show/hide quarantine parameters based on checkbox state
        if state:
            self.quarantine_params_box.show()
            self.status_label.setText("Quarantine enabled - zone will activate when criteria met")
        else:
            self.quarantine_params_box.hide()
            # Clear quarantine zone when disabled - move all quarantined particles back
            if self.sim.quarantine_particles:
                num_released = len(self.sim.quarantine_particles)
                # Move all quarantined particles back to main population
                if self.sim.mode == 'communities':
                    # In communities mode, distribute back to their home communities
                    for p in self.sim.quarantine_particles:
                        p.quarantined = False
                        # Find closest community and add particle there
                        # For simplicity, add to community 0
                        self.sim.communities[0]['particles'].append(p)
                else:
                    # In simple mode, move back to main particles list
                    for p in self.sim.quarantine_particles:
                        p.quarantined = False
                        self.sim.particles.append(p)

                # Clear the quarantine zone
                self.sim.quarantine_particles.clear()
                self.status_label.setText(f"Quarantine disabled - {num_released} particles released")
            else:
                self.status_label.setText("Quarantine disabled")

        # Force canvas redraw to show/hide quarantine zone
        self.canvas.update()

    def toggle_marketplace(self, state):
        """
        Toggle marketplace gatherings on/off.
        Also show/hide contextual marketplace parameters.

        Args:
            state (int): Qt checkbox state (0=unchecked, 2=checked)
        """
        params.marketplace_enabled = bool(state)
        self.status_label.setText(f"Marketplace {'enabled' if state else 'disabled'}")

        # Show/hide marketplace parameters based on checkbox state
        if state:
            self.marketplace_params_box.show()
        else:
            self.marketplace_params_box.hide()

    def toggle_infection_radius(self, state):
        """
        Toggle infection radius visualization.

        Args:
            state (int): Qt checkbox state (0=unchecked, 2=checked)
        """
        params.show_infection_radius = bool(state)
        self.canvas.update()  # Force redraw
        self.status_label.setText(f"Infection radius {'visible' if state else 'hidden'}")

    def load_theme(self, theme_name):
        """
        Load and apply a theme (dark or light).

        Args:
            theme_name (str): Theme name ('dark' or 'light')
        """
        from epidemic_sim.view import theme as theme_module
        if theme_name == "light":
            theme_module.current_theme = LIGHT_THEME
        else:
            theme_module.current_theme = DARK_THEME
        theme_module.update_legacy_colors()

    def toggle_theme(self):
        """Toggle between light and dark themes and save preference."""
        from epidemic_sim.view import theme as theme_module
        # Switch theme
        if theme_module.current_theme == DARK_THEME:
            theme_module.current_theme = LIGHT_THEME
            theme_name = "light"
            self.theme_btn.setText("DARK MODE")
        else:
            theme_module.current_theme = DARK_THEME
            theme_name = "dark"
            self.theme_btn.setText("LIGHT MODE")

        # Update legacy colors
        theme_module.update_legacy_colors()

        # Save preference
        self.settings.setValue("theme", theme_name)

        # Apply theme to all UI elements
        self.apply_theme()

        # Update panels with direct stylesheets
        from epidemic_sim.view.theme import BG_BLACK as BG, BORDER_GREEN as BORDER, NEON_GREEN as TEXT, PANEL_BLACK as PANEL
        self.left_panel.setStyleSheet(f"background-color: {BG};")
        self.right_panel.setStyleSheet(f"background-color: {BG};")

        # Update control panel background and borders
        self.ctrl_group.setStyleSheet(f"background-color: {PANEL}; border: 2px solid {BORDER}; padding: 8px;")

        # Update stats container background and borders
        self.stats_container.setStyleSheet(f"background-color: {PANEL}; border: 2px solid {BORDER}; padding: 10px;")

        # Update labels with theme-aware text colors
        self.speed_label.setStyleSheet(f"color: {TEXT}; font-size: 13px; margin-top: 5px;")
        self.pop_label.setStyleSheet(f"color: {TEXT}; font-size: 13px; margin-top: 8px;")
        self.stats_label.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {TEXT}; font-family: 'Courier New', monospace; background-color: transparent; border: none;")
        self.status_label.setStyleSheet(f"font-size: 13px; padding: 8px; color: {TEXT}; background-color: {PANEL}; border: 1px solid {BORDER}; font-family: 'Courier New', monospace;")
        self.shortcuts_label.setStyleSheet(f"font-size: 11px; padding: 5px; color: {TEXT}; background-color: {BG}; border: 1px solid {BORDER}; font-family: 'Courier New', monospace;")

        # Update all collapsible boxes
        for box in self.collapsible_boxes:
            box.update_theme()

        # Update canvas color cache for new theme
        self.canvas._update_color_cache()
        self.canvas.update()

        # Update graph colors
        self.graph_widget.setBackground(get_color('GRAPH_BG'))
        graph_grid_color = get_color('GRAPH_GRID')
        self.graph_widget.showGrid(x=True, y=True, alpha=graph_grid_color[3]/255.0)

        # Update all axes colors
        for side in ['left', 'bottom', 'right', 'top']:
            axis = self.graph_widget.getAxis(side)
            axis.setPen(pg.mkPen(color=get_color('BORDER_GRAY') if theme_module.current_theme == LIGHT_THEME else BORDER, width=2))
            axis.setTextPen(get_color('TEXT'))

        # Update pie chart
        self.pie_chart.fig.patch.set_facecolor(get_color('GRAPH_BG'))
        self.pie_chart.setStyleSheet(f"background-color: {get_color('GRAPH_BG')};")
        # Update pie chart axes
        if hasattr(self.pie_chart, 'axes'):
            self.pie_chart.axes.set_facecolor(get_color('GRAPH_BG'))
        self.pie_chart.draw()

        # Update all checkable button styles for new theme
        button_style = self.get_checkable_button_stylesheet()
        for i in range(self.speed_btns.buttons().__len__()):
            self.speed_btns.button(i).setStyleSheet(button_style)
        for i in range(self.mode_btns.buttons().__len__()):
            self.mode_btns.button(i).setStyleSheet(button_style)

        # Note: Tooltip styling is set once at startup to avoid flickering
        # DO NOT set global stylesheets here - it causes tooltip flicker on every theme change

        # Force full UI refresh
        self.status_label.setText(f"Theme switched to {theme_name.title()} mode")

    def toggle_fullscreen(self):
        """Toggle fullscreen mode by hiding/showing right panel."""
        self.right_panel.setVisible(not self.right_panel.isVisible())
        if not self.right_panel.isVisible():
            self.fullscreen_btn.setText("[X]")
            self.status_label.setText("Fullscreen mode (Press F to exit)")
        else:
            self.fullscreen_btn.setText("FULL")

    def toggle_mode(self):
        """Toggle between BASIC and ADVANCED mode."""
        self.mode = "ADVANCED" if self.mode == "BASIC" else "BASIC"
        self.mode_btn.setText("ADVANCED" if self.mode == "BASIC" else "BASIC")

        # Update parameter panel visibility
        self.update_mode_visibility()

        # In BASIC mode, enable infection radius by default
        if self.mode == "BASIC":
            params.show_infection_radius = True

        self.status_label.setText(f"Switched to {self.mode} mode")

    def update_mode_visibility(self):
        """Update visibility of parameter boxes based on current mode."""
        if self.mode == "BASIC":
            # BASIC mode: Hide advanced features (show only DISEASE PARAMETERS)
            self.pop_box.setVisible(False)
            self.interv_box.setVisible(False)
            self.presets_box.setVisible(False)
            self.interventions_box.setVisible(False)
            # Also hide community and marketplace param boxes
            if hasattr(self, 'community_box'):
                self.community_box.setVisible(False)
            if hasattr(self, 'marketplace_params_box'):
                self.marketplace_params_box.setVisible(False)
        else:
            # ADVANCED mode: Show all
            self.pop_box.setVisible(True)
            self.interv_box.setVisible(True)
            self.presets_box.setVisible(True)
            self.interventions_box.setVisible(True)
            # Community and marketplace boxes have their own visibility logic
            # so we don't force them visible here

    def toggle_tooltips(self):
        """Toggle tooltips on/off globally (Ctrl+T)."""
        self.tooltips_enabled = not self.tooltips_enabled

        if self.tooltips_enabled:
            # Enable tooltips with proper styling that respects current theme
            tooltip_bg = get_color('TOOLTIP_BG')
            tooltip_text = get_color('TOOLTIP_TEXT')
            tooltip_border = get_color('TOOLTIP_BORDER')
            QApplication.instance().setStyleSheet(f"""
                QToolTip {{
                    background-color: {tooltip_bg};
                    color: {tooltip_text};
                    border: 1px solid {tooltip_border};
                    padding: 5px;
                    border-radius: 3px;
                    font-size: 13px;
                }}
            """)
            self.add_log("Tooltips enabled (Ctrl+T)")
        else:
            # Disable tooltips by hiding them
            QApplication.instance().setStyleSheet("""
                QToolTip {
                    opacity: 0;
                    background-color: transparent;
                    border: none;
                }
            """)
            self.add_log("Tooltips disabled (Ctrl+T)")

    def adjust_font_size(self, delta):
        """
        Adjust the base font size of the application.

        Args:
            delta (int): Change in font size (+1 or -1)
        """
        if not hasattr(self, 'base_font_size'):
            self.base_font_size = 10  # Default size

        # Adjust size with limits (8-14)
        new_size = max(8, min(14, self.base_font_size + delta))

        if new_size == self.base_font_size:
            if delta > 0:
                self.status_label.setText("⚠ Maximum font size reached (14pt)")
            else:
                self.status_label.setText("⚠ Minimum font size reached (8pt)")
            return

        self.base_font_size = new_size

        # Apply new font to application - MUST preserve monospace retro "hacker" font!
        font = QFont("Courier New", self.base_font_size)
        font.setStyleHint(QFont.Monospace)  # Ensure monospace fallback
        font.setFamily("Courier New")  # Force Courier New
        QApplication.instance().setFont(font)

        # Save preference
        self.settings.setValue("font_size", self.base_font_size)

        self.status_label.setText(f"✓ Font size: {self.base_font_size}pt (Courier New preserved)")

    def toggle_pause(self):
        """Toggle simulation pause state."""
        self.paused = not self.paused
        self.pause_btn.setText("START" if self.paused else "PAUSE")
        if self.paused:
            self.status_label.setText(f"⏸ Simulation PAUSED at Day {self.sim.day_count}. Adjust parameters or press SPACE to resume.")
        else:
            self.status_label.setText(f"▶ Simulation RESUMED at {self.speed}x speed.")

    def reset_sim(self):
        """Reset simulation to initial state with current parameters."""
        self.sim.initialize()
        self.graph_widget.clear()

        # Adaptive performance optimization based on population size
        # More particles = skip more rendering frames
        if params.num_particles <= 200:
            self.skip_frames = 1  # Render every frame (60 FPS)
        elif params.num_particles <= 500:
            self.skip_frames = 2  # Render every 2nd frame (30 FPS)
        else:  # > 500 particles
            self.skip_frames = 3  # Render every 3rd frame (20 FPS)

        self.frame_count = 0
        self.status_label.setText(f"Simulation reset ({params.num_particles} particles, {60//self.skip_frames} FPS)")
        self.paused = False
        self.pause_btn.setText("PAUSE")

    def set_speed(self, speed):
        """
        Set simulation speed multiplier.

        Args:
            speed (float): Speed multiplier (0.5x to 5x)
        """
        self.speed = speed
        self.status_label.setText(f"Speed set to {speed}x")
        # Visual feedback - find and check the button
        for i, btn in enumerate(self.speed_btns.buttons()):
            if btn.text() == f"{speed}x":
                btn.setChecked(True)
                break

    def add_log(self, message):
        """
        Update status bar with important simulation events.

        Args:
            message (str): Log message from simulation
        """
        # Filter to show only important events
        important_keywords = ['INITIALIZING', 'PATIENT ZERO', 'PRESET', 'QUARANTINE', 'SPEED']
        if any(keyword in message for keyword in important_keywords):
            self.status_label.setText(message)

    def show_parameter_documentation(self):
        """
        Show comprehensive parameter documentation dialog (Ctrl+R).

        Displays detailed documentation for ALL simulation parameters including:
        - Disease parameters with epidemiological context
        - Population parameters with behavioral models
        - Intervention parameters with public health strategies
        - Community parameters for spatial modeling
        - Marketplace parameters for gathering dynamics
        - Statistical distributions and their mathematical justification
        """
        from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton
        from epidemic_sim.view.theme import get_color

        dialog = QDialog(self)
        dialog.setWindowTitle("Complete Parameter Documentation")
        dialog.setMinimumSize(1100, 800)  # Increased for better readability

        layout = QVBoxLayout()

        # Create scrollable text area
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setStyleSheet(f"""
            QTextEdit {{
                background-color: {get_color('BG_WHITE') if theme_module.current_theme == LIGHT_THEME else '#0a0a0a'};
                color: {get_color('TEXT')};
                font-family: 'Courier New', monospace;
                font-size: 13px;
                border: 2px solid {get_color('BORDER_GREEN') if theme_module.current_theme == DARK_THEME else get_color('BORDER_GRAY')};
                padding: 15px;
            }}
        """)

        # Comprehensive documentation content
        doc_text = f"""
╔════════════════════════════════════════════════════════════════════════════╗
║              EPIDEMIC SIMULATOR - COMPLETE PARAMETER GUIDE                 ║
║                    Scientific Documentation & Reference                     ║
╚════════════════════════════════════════════════════════════════════════════╝

Current Configuration: {self.sim.mode.upper()} MODE
Population: {params.num_particles} particles
Current Day: {self.sim.day_count}

═══════════════════════════════════════════════════════════════════════════════
STATISTICAL DISTRIBUTIONS (IHK Project Requirement)
═══════════════════════════════════════════════════════════════════════════════

The simulation implements THREE statistical distributions as required:

1. UNIFORM DISTRIBUTION (Gleichverteilung)
   ────────────────────────────────────────────────────────────────
   Mathematical Form:  f(x) = 1/(b-a) for x ∈ [a,b]

   Used For:
   • Particle initial positions (x, y) - Random spatial placement
   • Particle velocities (vx, vy) - Unbiased movement direction
   • Random travel decisions - No preference in community selection

   Parameters: Range [-0.2, 0.2] for velocities
   Justification: All values equally likely → No inherent bias in
                  position or movement direction

   Properties:
   • Mean = (a+b)/2 = 0.0
   • Variance = (b-a)²/12
   • Every value in range has equal probability

2. NORMAL DISTRIBUTION (Normalverteilung/Gaussian)
   ────────────────────────────────────────────────────────────────
   Mathematical Form:  f(x) = (1/σ√2π) * e^(-(x-μ)²/2σ²)

   Used For: Individual Infection Susceptibility

   Parameters:
   • Mean (μ) = 1.0 (average person)
   • Standard Deviation (σ) = 0.2 (biological variation)
   • Range: Clamped to [0.1, ∞) to avoid negative susceptibility

   Current Value: {1.0} (effective multiplier on infection probability)

   Justification: Models natural biological variation in immune response.
                  Most people cluster around average (68% within ±σ),
                  with few being highly susceptible or highly resistant.

   Properties:
   • ~68% of population has susceptibility between 0.8 and 1.2
   • ~95% of population has susceptibility between 0.6 and 1.4
   • Bell curve represents Central Limit Theorem in biology

3. EXPONENTIAL DISTRIBUTION (Exponentialverteilung)
   ────────────────────────────────────────────────────────────────
   Mathematical Form:  f(x) = λe^(-λx) for x ≥ 0

   Used For: Individual Recovery Time Variation

   Parameters:
   • Scale (λ) = 1.0, therefore Mean = 1/λ = 1.0
   • Range: Clamped to [0.5, 3.0] for realistic recovery times

   Current Value: {1.0} (effective multiplier on infection duration)

   Justification: Exponential distribution has "memoryless property"
                  which perfectly models time-until-event phenomena.
                  Some recover quickly (<1.0x), others take longer (>1.0x).
                  Ideal for disease progression modeling.

   Properties:
   • Median < Mean (right-skewed distribution)
   • P(recovery in next day) independent of days already infected
   • Models random time until recovery event occurs

═══════════════════════════════════════════════════════════════════════════════
DISEASE PARAMETERS (Epidemiological Model)
═══════════════════════════════════════════════════════════════════════════════

Infection Radius: {params.infection_radius:.3f}
   • Range: 0.01 - 0.40 (simulation units)
   • Current: {params.infection_radius:.3f}
   • Meaning: How close particles must be for disease transmission
   • Epidemiological Context: Represents "contact distance" for airborne/
                             droplet transmission (e.g., 1.5-2m in reality)
   • Effect: Larger radius → faster spread, more contacts per timestep
   • Recommendation: 0.10-0.20 for realistic airborne diseases

Infection Probability: {params.prob_infection:.1%}
   • Range: 0% - 100%
   • Current: {params.prob_infection:.1%} ({params.prob_infection:.3f})
   • Meaning: Chance of transmission per contact PER TIMESTEP
   • IMPORTANT: Adjusted by individual susceptibility (Normal distribution)
   • Formula: effective_prob = base_prob × susceptibility / steps_per_day
   • Epidemiological Context: R₀ (basic reproduction number) depends on:
                             infection_prob × contacts_per_day × infection_duration
   • Effect: Higher probability → more aggressive spread, higher R₀
   • Recommendation: 20-40% for moderate diseases like influenza

Infection Duration: {params.infection_duration:.1f} days
   • Range: 1 - 90 days
   • Current: {params.infection_duration:.1f} days
   • Meaning: How long a particle remains infectious
   • IMPORTANT: Adjusted by individual recovery modifier (Exponential distribution)
   • Formula: effective_duration = base_duration × recovery_modifier
   • Epidemiological Context: Matches typical disease infectious periods
                             (flu ~7 days, COVID-19 ~10-14 days)
   • Effect: Longer duration → more transmission opportunities per case
   • Recommendation: 7-21 days for most respiratory diseases

Asymptomatic Probability: {params.prob_no_symptoms:.1%}
   • Range: 0% - 100%
   • Current: {params.prob_no_symptoms:.1%}
   • Meaning: Percentage of infected who show NO symptoms
   • Epidemiological Context: Asymptomatic carriers crucial for COVID-19,
                             less common in symptomatic diseases like measles
   • Effect on Behavior: Asymptomatic → no quarantine even if enabled
   • Visualization: Orange particles (vs red symptomatic)
   • Recommendation: 20-40% for COVID-like diseases, 0-10% for measles

Mortality Rate: {params.mortality_rate:.1%}
   • Range: 0% - 100%
   • Current: {params.mortality_rate:.1%}
   • Meaning: Percentage of infected who DIE (vs recover)
   • Epidemiological Context: Case Fatality Rate (CFR)
   • Roll timing: When infection_duration expires
   • Effect: Dead particles stop moving, turn dark red
   • Historical Context: Spanish Flu ~2-3%, COVID-19 ~1-2%, Ebola ~50%
   • Recommendation: 0-5% for most modern diseases

═══════════════════════════════════════════════════════════════════════════════
POPULATION PARAMETERS (Behavioral Model)
═══════════════════════════════════════════════════════════════════════════════

Population Size: {params.num_particles}
   • Range: 50 - 5000 particles
   • Current: {params.num_particles}
   • Meaning: Total number of individuals in simulation
   • Performance Impact: >1000 may slow simulation on older machines
   • Recommendation: 200-500 for good visualization, 1000+ for statistics

Particle Size: {params.particle_size} pixels
   • Range: 2 - 12 pixels
   • Current: {params.particle_size} pixels
   • Meaning: Visual size of each particle on canvas
   • Effect: Larger → easier to see, but may overlap visually
   • Recommendation: 4-6 for 500 particles, 2-3 for 2000+ particles

Particle Speed: {params.speed_limit:.2f}
   • Range: 0.01 - 1.0
   • Current: {params.speed_limit:.2f}
   • Meaning: Maximum particle velocity
   • Effect: Higher speed → more contacts, faster mixing
   • Epidemiological Context: Represents population mobility
   • Recommendation: 0.05-0.15 for realistic movement

Social Distance Compliance: {params.social_distance_obedient:.1%}
   • Range: 0% - 100%
   • Current: {params.social_distance_obedient:.1%}
   • Meaning: % of population that practices social distancing
   • Behavior: Compliant particles keep ≥2x infection radius apart
   • Epidemiological Context: Models voluntary behavioral change
   • Effect: Higher compliance → slower spread, lower R₀
   • Recommendation: 0% (baseline), 60-80% (moderate intervention)

Initial Infected: {int(params.fraction_infected_init * params.num_particles)}
   • Range: Fraction: 0.0 - 1.0 (0% - 100%)
   • Current: {params.fraction_infected_init:.2%} = {int(params.fraction_infected_init * params.num_particles)} particles
   • Meaning: "Patient Zero" - fraction/number of infected at day 0
   • Epidemiological Context: Index cases that seed the outbreak
   • Effect: More initial → faster initial growth, less randomness
   • Recommendation: 0.5-2% for realistic outbreak, 5%+ for fast testing

═══════════════════════════════════════════════════════════════════════════════
INTERVENTION PARAMETERS (Public Health Strategies)
═══════════════════════════════════════════════════════════════════════════════

Quarantine Enabled: {params.quarantine_enabled}
   • Toggle: Keyboard 'Q' or checkbox
   • Current: {'ACTIVE' if params.quarantine_enabled else 'DISABLED'}
   • Meaning: Isolate symptomatic infected particles
   • Mechanism: Move to quarantine zone, reduce movement
   • Epidemiological Context: Historical quarantine (isolation of sick)
   • Effect: Reduces R₀ by removing infectious from circulation
   • Limitation: Only catches SYMPTOMATIC (misses asymptomatic)

Quarantine After: {params.quarantine_after} days
   • Range: 0 - 365 days
   • Current: {params.quarantine_after} days (if enabled)
   • Meaning: Days AFTER infection before quarantine begins
   • Epidemiological Context: Represents incubation + detection delay
   • Effect: 0 days = instant quarantine, 5-10 days = realistic delay
   • Recommendation: 5-10 days for COVID-like disease

Quarantine Duration: {params.quarantine_duration:.1f} days
   • Range: 5 - 90 days
   • Current: {params.quarantine_duration:.1f} days (if enabled)
   • Meaning: How long particles remain quarantined
   • Release: After duration OR recovery (whichever first)
   • Recommendation: Match or exceed infection_duration

Vaccination Enabled: {getattr(self.sim, 'vaccination_enabled', False)}
   • Toggle: Must reset simulation to enable
   • Current: {'ACTIVE' if getattr(self.sim, 'vaccination_enabled', False) else 'DISABLED'}
   • Meaning: Vaccinate susceptible particles over time
   • Mechanism: Reduces infection_susceptibility by vaccine_efficacy
   • Formula: new_susceptibility = old × (1 - efficacy)
   • Example: 70% efficacy → susceptibility reduced to 30% of original

Vaccine Efficacy: {getattr(self.sim, 'vaccine_efficacy', 0.0):.1%}
   • Range: 0% - 100%
   • Current: {getattr(self.sim, 'vaccine_efficacy', 0.0):.1%} (if vaccination enabled)
   • Meaning: How much vaccine REDUCES infection risk
   • Real-world: Pfizer/Moderna ~95%, AstraZeneca ~70%, flu ~40-60%
   • Effect: Higher efficacy → fewer vaccinated infections

Vaccination Rate: {getattr(self.sim, 'vaccination_rate', 0.0):.1%}/day
   • Range: 0% - 10%/day
   • Current: {getattr(self.sim, 'vaccination_rate', 0.0):.1%}/day (if enabled)
   • Meaning: % of susceptible population vaccinated per day
   • Example: 1%/day → 100 days to vaccinate all susceptible
   • Epidemiological Context: Represents vaccination campaign speed

═══════════════════════════════════════════════════════════════════════════════
COMMUNITY PARAMETERS (Spatial Modeling) - COMMUNITIES MODE ONLY
═══════════════════════════════════════════════════════════════════════════════

Particles per Community: {params.num_per_community}
   • Range: 50 - 500 per community
   • Current: {params.num_per_community}
   • Meaning: Population of each community in grid
   • Total Communities: 9 (3×3 grid)
   • Total Population: {params.num_per_community * 9}

Travel Probability: {params.travel_probability:.1%}
   • Range: 0% - 10%
   • Current: {params.travel_probability:.1%}
   • Meaning: Chance per timestep that particle travels to new community
   • Epidemiological Context: Models inter-community mixing
   • Effect: Higher travel → faster spatial spread, earlier epidemics in remote communities
   • Recommendation: 0.1-1% for low mobility, 3-5% for high mobility

Communities to Infect: {params.communities_to_infect}
   • Range: 1 - 9
   • Current: {params.communities_to_infect}
   • Meaning: How many communities start with infections
   • Pattern: Center community always infected first
   • Effect: More → simultaneous outbreaks, less spatial lag
   • Recommendation: 1 for single-source, 3-5 for multi-source outbreak

═══════════════════════════════════════════════════════════════════════════════
MARKETPLACE PARAMETERS (Mass Gathering Events)
═══════════════════════════════════════════════════════════════════════════════

Marketplace Enabled: {params.marketplace_enabled}
   • Toggle: Keyboard 'M' or checkbox
   • Current: {'ACTIVE' if params.marketplace_enabled else 'DISABLED'}
   • Meaning: Periodic gatherings at central location
   • Epidemiological Context: Super-spreader events (concerts, markets, etc.)
   • Effect: Creates transmission hotspots, increases R₀ during events

Marketplace Interval: {params.marketplace_interval:.1f} hours
   • Range: 6 - 168 hours (0.25 - 7 days)
   • Current: {params.marketplace_interval:.1f} hours = {params.marketplace_interval/24:.1f} days
   • Meaning: Time between marketplace events
   • Example: 24 hours = daily market, 168 hours = weekly event
   • Recommendation: 24-48 hours for frequent, 168 for rare events

Marketplace Duration: {params.marketplace_duration:.1f} hours
   • Range: 0.5 - 24 hours
   • Current: {params.marketplace_duration:.1f} hours
   • Meaning: How long each gathering lasts
   • Epidemiological Context: Longer events → more transmission opportunities
   • Recommendation: 2-4 hours for market, 8-12 for festival

Marketplace Attendance: {params.marketplace_attendance:.1%}
   • Range: 0% - 100%
   • Current: {params.marketplace_attendance:.1%}
   • Meaning: % of population attending each event
   • Selection: Random each time (Uniform distribution)
   • Effect: Higher attendance → more mixing, super-spreader potential
   • Recommendation: 20-40% for routine events, 60-80% for major gatherings

Marketplace Location:
   • X: {params.marketplace_x:.2f}, Y: {params.marketplace_y:.2f}
   • Simple Mode: Center of simulation space
   • Communities Mode: Center community in grid
   • Visual: Orange circle (simple) or orange community border

═══════════════════════════════════════════════════════════════════════════════
SIMULATION SETTINGS (Technical)
═══════════════════════════════════════════════════════════════════════════════

Time Steps per Day: {params.time_steps_per_day}
   • Current: {params.time_steps_per_day} steps = {24/params.time_steps_per_day:.1f} hours/step
   • Meaning: Time resolution of simulation
   • Effect on Calculations: Infection probability DIVIDED by this value
   • Recommendation: Keep at 24 for balance of speed and accuracy

Simulation Speed: {self.speed}x
   • Current: {self.speed}x (real-time multiplier)
   • Effect: Visual only - does NOT change disease mechanics
   • Keyboard: 1-4 for speed presets

Show Infection Radius: {params.show_infection_radius}
   • Toggle: Checkbox in visualization
   • Effect: Display red circles around infected particles
   • Purpose: Visualize transmission range

═══════════════════════════════════════════════════════════════════════════════
EPIDEMIOLOGICAL CONCEPTS (For Understanding)
═══════════════════════════════════════════════════════════════════════════════

R₀ (Basic Reproduction Number):
   • Definition: Average # of people ONE infected person infects
   • Factors: infection_prob × contacts_per_day × infection_duration
   • Interpretation: R₀ > 1 → epidemic grows
                    R₀ = 1 → endemic (stable)
                    R₀ < 1 → epidemic dies out
   • Real Diseases: Measles ~15-18, COVID-19 ~2-3, Flu ~1-2

SIR Model (Classic):
   • S = Susceptible (blue/cyan particles)
   • I = Infected (red/orange particles)
   • R = Removed/Recovered (gray particles)

SEIRD Model (Enhanced - This Simulation):
   • S = Susceptible
   • E = Exposed (infected but not yet infectious - incubation)
   • I = Infectious (can spread disease)
   • R = Recovered (immune)
   • D = Dead

Herd Immunity Threshold:
   • Formula: 1 - (1/R₀)
   • Example: R₀=3 → threshold = 1-(1/3) = 66.7% immune needed
   • Achieved by: Recovery OR Vaccination
   • Effect: Epidemic cannot sustain when threshold reached

═══════════════════════════════════════════════════════════════════════════════
KEYBOARD SHORTCUTS
═══════════════════════════════════════════════════════════════════════════════

SPACE    - Pause/Resume simulation
R        - Reset simulation (keeps current parameters)
F        - Toggle fullscreen mode
Q        - Toggle quarantine on/off
M        - Toggle marketplace on/off
Ctrl+R   - Show this documentation (Parameter Reference)
Alt+T    - Toggle light/dark theme
1-9      - Load preset scenarios (1=Baseline, 2=Aggressive, etc.)

═══════════════════════════════════════════════════════════════════════════════
RECOMMENDED SCENARIOS FOR EXPERIMENTATION
═══════════════════════════════════════════════════════════════════════════════

Baseline Epidemic (No Intervention):
   • Quarantine: OFF
   • Marketplace: OFF
   • Social Distance: 0%
   • Observe: Natural disease spread, peak infection day

Effect of Quarantine:
   • Start with baseline
   • Enable quarantine after day 20
   • Observe: "Flattening the curve" effect

Super-Spreader Events:
   • Marketplace: ON
   • Attendance: 60-80%
   • Interval: 24-48 hours
   • Observe: Periodic spikes in infections

Vaccination Campaign:
   • Enable vaccination
   • Efficacy: 70-90%
   • Rate: 1-2%/day
   • Observe: Approach to herd immunity threshold

═══════════════════════════════════════════════════════════════════════════════

Documentation Version: 3.0
Last Updated: 2024-12-09
IHK Project: Three Statistical Distributions in Epidemic Simulation

═══════════════════════════════════════════════════════════════════════════════
"""

        text_edit.setPlainText(doc_text)
        layout.addWidget(text_edit)

        # Close button
        close_btn = QPushButton("Close (ESC)")
        close_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {get_color('BORDER_GREEN') if theme_module.current_theme == DARK_THEME else get_color('PRIMARY')};
                color: #000000;
                border: none;
                padding: 10px;
                font-weight: bold;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: {get_color('NEON_GREEN') if theme_module.current_theme == DARK_THEME else get_color('SECONDARY')};
            }}
        """)
        close_btn.clicked.connect(dialog.close)
        layout.addWidget(close_btn)

        dialog.setLayout(layout)

        # Set dialog background
        dialog.setStyleSheet(f"""
            QDialog {{
                background-color: {get_color('BG_WHITE') if theme_module.current_theme == LIGHT_THEME else get_color('BG_BLACK')};
            }}
        """)

        dialog.exec_()

    def _configure_tooltips_simple(self):
        """Configure tooltips to work properly without flickering."""
        # Set tooltip delay to prevent instant appearance
        # DO NOT call this repeatedly - it's called once at startup
        # Tooltips are styled via the QMainWindow stylesheet in apply_theme()
        pass  # No longer needed - tooltip styling is in the main stylesheet

    def keyPressEvent(self, event):
        """
        Handle keyboard shortcuts for quick access to common functions.

        Shortcuts:
            SPACE: Pause/Resume
            R: Reset simulation
            Ctrl+R: Show parameter documentation
            F: Fullscreen toggle
            Q: Toggle quarantine
            M: Toggle marketplace
            Ctrl+T: Toggle tooltips
            Alt+T: Toggle theme
            1-9: Load preset by number

        Args:
            event (QKeyEvent): Keyboard event
        """
        key = event.key()
        modifiers = event.modifiers()

        # Ctrl+T: Toggle tooltips
        if key == Qt.Key_T and modifiers & Qt.ControlModifier:
            self.toggle_tooltips()
            return

        # Alt+T: Toggle theme
        if key == Qt.Key_T and modifiers & Qt.AltModifier:
            self.toggle_theme()
            return

        # Space: Pause/Resume
        if key == Qt.Key_Space:
            self.toggle_pause()
            return

        # Ctrl+R: Show parameter documentation
        if key == Qt.Key_R and modifiers & Qt.ControlModifier:
            self.show_parameter_documentation()
            return

        # R: Reset (without Ctrl)
        if key == Qt.Key_R and not (modifiers & Qt.ControlModifier):
            self.reset_sim()
            return

        # 1-9: Quick preset selection
        if Qt.Key_1 <= key <= Qt.Key_9:
            preset_index = key - Qt.Key_1  # 0-8
            preset_names = list(PRESETS.keys())
            if preset_index < len(preset_names):
                preset_name = preset_names[preset_index]
                self.preset_combo.setCurrentText(preset_name)
            return

        # Q: Toggle quarantine
        if key == Qt.Key_Q:
            new_state = not params.quarantine_enabled
            self.quarantine_checkbox.setChecked(new_state)
            return

        # M: Toggle marketplace
        if key == Qt.Key_M:
            new_state = not params.marketplace_enabled
            self.marketplace_checkbox.setChecked(new_state)
            return

        # B: Toggle BASIC/ADVANCED mode
        if key == Qt.Key_B:
            self.toggle_mode()
            return

        # F: Toggle fullscreen
        if key == Qt.Key_F:
            self.toggle_fullscreen()
            return

        # Pass other events to parent
        super().keyPressEvent(event)

    def update_simulation(self):
        """Update simulation state and canvas rendering (called by timer)."""
        if not self.paused:
            # Accumulate fractional speed for smooth slow speeds (0.5x)
            self.speed_accumulator += self.speed
            steps_to_run = int(self.speed_accumulator)

            for _ in range(steps_to_run):
                self.sim.step()

            # Keep the fractional part for next frame
            self.speed_accumulator -= steps_to_run

        # Adaptive frame skipping for performance with many particles
        self.frame_count += 1
        if self.frame_count >= self.skip_frames:
            self.frame_count = 0
            self.canvas.update()  # Only update canvas every Nth frame

    def update_stats_display(self, counts):
        """
        Update statistics display, graph, and pie chart.

        Args:
            counts (dict): Current population counts by state
        """
        # Use initial population for percentages
        initial = self.sim.initial_population
        if initial == 0:
            return

        s_pct = counts['susceptible']/initial*100
        i_pct = counts['infected']/initial*100
        r_pct = counts['removed']/initial*100
        d_pct = counts['dead']/initial*100

        # Get absolute counts
        s_count = counts['susceptible']
        i_count = counts['infected']
        r_count = counts['removed']
        d_count = counts['dead']

        # Always show all stats (S/I/R/D) for consistency
        text = f"DAY: {self.sim.day_count:03d}\n"
        text += f"S: {s_count:3d} ({s_pct:5.1f}%) | I: {i_count:3d} ({i_pct:5.1f}%)\n"
        text += f"R: {r_count:3d} ({r_pct:5.1f}%) | D: {d_count:3d} ({d_pct:5.1f}%)"
        self.stats_label.setText(text)

        # Update pie chart only every 5 days to reduce stuttering
        if self.sim.day_count % 5 == 0 or self.sim.day_count == 0:
            self.pie_chart.update_chart(counts)

        # Update graph with clear separate lines
        if len(self.sim.stats['day']) > 1:
            self.graph_widget.clear()

            days = self.sim.stats['day']
            s_data = self.sim.stats['susceptible']
            i_data = self.sim.stats['infected']
            r_data = self.sim.stats['removed']
            d_data = self.sim.stats['dead']

            # Plot as separate, clear lines (NO fill!)
            # Susceptible - Cyan line
            s_curve = pg.PlotDataItem(
                days, s_data,
                pen=pg.mkPen(color=(0, 191, 255), width=3),
                brush=None,  # NO FILL
                fillLevel=None,
                name='Susceptible'
            )
            self.graph_widget.addItem(s_curve)

            # Infected - Red line
            i_curve = pg.PlotDataItem(
                days, i_data,
                pen=pg.mkPen(color=(255, 69, 69), width=3),
                brush=None,  # NO FILL
                fillLevel=None,
                name='Infected'
            )
            self.graph_widget.addItem(i_curve)

            # Removed - Gray line
            r_curve = pg.PlotDataItem(
                days, r_data,
                pen=pg.mkPen(color=(120, 120, 120), width=3),
                brush=None,  # NO FILL
                fillLevel=None,
                name='Removed'
            )
            self.graph_widget.addItem(r_curve)

            # Dead - Dark red/black line
            if max(d_data) > 0:  # Only show if there are deaths
                d_curve = pg.PlotDataItem(
                    days, d_data,
                    pen=pg.mkPen(color=(80, 0, 0), width=3),
                    brush=None,  # NO FILL
                    fillLevel=None,
                    name='Dead'
                )
                self.graph_widget.addItem(d_curve)

            # Auto-range X to show full epidemic curve from start to current
            # This ensures the entire development is visible, not stuck on first 15 days
            self.graph_widget.setXRange(0, max(days), padding=0.02)
            # Always keep Y-axis fixed at 0-100 for percentage data
            self.graph_widget.setYRange(0, 100, padding=0)
            self.graph_widget.enableAutoRange(axis='x', enable=False)
            self.graph_widget.enableAutoRange(axis='y', enable=False)
