# AI Event Monitoring Models Package
# This package contains detection models for:
# - Fire/Smoke detection
# - Crowd surge detection  
# - Unconscious person detection

from .fire_smoke import check_fire_smoke
from .crowd_surge import check_crowd_surge
from .unconscious import check_unconscious

__all__ = ['check_fire_smoke', 'check_crowd_surge', 'check_unconscious'] 