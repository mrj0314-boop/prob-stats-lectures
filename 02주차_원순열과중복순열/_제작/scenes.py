"""원순열 애니메이션 (manim). 렌더링: python _공용/render.py <주차폴더> [장면...]."""
from itertools import permutations

from common import *


def turn_arrow(center, r, cw=True, color=GRAY):
    a, b = (2.2, 0.9) if cw else (0.9, 2.2)
    return CurvedArrow(center + r * np.array([np.cos(a), np.sin(a), 0]),
                       center + r * np.array([np.cos(b), np.sin(b), 0]),
                       angle=-1.3 if cw else 1.3, color=color, stroke_width=4, tip_length=0.2)


class RoundTableRotate(Scene):
    """비유: 원탁 회의. 모두 한 칸씩 돌아 앉아도 같은 배치."""

    def construct(self):
        c, R = LEFT * 2.4 + UP * 0.4, 1.7
        rr = R + 0.15
        ang = ValueTracker(0)

        def pos(k):
            a = PI / 2 - k * TAU / 4 - ang.get_value()
            return c + rr * np.array([np.cos(a), np.sin(a), 0])

        people = VGroup(*[person(ch, r=0.48) for ch in "ABCD"])
        for k, p in enumerate(people):
            p.move_to(pos(k))
        people.add_updater(lambda m: [m[k].move_to(pos(k)) for k in range(4)])
        start = Text("기준 자리", font_size=22, color=GRAY).next_to(c + UP * (rr + 0.5), UP, buff=0.05)

        self.play(FadeIn(table(c, R)), Create(turn_arrow(c, R * 0.55, color=WOOD_EDGE)), FadeIn(start))
        self.play(LaggedStart(*[FadeIn(p, scale=0.5) for p in people], lag_ratio=0.2))
        cap = caption("원탁에 4명이 앉는 상황")
        head = Text("기준 자리부터 시계 방향으로 읽기", font_size=22, color=GRAY).move_to(RIGHT * 2.9 + UP * 2.9)

        def row(s, i):
            return Text(" → ".join(s), font_size=34, weight=BOLD).move_to(RIGHT * 2.9 + UP * (1.9 - i * 0.95))

        rows = VGroup(row("ABCD", 0))
        self.play(FadeIn(cap), Write(head), Write(rows[0]))
        self.wait(0.8)
        cap = swap_caption(self, cap, "모두 함께 한 칸씩 옆자리로 이동")
        for i, s in enumerate(["DABC", "CDAB", "BCDA"], 1):
            self.play(ang.animate.increment_value(TAU / 4), run_time=1.1)
            r = row(s, i)
            self.play(Write(r), run_time=0.6)
            rows.add(r)
        self.play(ang.animate.increment_value(TAU / 4), run_time=1.1)
        cap = swap_caption(self, cap, "4번 돌면 제자리 → 서로의 <b>상대적 위치</b>는 그대로")

        box = SurroundingRectangle(rows, color=ORANGE, buff=0.2, corner_radius=0.15, stroke_width=4)
        same = Text("모두 같은 원형 배치", font_size=28, color=ORANGE, weight=BOLD).next_to(box, DOWN, buff=0.2)
        self.play(Create(box), Write(same))
        cap = swap_caption(self, cap, "일렬로는 4가지, 원형으로는 <b>1가지</b>")
        self.wait(3)


class LineToCircle(Scene):
    """회전 관계인 일렬 배열 4개가 원탁 위에서 하나로 겹치는 장면."""

    def construct(self):
        orders = ["ABCD", "BCDA", "CDAB", "DABC"]
        rows = VGroup()
        for i, s in enumerate(orders):
            rows.add(VGroup(*[person(ch, r=0.3) for ch in s]).arrange(RIGHT, buff=0.18)
                     .move_to(LEFT * 3.4 + UP * (2.4 - i * 1.2)))
        cc, R = RIGHT * 2.5 + UP * 0.6, 1.4
        seats = dict(zip("ABCD", seat_points(cc, R + 0.08, 4)))

        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.3) for r in rows], lag_ratio=0.25))
        cap = caption("일렬 배열 4가지: 맨 앞 사람을 맨 뒤로 보내며 만든 배열")
        self.play(FadeIn(cap))
        self.play(FadeIn(table(cc, R)), Create(turn_arrow(cc, R * 0.55, color=WOOD_EDGE)))
        cap = swap_caption(self, cap, "줄의 양 끝을 이어 원탁에 앉히기")

        count = Text("", font_size=26)
        for i, r in enumerate(rows):
            copy = r.copy()
            self.play(*[m.animate.move_to(seats[ch]) for m, ch in zip(copy, orders[i])],
                      r.animate.set_opacity(0.35), run_time=1.0)
            new = Text(f"겹친 배열 {i + 1}개", font_size=26, color=ORANGE, weight=BOLD).next_to(cc + DOWN * R, DOWN, buff=0.6)
            self.play(Transform(count, new), Flash(cc, color=ORANGE, flash_radius=R + 0.5, line_length=0.3), run_time=0.6)
        cap = swap_caption(self, cap, "4가지 일렬 배열 → 원형으로는 모두 같은 1가지")
        calc = Text("4! ÷ 4 = 24 ÷ 4 = 6", font_size=34, color=ORANGE, weight=BOLD).move_to(DOWN * 2.45)
        self.play(FadeOut(count), Write(calc))
        cap = swap_caption(self, cap, "회전해서 같은 것 4개씩 묶기 → 일렬 배열 수를 4로 나누기")
        self.wait(3)


class FixOnePerson(Scene):
    """A를 맨 위에 고정하면 나머지 3명의 일렬 배치와 같아짐: 3! = 6."""

    def construct(self):
        title = Text("A를 맨 위에 고정, 나머지 B·C·D만 배치", font_size=28, weight=BOLD).to_edge(UP, buff=0.3)
        self.play(Write(title))
        orders = ["A" + "".join(p) for p in permutations("BCD")]
        spots = [np.array([x, y, 0]) for y in (1.25, -1.45) for x in (-3.3, 0, 3.3)]
        tables = VGroup()
        for o, s in zip(orders, spots):
            t = round_table(o, s, r=0.85, pr=0.3)
            t[1][0][0].set_stroke(ORANGE, 6)
            tables.add(t)
        cap = caption("A의 자리를 기준으로 정하면 회전으로 겹치는 경우 없음")
        self.play(FadeIn(cap))
        for t in tables:
            self.play(FadeIn(t[0]), LaggedStart(*[FadeIn(p, scale=0.5) for p in t[1]], lag_ratio=0.15), run_time=0.8)
        cap = swap_caption(self, cap, "나머지 3명을 일렬로 세우는 것과 같음 → 3! = 6가지")
        self.wait(1.5)
        formula = Text("원순열의 수 = (n − 1)!", font_size=34, color=ORANGE, weight=BOLD).to_edge(UP, buff=0.3)
        self.play(ReplacementTransform(title, formula))
        cap = swap_caption(self, cap, "n명 중 1명 고정 → 나머지 (n − 1)명 일렬 배치")
        self.wait(3)


class PolygonTable(Scene):
    """정팔각형 탁자는 원탁과 같고, 변마다 2명 앉는 정사각형 탁자는 원순열 × 2."""

    def construct(self):
        # 1부: 정팔각형 탁자, 변마다 1명
        c = LEFT * 2.2 + UP * 0.4
        octagon = RegularPolygon(8, start_angle=PI / 2 - PI / 8, radius=1.8, fill_color=WOOD, fill_opacity=1,
                                 stroke_color=WOOD_EDGE, stroke_width=5).move_to(c)
        dist = 1.8 * np.cos(PI / 8) + 0.45
        ang = ValueTracker(0)

        def pos(k):
            a = PI / 2 - k * TAU / 8 - ang.get_value()
            return c + dist * np.array([np.cos(a), np.sin(a), 0])

        people = VGroup(*[person(ch, r=0.34) for ch in "ABCDEFGH"])
        for k, p in enumerate(people):
            p.move_to(pos(k))
        people.add_updater(lambda m: [m[k].move_to(pos(k)) for k in range(8)])
        self.play(FadeIn(octagon), LaggedStart(*[FadeIn(p, scale=0.5) for p in people], lag_ratio=0.1))
        cap = caption("정팔각형 탁자, 각 변에 1명씩 8명")
        self.play(FadeIn(cap))
        cap = swap_caption(self, cap, "한 칸씩 돌려도 탁자 모양 그대로")
        for _ in range(2):
            self.play(ang.animate.increment_value(TAU / 8), run_time=1.0)
        same = VGroup(Text("원탁과 같음", font_size=30, color=ORANGE, weight=BOLD),
                      Text("(8 − 1)! = 7!", font_size=34, weight=BOLD)).arrange(DOWN, buff=0.3).move_to(RIGHT * 3.0 + UP * 0.4)
        self.play(Write(same))
        cap = swap_caption(self, cap, "모든 자리가 회전으로 겹침 → 원순열의 수 그대로")
        self.wait(2)
        people.clear_updaters()
        self.play(FadeOut(VGroup(octagon, people, same)))

        # 2부: 정사각형 탁자, 변마다 2명
        def square_seats(center):
            o, d = 0.6, 1.2 + 0.48
            pts = [(-o, d), (o, d), (d, o), (d, -o), (o, -d), (-o, -d), (-d, -o), (-d, o)]
            return [center + np.array([x, y, 0]) for x, y in pts]

        lc, rc = LEFT * 2.6 + UP * 0.5, RIGHT * 2.6 + UP * 0.5
        tables = VGroup(*[Square(2.4, fill_color=WOOD, fill_opacity=1, stroke_color=WOOD_EDGE, stroke_width=5).move_to(p)
                          for p in (lc, rc)])
        order = "ABCDEFGH"
        left_p = VGroup(*[person(ch, r=0.3).move_to(p) for ch, p in zip(order, square_seats(lc))])
        right_p = VGroup(*[person(ch, r=0.3).move_to(p) for ch, p in zip(order, square_seats(rc))])
        cap = swap_caption(self, cap, "정사각형 탁자, 각 변에 2명씩 8명")
        self.play(FadeIn(tables), FadeIn(left_p), FadeIn(right_p))
        labels = VGroup(Text("배치 ①", font_size=24).next_to(tables[0], DOWN, buff=1.15),
                        Text("배치 ② = 모두 한 칸 이동", font_size=24, color=ORANGE).next_to(tables[1], DOWN, buff=1.15))
        seats_r = square_seats(rc)
        self.play(*[p.animate.move_to(seats_r[(k + 1) % 8]) for k, p in enumerate(right_p)], FadeIn(labels), run_time=1.5)
        cap = swap_caption(self, cap, "원탁이면 같은 배치지만 정사각형에서는?")
        self.play(Indicate(left_p[0], color=ORANGE, scale_factor=1.5), Indicate(right_p[0], color=ORANGE, scale_factor=1.5))
        cap = swap_caption(self, cap, "A가 변의 왼쪽 끝 ↔ 오른쪽 끝: 회전해도 겹치지 않는 <b>다른 배치</b>")
        self.wait(2)
        f = Text("원순열 7! × 2 = 10080", font_size=32, color=ORANGE, weight=BOLD).move_to(DOWN * 2.45)
        self.play(FadeOut(labels), Write(f))
        cap = swap_caption(self, cap, "원순열 1가지마다 서로 다른 배치 2가지")
        self.wait(3)


class NecklaceFlip(Scene):
    """비유: 팔찌는 뒤집어 찰 수 있음 → 시계/반시계 방향 배열이 같은 것."""

    def construct(self):
        colors = [RED, ORANGE, GOLD, GREEN, BLUE]

        def bracelet(center):
            string = Circle(radius=1.4, color=GRAY, stroke_width=4).move_to(center)
            beads = VGroup(*[Circle(radius=0.32, fill_color=col, fill_opacity=1, stroke_color=WHITE, stroke_width=3)
                             .move_to(p) for col, p in zip(colors, seat_points(center, 1.4, 5))])
            return VGroup(string, beads)

        lc, rc = LEFT * 2.6 + UP * 0.45, RIGHT * 2.6 + UP * 0.45
        left = bracelet(lc)
        self.play(Create(left[0]), LaggedStart(*[GrowFromCenter(b) for b in left[1]], lag_ratio=0.15))
        l_arrow = turn_arrow(lc, 0.75, cw=True)
        self.play(Create(l_arrow))
        cap = caption("구슬 5개를 꿴 팔찌 (시계 방향: 빨·주·노·초·파)")
        self.play(FadeIn(cap))
        self.wait(0.8)

        right = left.copy()
        self.play(right.animate.move_to(rc), run_time=1.0)
        cap = swap_caption(self, cap, "오른쪽 팔찌를 뒤집으면?")
        self.play(Rotate(right, PI, axis=UP, about_point=rc), run_time=2)
        r_arrow = turn_arrow(rc, 0.75, cw=False, color=ORANGE)
        self.play(Create(r_arrow))
        labels = VGroup(Text("원래 팔찌", font_size=24).next_to(lc + DOWN * 1.75, DOWN, buff=0.1),
                        Text("뒤집은 팔찌", font_size=24, color=ORANGE).next_to(rc + DOWN * 1.75, DOWN, buff=0.1))
        self.play(FadeIn(labels))
        cap = swap_caption(self, cap, "순서가 반시계 방향으로 바뀜 → 원순열로는 서로 다른 2가지")
        self.wait(1.5)
        cap = swap_caption(self, cap, "하지만 팔찌로는 <b>같은 1가지</b> → 원순열 수를 2로 나누기")
        f = Text("팔찌 수 = (n − 1)! ÷ 2     n = 5 → 24 ÷ 2 = 12", font_size=28, color=ORANGE, weight=BOLD) \
            .move_to(DOWN * 2.6)
        self.play(Write(f))
        self.wait(3)


class NeighborsGlue(Scene):
    """이웃 조건: A와 B를 한 묶음으로 보고 원순열 → 묶음 안 순서 곱하기."""

    def construct(self):
        people = VGroup(*[person(ch, r=0.4) for ch in "ABCDEF"]).arrange(RIGHT, buff=0.45).move_to(UP * 2.7)
        A, B = people[0], people[1]
        self.play(LaggedStart(*[FadeIn(p, scale=0.5) for p in people], lag_ratio=0.12))
        cap = caption("6명이 원탁에 앉을 때 A와 B는 반드시 이웃")
        self.play(FadeIn(cap), Indicate(A, color=ORANGE), Indicate(B, color=ORANGE))

        self.play(B.animate.next_to(A, RIGHT, buff=0.08), people[2:].animate.shift(LEFT * 0.4))
        band = SurroundingRectangle(VGroup(A, B), color=ORANGE, buff=0.1, corner_radius=0.3, stroke_width=5)
        block = VGroup(band, A, B)
        self.play(Create(band))
        cap = swap_caption(self, cap, "A와 B를 끈으로 묶어 <b>한 사람</b>처럼 취급 → 묶음 1개 + 4명 = 5개")
        self.wait(1)

        tc, R = LEFT * 1.7 + DOWN * 0.35, 1.35
        seats = seat_points(tc, R + 0.55, 5)
        self.play(FadeIn(table(tc, R)))
        self.play(block.animate.move_to(seats[0]), *[p.animate.move_to(s) for p, s in zip(people[2:], seats[1:])],
                  run_time=1.6)
        panel = VGroup(Text("① 5개의 원순열", font_size=26), Text("(5 − 1)! = 24", font_size=30, weight=BOLD),
                       Text("② 묶음 안 순서", font_size=26), Text("AB, BA → 2! = 2", font_size=30, weight=BOLD),
                       Text("24 × 2 = 48", font_size=40, color=ORANGE, weight=BOLD)) \
            .arrange(DOWN, buff=0.28, aligned_edge=LEFT).move_to(RIGHT * 3.2 + UP * 0.2)
        panel[4].shift(DOWN * 0.2)
        cap = swap_caption(self, cap, "묶음 1개와 C, D, E, F를 원탁에 배치")
        self.play(Write(panel[0]), Write(panel[1]))
        self.wait(1)
        cap = swap_caption(self, cap, "묶음 안에서 A와 B의 자리 바꾸기")
        self.play(Swap(A, B), run_time=1.2)
        self.play(Write(panel[2]), Write(panel[3]))
        self.play(Write(panel[4]))
        cap = swap_caption(self, cap, "이웃 조건: <b>묶어서 원순열</b> × <b>묶음 안 순서</b>")
        self.wait(3)
