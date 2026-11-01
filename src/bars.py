# 카탈로그 4쪽 그림처럼 베어링 바 1본을 비스듬히 본 그림
def bar_svg(kind):
    X0, YT, H, DX, DY = 22, 34, 60, 92, 30   # 앞 끝 위치, 높이, 깊이 방향
    S = '#231916'; FACE = '#d3d7da'; FACE2 = '#bcc2c6'; END = '#8e969b'
    serr = kind in ('si', 'sf')
    ibar = kind in ('i', 'si')
    def top_pt(t, dip=0):
        return (X0 + DX * t, YT - DY * t + dip)
    # 윗변(톱니면 반원 홈)
    top = []
    n = 5
    if serr:
        for k in range(n + 1):
            top.append(top_pt(k / n))
            if k < n:
                for j in range(1, 8):
                    tt = (k + j / 8) / n
                    import math
                    dip = 6 * math.sin(math.pi * j / 8) if 0.15 < (j / 8) < 0.85 or True else 0
                    top.append(top_pt(tt, dip if j in range(2, 7) else dip * 0.3))
    else:
        top = [top_pt(0), top_pt(1)]
    bot = [(X0 + DX, YT - DY + H), (X0, YT + H)]
    pts = top + bot
    d = 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pts) + 'Z'
    out = [f'<path d="{d}" fill="{FACE}" stroke="{S}" stroke-width="1.3" stroke-linejoin="round"/>']
    if ibar:
        # 위아래 볼록한 띠(I형 단면의 머리 부분)
        b = 8
        out.append(f'<path d="M{X0} {YT+b+ (6 if serr else 0)} L{X0+DX} {YT-DY+b+(6 if serr else 0)}" stroke="{S}" stroke-width="1" opacity=".55"/>')
        out.append(f'<path d="M{X0} {YT+H-b} L{X0+DX} {YT-DY+H-b}" stroke="{S}" stroke-width="1" opacity=".55"/>')
        out.append(f'<path d="M{X0} {YT+H-b} L{X0+DX} {YT-DY+H-b} L{X0+DX} {YT-DY+H} L{X0} {YT+H}Z" fill="{FACE2}"/>')
        # 단면(I형): 머리·다리가 웨브보다 두껍다
        y1 = YT + (6 if serr else 0)
        y2 = YT + H
        prof = (f'M{X0} {y1} L{X0-9} {y1+2} L{X0-10} {y1+b} L{X0-6} {y1+b+3} L{X0-6} {y2-b-3} '
                f'L{X0-10} {y2-b} L{X0-9} {y2-1} L{X0} {y2}Z')
    else:
        y1 = YT + (6 if serr else 0)
        prof = f'M{X0} {y1} L{X0-7} {y1+2} L{X0-7} {YT+H+2} L{X0} {YT+H}Z'
    out.append(f'<path d="{prof}" fill="{END}" stroke="{S}" stroke-width="1.3" stroke-linejoin="round"/>')
    return f'<svg viewBox="0 0 124 100" aria-hidden="true">{"".join(out)}</svg>'

if __name__ == '__main__':
    html = '<body style="background:#fff">' + ''.join(f'<div style="display:inline-block;width:220px;border:1px solid #ddd;margin:8px">{bar_svg(k)}</div>' for k in ('i','f','si','sf')) + '</body>'
    open('/tmp/claude-0/-home-claude/d96c5727-e734-5c56-b33c-0c0f3100ab1b/scratchpad/bars.html','w').write(html)
