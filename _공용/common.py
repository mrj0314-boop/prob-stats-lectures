"""manim 장면 공통 설정: 화면 크기, 색상, 자막·분수·사람·탁자 도우미.

LaTeX 없이 동작하도록 수식도 Text로 구성함.
"""
import numpy as np
from manim import *

# 슬라이드 오른쪽 절반에 들어가는 4:3 화면
config.pixel_width = 800
config.pixel_height = 600
config.frame_rate = 15
config.frame_height = 8
config.frame_width = 8 * 4 / 3
config.background_color = WHITE

NAVY = ManimColor("#23373B")
ORANGE = ManimColor("#EB811B")
BLUE = ManimColor("#3B7EA1")
GREEN = ManimColor("#5B9E6F")
RED = ManimColor("#C0504D")
PURPLE = ManimColor("#8064A2")
GOLD = ManimColor("#D4A017")
GRAY = ManimColor("#8A9499")
LIGHT = ManimColor("#E9EDEE")
WOOD = ManimColor("#E3C59E")
WOOD_EDGE = ManimColor("#A0784F")
FONT = "Malgun Gothic"
PEOPLE_COLORS = [BLUE, ORANGE, GREEN, RED, PURPLE, GOLD]

Text.set_default(font=FONT, color=NAVY)
MarkupText.set_default(font=FONT, color=NAVY)


def caption(s, size=28):
    t = MarkupText(s, font_size=size)
    if t.width > config.frame_width - 0.6:
        t.scale_to_fit_width(config.frame_width - 0.6)
    return t.to_edge(DOWN, buff=0.35)


def swap_caption(scene, old, new_text):
    new = caption(new_text)
    scene.play(FadeOut(old, shift=UP * 0.2), FadeIn(new, shift=UP * 0.2), run_time=0.6)
    return new


def frac(num, den, size=32, color=NAVY):
    n = Text(num, font_size=size, color=color)
    d = Text(den, font_size=size, color=color)
    w = max(n.width, d.width) + 0.2
    bar = Line(LEFT * w / 2, RIGHT * w / 2, color=color, stroke_width=3)
    return VGroup(n, bar, d).arrange(DOWN, buff=0.12)


def person(letter, color=None, r=0.38):
    color = color or PEOPLE_COLORS["ABCDEFGH".index(letter) % 6]
    c = Circle(radius=r, fill_color=color, fill_opacity=1, stroke_color=WHITE, stroke_width=3)
    return VGroup(c, Text(letter, font_size=int(r * 80), color=WHITE, weight=BOLD).move_to(c))


def seat_points(center, radius, n):
    """맨 위에서 시작해 시계 방향으로 n개 자리 좌표."""
    return [center + radius * np.array([np.cos(PI / 2 - k * TAU / n), np.sin(PI / 2 - k * TAU / n), 0])
            for k in range(n)]


def table(center, r):
    return Circle(radius=r, fill_color=WOOD, fill_opacity=1, stroke_color=WOOD_EDGE, stroke_width=5).move_to(center)


def round_table(order, center=ORIGIN, r=1.0, pr=0.3):
    """order 문자열을 맨 위부터 시계 방향으로 앉힌 원탁."""
    t = table(center, r)
    ps = VGroup(*[person(ch, r=pr).move_to(p) for ch, p in zip(order, seat_points(center, r + pr * 0.2, len(order)))])
    return VGroup(t, ps)


def cw_arrow(center, r, color=GRAY):
    """시계 방향 표시 화살표."""
    return CurvedArrow(center + r * np.array([np.cos(2.2), np.sin(2.2), 0]),
                       center + r * np.array([np.cos(0.9), np.sin(0.9), 0]),
                       angle=-1.3, color=color, stroke_width=4, tip_length=0.2)
