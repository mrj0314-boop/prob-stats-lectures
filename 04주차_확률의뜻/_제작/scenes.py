"""1주차 확률의 기초 애니메이션 (manim). 렌더링: python _공용/render.py <주차폴더> [장면...]."""
from common import *


def die_face(k, size=0.9):
    sq = RoundedRectangle(corner_radius=0.12, width=size, height=size,
                          fill_color=WHITE, fill_opacity=1, stroke_color=NAVY, stroke_width=4)
    pos = {1: [(0, 0)], 2: [(-1, 1), (1, -1)], 3: [(-1, 1), (0, 0), (1, -1)],
           4: [(-1, 1), (1, 1), (-1, -1), (1, -1)],
           5: [(-1, 1), (1, 1), (0, 0), (-1, -1), (1, -1)],
           6: [(-1, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (1, -1)]}[k]
    pips = VGroup(*[Dot(sq.get_center() + np.array([x, y, 0]) * size * 0.27,
                        radius=size * 0.08, color=NAVY) for x, y in pos])
    return VGroup(sq, pips)


class GachaSampleSpace(Scene):
    """비유: 표본공간 = 뽑기 상자, 사건 = 바구니에 골라 담은 공."""

    def construct(self):
        box = RoundedRectangle(corner_radius=0.3, width=4.6, height=3.6,
                               color=NAVY, stroke_width=5).shift(LEFT * 2.6 + UP * 0.6)
        box_label = Text("뽑기 상자 = 표본공간 S", font_size=28, weight=BOLD).next_to(box, UP, buff=0.25)
        colors = [BLUE, ORANGE, GREEN, "#C0504D", "#8064A2", "#D4A017"]
        balls = VGroup()
        for k in range(6):
            c = Circle(radius=0.5, fill_color=colors[k], fill_opacity=1, stroke_color=WHITE, stroke_width=3)
            balls.add(VGroup(c, Text(str(k + 1), font_size=36, color=WHITE, weight=BOLD).move_to(c)))
        balls.arrange_in_grid(2, 3, buff=0.35).move_to(box)

        self.play(Create(box), Write(box_label))
        self.play(LaggedStart(*[FadeIn(b, scale=0.4) for b in balls], lag_ratio=0.15))
        cap = caption("주사위를 던져 나올 수 있는 모든 결과 = 상자 속 공 6개")
        self.play(FadeIn(cap))
        self.wait(1.2)

        top = RIGHT * 3.0 + UP * 1.2
        basket = Polygon(top + LEFT * 1.5, top + RIGHT * 1.5, top + RIGHT * 1.1 + DOWN * 1.9,
                         top + LEFT * 1.1 + DOWN * 1.9, color=ORANGE, stroke_width=5,
                         fill_color=ORANGE, fill_opacity=0.08)
        handle = Arc(radius=1.5, start_angle=0, angle=PI, arc_center=top, color=ORANGE, stroke_width=5)
        basket_label = Text("바구니 = 사건 A", font_size=28, weight=BOLD, color=ORANGE).next_to(handle, UP, buff=0.15)
        self.play(Create(basket), Create(handle), Write(basket_label))
        cap = swap_caption(self, cap, "‘짝수가 나온다’는 조건에 맞는 공만 골라 담기")

        center = basket.get_center() + UP * 0.1
        picks = [balls[i].copy() for i in (1, 3, 5)]
        self.play(LaggedStart(*[p.animate.scale(0.75).move_to(center + RIGHT * dx)
                                for p, dx in zip(picks, (-0.8, 0, 0.8))], lag_ratio=0.3), run_time=2)
        cap = swap_caption(self, cap, "바구니 속 공 = 사건 A  →  표본공간의 <b>부분집합</b>")

        sets = Text("S = {1, 2, 3, 4, 5, 6}        A = {2, 4, 6}", font_size=32).move_to(DOWN * 2.3)
        sets[-9:].set_color(ORANGE)
        self.play(Write(sets))
        self.wait(3)


class ClubVenn(Scene):
    """비유: 반 학생(점)과 두 동아리(원)로 보는 사건의 연산."""

    def construct(self):
        S = Rectangle(width=9.6, height=5.8, color=NAVY, stroke_width=4).shift(UP * 0.55)
        S_label = Text("우리 반 학생 전체 S", font_size=24).next_to(S.get_corner(UL), DR, buff=0.18)
        ca, cb, r = np.array([-1.25, 0.25, 0]), np.array([1.25, 0.25, 0]), 1.95
        A = Circle(radius=r, color=BLUE, stroke_width=6).move_to(ca)
        B = Circle(radius=r, color=GREEN, stroke_width=6).move_to(cb)
        A_lab = Text("축구부 A", font_size=28, color=BLUE, weight=BOLD).next_to(A, UP, buff=0.08).shift(LEFT * 1.1)
        B_lab = Text("밴드부 B", font_size=28, color=GREEN, weight=BOLD).next_to(B, UP, buff=0.08).shift(RIGHT * 1.1)

        rng = np.random.default_rng(5)
        pts = []
        while len(pts) < 46:
            p = np.array([rng.uniform(-4.5, 4.5), rng.uniform(-2.0, 3.0), 0])
            if abs(p[0]) < 4.2 and -2.0 < p[1] < 2.6 and all(np.linalg.norm(p - q) > 0.42 for q in pts):
                pts.append(p)
        pts = np.array(pts)
        inA = np.linalg.norm(pts - ca, axis=1) < r
        inB = np.linalg.norm(pts - cb, axis=1) < r
        dots = VGroup(*[Dot(p, radius=0.09, color=NAVY) for p in pts]).set_z_index(3)

        self.play(Create(S), Write(S_label))
        self.play(LaggedStart(*[FadeIn(d, scale=0.3) for d in dots], lag_ratio=0.03))
        cap = caption("점 하나 = 학생 한 명")
        self.play(FadeIn(cap))
        self.play(Create(A), Create(B), Write(A_lab), Write(B_lab))
        self.wait(0.8)

        phases = [
            ("<b>A ∪ B</b>  합사건: 둘 중 하나라도 가입", Union(A, B), inA | inB),
            ("<b>A ∩ B</b>  곱사건: 두 동아리 모두 가입", Intersection(A, B), inA & inB),
            ("<b>A<sup>c</sup></b>  여사건: 축구부가 아닌 학생", Difference(S, A), ~inA),
            ("<b>A − B</b>  차사건: 축구부만 가입", Difference(A, B), inA & ~inB),
        ]
        region, count = None, None
        for text, shape, mask in phases:
            shape.set_fill(ORANGE, 0.35).set_stroke(width=0).set_z_index(-1)
            new_count = Text(f"해당 학생 {mask.sum()}명", font_size=26, color=ORANGE, weight=BOLD) \
                .next_to(S.get_corner(UR), DL, buff=0.18)
            anims = [FadeIn(shape), FadeIn(new_count)]
            if region is not None:
                anims += [FadeOut(region), FadeOut(count)]
            anims += [d.animate.set_color(NAVY if m else GRAY).scale(1.0) for d, m in zip(dots, mask)]
            self.play(*anims, FadeOut(cap), run_time=0.9)
            cap = caption(text)
            self.play(FadeIn(cap, shift=UP * 0.2), run_time=0.5)
            region, count = shape, new_count
            self.wait(2.2)
        self.wait(1)


class PizzaClassical(Scene):
    """비유: 공평한 주사위 = 똑같이 자른 피자. 고전적 확률 = 조각 수 비율."""

    def construct(self):
        center, R = LEFT * 2.5 + UP * 0.5, 2.4
        cheese, crust = ManimColor("#F6CF6B"), ManimColor("#C8812A")

        def make_pizza(angles):
            sectors, start = VGroup(), PI / 2
            for a in angles:
                sectors.add(AnnularSector(inner_radius=0, outer_radius=R, angle=-a, start_angle=start,
                                          fill_color=cheese, fill_opacity=1, stroke_color=crust,
                                          stroke_width=6).shift(center))
                start -= a
            return sectors

        slices = make_pizza([TAU / 6] * 6)
        mids = [PI / 2 - (k + 0.5) * TAU / 6 for k in range(6)]
        dirs = [np.array([np.cos(m), np.sin(m), 0]) for m in mids]
        labels = VGroup(*[Text(str(k + 1), font_size=40, weight=BOLD).move_to(center + d * R * 0.62)
                          for k, d in enumerate(dirs)])
        rng = np.random.default_rng(1)
        pepperoni = VGroup()
        for d in dirs:
            for _ in range(2):
                rot = rng.uniform(-0.3, 0.3)
                v = np.array([d[0] * np.cos(rot) - d[1] * np.sin(rot), d[0] * np.sin(rot) + d[1] * np.cos(rot), 0])
                pepperoni.add(Circle(radius=0.17, fill_color="#C0504D", fill_opacity=0.9, stroke_width=0)
                              .move_to(center + v * R * rng.uniform(0.3, 0.78)))
        slice_groups = [VGroup(s) for s in slices]

        self.play(LaggedStart(*[GrowFromPoint(s, center) for s in slices], lag_ratio=0.12))
        self.play(FadeIn(pepperoni, lag_ratio=0.05), Write(labels))
        cap = caption("공평한 주사위 = <b>똑같은 크기</b>로 자른 피자 6조각")
        self.play(FadeIn(cap))
        self.wait(1.2)

        cap = swap_caption(self, cap, "사건 A: ‘5 이상’ → 5번, 6번 조각 고르기")
        movers = []
        for k in (4, 5):
            g = VGroup(slices[k], labels[k], *[p for p in pepperoni if np.dot(p.get_center() - center, dirs[k]) > 0.85 * np.linalg.norm(p.get_center() - center)])
            movers.append(g.animate.shift(dirs[k] * 0.35))
        self.play(*movers, slices[4].animate.set_stroke(ORANGE, 9), slices[5].animate.set_stroke(ORANGE, 9))

        row1 = VGroup(Text("P(A) =", font_size=34), frac("고른 조각 수", "전체 조각 수", 26)).arrange(RIGHT, buff=0.25)
        row2 = VGroup(Text("=", font_size=36), frac("2", "6", 40), Text("=", font_size=36),
                      frac("1", "3", 40, ORANGE)).arrange(RIGHT, buff=0.3)
        panel = VGroup(row1, row2).arrange(DOWN, buff=0.6, aligned_edge=LEFT).move_to(RIGHT * 2.95 + UP * 0.5)
        self.play(Write(row1))
        self.play(Write(row2))
        cap = swap_caption(self, cap, "고전적 확률 = 조건에 맞는 결과 수 ÷ 전체 결과 수")
        self.wait(2.5)

        cap = swap_caption(self, cap, "그런데 조각 크기가 다르다면?")
        uneven = make_pizza([a * DEGREES for a in (110, 35, 85, 25, 65, 40)])
        self.play(FadeOut(labels), FadeOut(pepperoni), FadeOut(panel))
        self.play(*[Transform(s, u.set_stroke(crust, 6)) for s, u in zip(slices, uneven)], run_time=1.5)
        warn = VGroup(Text("찌그러진 주사위", font_size=32, color="#C0504D", weight=BOLD),
                      Text("조각 수만 세면 틀린 답", font_size=28),
                      Text("→ 상대도수로 확률 추정", font_size=28, color=ORANGE)) \
            .arrange(DOWN, buff=0.3).move_to(RIGHT * 2.95 + UP * 0.5)
        self.play(FadeIn(warn, lag_ratio=0.3), run_time=1.2)
        cap = swap_caption(self, cap, "고전적 확률의 전제: 모든 결과가 <b>같은 가능성</b>")
        self.wait(3)


class CoinLLN(Scene):
    """동전 던지기 상대도수가 0.5 근처로 안정되는 과정."""

    def construct(self):
        N = 1000
        rng = np.random.default_rng(7)
        flips = rng.integers(0, 2, N)
        freq = np.cumsum(flips) / np.arange(1, N + 1)

        ax = Axes(x_range=[0, N, 250], y_range=[0, 1, 0.25], x_length=7.8, y_length=3.9,
                  axis_config={"color": NAVY, "stroke_width": 3}, tips=False).shift(DOWN * 0.45 + RIGHT * 0.55)
        xt = VGroup(*[Text(str(v), font_size=20).next_to(ax.c2p(v, 0), DOWN, buff=0.15) for v in range(0, N + 1, 250)])
        yt = VGroup(*[Text(f"{v:g}", font_size=20).next_to(ax.c2p(0, v), LEFT, buff=0.15) for v in (0, 0.25, 0.5, 0.75, 1)])
        xl = Text("던진 횟수 n", font_size=22).next_to(ax.c2p(N, 0), UP + LEFT, buff=0.15)
        yl = Text("앞면 비율", font_size=22).next_to(ax.y_axis, UP, buff=0.3)
        half = DashedLine(ax.c2p(0, 0.5), ax.c2p(N, 0.5), color=ORANGE, stroke_width=4)
        half_lab = Text("0.5", font_size=24, color=ORANGE, weight=BOLD).next_to(half, RIGHT, buff=0.1)

        coin_c = Circle(radius=0.6, fill_color="#D4A017", fill_opacity=1, stroke_color="#9C7410", stroke_width=5)
        coin_t = Text("앞", font_size=34, color=WHITE, weight=BOLD)
        coin = VGroup(coin_c, coin_t).move_to(LEFT * 4.1 + UP * 3.0)

        n = ValueTracker(0)

        def path():
            k = int(n.get_value())
            p = VMobject(color=NAVY, stroke_width=4)
            if k >= 2:
                p.set_points_as_corners([ax.c2p(i, freq[i - 1]) for i in range(1, k + 1)])
            return p

        def status():
            k = max(int(n.get_value()), 1)
            heads = int(flips[:k].sum())
            return Text(f"n = {k:,}    앞면 {heads}번    비율 {freq[k - 1]:.3f}", font_size=28) \
                .move_to(RIGHT * 1.0 + UP * 3.0)

        graph = always_redraw(path)
        info = always_redraw(status)
        self.play(Create(ax), FadeIn(xt, yt, xl, yl), Create(half), FadeIn(half_lab))
        self.play(FadeIn(coin, scale=0.5))
        self.add(graph)
        cap = caption("처음 몇 번은 비율이 크게 출렁임")
        self.play(FadeIn(cap), FadeIn(info))

        for i in range(12):
            self.play(coin_c.animate.stretch_to_fit_width(0.05), FadeOut(coin_t), run_time=0.12)
            heads = flips[i] == 1
            coin_c.set_fill("#D4A017" if heads else "#A9A9A9")
            coin_t = Text("앞" if heads else "뒤", font_size=34, color=WHITE, weight=BOLD).move_to(coin_c)
            self.play(coin_c.animate.stretch_to_fit_width(1.2), FadeIn(coin_t), n.animate.set_value(i + 1),
                      run_time=0.15)
        coin = VGroup(coin_c, coin_t)

        cap = swap_caption(self, cap, "1,000번까지 빠르게 반복")
        self.play(n.animate.set_value(N), Rotate(coin, angle=TAU * 6, axis=UP), run_time=6, rate_func=rush_into)
        cap = swap_caption(self, cap, "던질수록 비율이 <b>0.5 근처로 안정</b> = 상대도수 확률")
        self.wait(3.5)


class RainArea(Scene):
    """비유: 타일 위 빗방울. 떨어진 비율이 넓이 비율 1/4에 가까워짐 (큰 수의 법칙)."""

    def construct(self):
        side = 5.0
        c = LEFT * 2.3 + UP * 0.45
        tile = Square(side, color=NAVY, stroke_width=5).move_to(c)
        quarter = Square(side / 2, stroke_width=0, fill_color=ORANGE, fill_opacity=0.25) \
            .move_to(c + (LEFT + DOWN) * side / 4)
        grid = VGroup(Line(c + UP * side / 2, c + DOWN * side / 2), Line(c + LEFT * side / 2, c + RIGHT * side / 2)) \
            .set_stroke(GRAY, 2)
        tag = Text("색칠한 칸 = 전체 넓이의 1/4", font_size=24, color=ORANGE, weight=BOLD).next_to(tile, UP, buff=0.2)

        self.play(Create(tile), Create(grid), FadeIn(quarter), Write(tag))
        cap = caption("마당 타일 위에 비가 아무 곳에나 떨어지는 상황")
        self.play(FadeIn(cap))

        rng = np.random.default_rng(11)
        total, hits = 0, 0

        def panel(total, hits):
            ratio = hits / total if total else 0
            rows = VGroup(Text(f"빗방울 수   {total:,}", font_size=28),
                          Text(f"색칠한 칸   {hits:,}", font_size=28, color=ORANGE),
                          Text(f"비율   {ratio:.3f}", font_size=34, weight=BOLD)) \
                .arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(RIGHT * 3.25 + UP * 1.5)
            return rows

        nl = NumberLine(x_range=[0, 1, 0.25], length=3.6, color=NAVY, include_numbers=False) \
            .move_to(RIGHT * 3.25 + DOWN * 0.8)
        nl_t = VGroup(*[Text(f"{v:g}", font_size=18).next_to(nl.n2p(v), DOWN, buff=0.12) for v in (0, 0.25, 0.5, 1)])
        goal = Line(nl.n2p(0.25) + UP * 0.35, nl.n2p(0.25) + DOWN * 0.05, color=ORANGE, stroke_width=5)
        marker = Triangle(fill_color=NAVY, fill_opacity=1, stroke_width=0).scale(0.14).rotate(PI) \
            .next_to(nl.n2p(0), UP, buff=0.05)
        info = panel(0, 0)
        self.play(FadeIn(info), Create(nl), FadeIn(nl_t), Create(goal), FadeIn(marker))

        drops_all = VGroup()
        for b, size in enumerate([4, 8, 16, 32, 64, 128, 256, 512]):
            xy = rng.uniform(-side / 2, side / 2, (size, 2))
            inside = (xy[:, 0] < 0) & (xy[:, 1] < 0)
            drops = VGroup(*[Dot(c + np.array([x, y, 0]), radius=0.07 if size < 64 else 0.045,
                                 color=ORANGE if i else BLUE) for (x, y), i in zip(xy, inside)])
            total += size
            hits += int(inside.sum())
            new_info = panel(total, hits)
            if b < 2:
                self.play(LaggedStart(*[FadeIn(d, shift=DOWN * 1.5) for d in drops], lag_ratio=0.2), run_time=1.2)
            else:
                self.play(FadeIn(drops, lag_ratio=0.02), run_time=0.9)
            drops_all.add(drops)
            self.play(Transform(info, new_info),
                      marker.animate.next_to(nl.n2p(hits / total), UP, buff=0.05), run_time=0.5)
            if b == 1:
                cap = swap_caption(self, cap, "빗방울이 적을 때: 비율이 1/4에서 크게 벗어남")
            if b == 5:
                cap = swap_caption(self, cap, "빗방울이 많아질수록 …")
        cap = swap_caption(self, cap, "비율 → 넓이 비율 1/4  (<b>큰 수의 법칙</b>)")
        self.wait(3.5)


class DiceSumBars(Scene):
    """두 주사위 합: 많이 던질수록 막대(실험)가 주황 점(이론)에 맞춰짐."""

    def construct(self):
        TOTAL = 6000
        rng = np.random.default_rng(3)
        rolls = rng.integers(1, 7, (TOTAL, 2))
        sums = rolls.sum(axis=1)
        theory = np.array([min(s - 1, 13 - s) / 36 for s in range(2, 13)])
        steps = np.unique(np.geomspace(5, TOTAL, 24).astype(int))

        ax = Axes(x_range=[1, 13, 1], y_range=[0, 0.25, 0.05], x_length=8.6, y_length=4.0,
                  axis_config={"color": NAVY, "stroke_width": 3}, tips=False).shift(DOWN * 0.4)
        xt = VGroup(*[Text(str(v), font_size=22).next_to(ax.c2p(v, 0), DOWN, buff=0.15) for v in range(2, 13)])
        yt = VGroup(*[Text(f"{v:.2f}", font_size=18).next_to(ax.c2p(1, v), LEFT, buff=0.12) for v in (0.05, 0.1, 0.15, 0.2)])
        xl = Text("눈의 합", font_size=20, color=GRAY).next_to(xt, RIGHT, buff=0.2)
        dots = VGroup(*[Dot(ax.c2p(s, p), radius=0.12, color=ORANGE).set_z_index(3)
                        for s, p in zip(range(2, 13), theory)])
        bw = ax.c2p(1.7, 0)[0] - ax.c2p(1, 0)[0]

        def bars_for(heights):
            return VGroup(*[Rectangle(width=bw, height=max(ax.c2p(0, h)[1] - ax.c2p(0, 0)[1], 0.001),
                                      fill_color=BLUE, fill_opacity=0.85, stroke_width=0)
                            .move_to(ax.c2p(s, 0), aligned_edge=DOWN) for s, h in zip(range(2, 13), heights)])

        d1, d2 = die_face(1).move_to(LEFT * 1.1 + UP * 3.15), die_face(1).move_to(RIGHT * 0.1 + UP * 3.15)
        plus = Text("+", font_size=36).move_to((d1.get_center() + d2.get_center()) / 2)
        roll_txt = Text("", font_size=28)
        legend = VGroup(VGroup(Square(0.28, fill_color=BLUE, fill_opacity=0.85, stroke_width=0), Text("실험 결과", font_size=22)).arrange(RIGHT, buff=0.12),
                        VGroup(Dot(radius=0.12, color=ORANGE), Text("이론 확률", font_size=22)).arrange(RIGHT, buff=0.12)) \
            .arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(UR, buff=0.35).shift(DOWN * 1.3)

        bars = bars_for(np.zeros(11))
        self.play(Create(ax), FadeIn(xt, yt, xl))
        self.play(FadeIn(d1, d2, plus), FadeIn(dots, lag_ratio=0.1), FadeIn(legend))
        self.add(bars)
        cap = caption("주사위 두 개를 던져 합을 기록")
        self.play(FadeIn(cap))

        def update_dice(i):
            a, b = rolls[i]
            d1.become(die_face(int(a)).move_to(d1))
            d2.become(die_face(int(b)).move_to(d2))
            return Text(f"합 {a + b}    누적 {i + 1:,}번", font_size=28).next_to(d2, RIGHT, buff=0.5)

        for i in range(5):
            new_txt = update_dice(i)
            h = np.bincount(sums[:i + 1], minlength=13)[2:] / (i + 1)
            self.play(Transform(bars, bars_for(h)), Transform(roll_txt, new_txt), run_time=0.45)
            self.wait(0.2)

        cap = swap_caption(self, cap, "횟수를 늘려 가며 비율 비교")
        for n in steps:
            new_txt = update_dice(n - 1)
            h = np.bincount(sums[:n], minlength=13)[2:] / n
            self.play(Transform(bars, bars_for(h)), Transform(roll_txt, new_txt), run_time=0.3)
        cap = swap_caption(self, cap, "6,000번: 막대가 주황 점에 거의 일치, 합 7이 가장 흔함")
        self.wait(3.5)
