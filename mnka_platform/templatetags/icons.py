from django import template
from django.utils.safestring import mark_safe

register = template.Library()

# Stroke-based line icons (24x24, currentColor) so they inherit the
# tile/text color wherever they're dropped. Kept deliberately simple
# and consistent with the logo's own flat line-art house + sparkles.
_ICONS = {
    "home": """<path d="M4 11.5 12 4l8 7.5" /><path d="M6 10v9a1 1 0 0 0 1 1h10a1 1 0 0 0 1-1v-9" /><path d="M10 20v-5h4v5" />""",
    "building": """<rect x="5" y="3" width="14" height="18" rx="1" /><path d="M9 8h1M14 8h1M9 12h1M14 12h1M9 16h1M14 16h1" /><path d="M10 21v-3h4v3" />""",
    "sparkles": """<path d="M12 3v4M12 17v4M3 12h4M17 12h4" /><path d="M12 8a4 4 0 0 0 4 4 4 4 0 0 0-4 4 4 4 0 0 0-4-4 4 4 0 0 0 4-4Z" />""",
    "window": """<rect x="4" y="4" width="16" height="16" rx="1" /><path d="M12 4v16M4 12h16" />""",
    "gear": """<circle cx="12" cy="12" r="3" /><path d="M19.4 15a1.7 1.7 0 0 0 .34 1.87l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.7 1.7 0 0 0-1.87-.34 1.7 1.7 0 0 0-1 1.55V21a2 2 0 1 1-4 0v-.09A1.7 1.7 0 0 0 9 19.4a1.7 1.7 0 0 0-1.87.34l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06A1.7 1.7 0 0 0 4.6 15a1.7 1.7 0 0 0-1.55-1H3a2 2 0 1 1 0-4h.09A1.7 1.7 0 0 0 4.6 9a1.7 1.7 0 0 0-.34-1.87l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06A1.7 1.7 0 0 0 9 4.6a1.7 1.7 0 0 0 1-1.55V3a2 2 0 1 1 4 0v.09a1.7 1.7 0 0 0 1 1.55 1.7 1.7 0 0 0 1.87-.34l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06A1.7 1.7 0 0 0 19.4 9a1.7 1.7 0 0 0 1.55 1H21a2 2 0 1 1 0 4h-.09a1.7 1.7 0 0 0-1.51 1Z" />""",
    "broom": """<path d="M20 4 10 14" /><path d="m9 15-3 3" /><path d="M4 20c1-3 2.5-4.5 5-5 1.5-.4 2.5-1.4 3-3l1 1c-.6 1.5-1.6 2.5-3 3-2.5.6-4 2-5 5Z" /><path d="M16 3l5 5" />""",
    "shield": """<path d="M12 3 4 6v6c0 4.5 3 8 8 9 5-1 8-4.5 8-9V6l-8-3Z" /><path d="m9 12 2 2 4-4" />""",
    "leaf": """<path d="M5 21c9 0 14-5 14-14V4h-3C7 4 5 9 5 18v3Z" /><path d="M5 21c3-4 6-7 12-10" />""",
    "clock": """<circle cx="12" cy="12" r="9" /><path d="M12 7v5l3 2" />""",
    "thumb": """<path d="M7 10v11" /><path d="M11 21h6.5a2 2 0 0 0 2-1.7l1.1-7A2 2 0 0 0 18.6 10H14l.8-4.3A1.7 1.7 0 0 0 13.1 4 1.7 1.7 0 0 0 11.6 5L7 10v11h4Z" />""",
    "check": """<circle cx="12" cy="12" r="10" /><path d="m8 12 3 3 5-6" />""",
    "spark-dot": """<path d="M12 2v3M12 19v3M2 12h3M19 12h3" /><path d="M12 6a6 6 0 0 0 6 6 6 6 0 0 0-6 6 6 6 0 0 0-6-6 6 6 0 0 0 6-6Z" />""",
}


@register.simple_tag
def icon(name, size=24, stroke_width=1.8, css_class=""):
    body = _ICONS.get(name, _ICONS["sparkles"])
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
        f'viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        f'stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round" '
        f'class="{css_class}">{body}</svg>'
    )
    return mark_safe(svg)
