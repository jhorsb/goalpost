"""Accessibility checks for the generated explainer scatter panels."""

import importlib.util
from pathlib import Path


def _module():
    path = Path("phase7/render_scatter.py")
    spec = importlib.util.spec_from_file_location("goalpost_render_scatter", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_panel_accessible_description_contains_each_plotted_value():
    scatter = _module()
    points = [
        {"label": "Alpha", "value": 0.61, "architecture": "structured", "x": 1},
        {"label": "Bravo", "value": 0.49, "architecture": "freeform", "x": 2},
    ]

    svg = scatter.panel(
        "By test axis", "test axis", points,
        lambda point: point["x"], [1, 2], lambda value: str(value),
    )

    assert 'aria-labelledby="gp-scatter-by-test-axis-title gp-scatter-by-test-axis-desc"' in svg
    assert '<title id="gp-scatter-by-test-axis-title">By test axis</title>' in svg
    assert '<desc id="gp-scatter-by-test-axis-desc">' in svg
    assert "Alpha: recourse stability 0.61 at test axis 1" in svg
    assert "Bravo: recourse stability 0.49 at test axis 2" in svg
