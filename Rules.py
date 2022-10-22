"""
Rule Functions
"""

# Imports
from RuleLibrary import Rules_ConwaysGameofLife

# Main Functions

# Main Vars
RULE_FUNCS = {
    "2D": {
        **Rules_ConwaysGameofLife.RULE_FUNCS["2D"]
    },
    "3D": {
        **Rules_ConwaysGameofLife.RULE_FUNCS["3D"]
    }
}