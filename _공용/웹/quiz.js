// 간단 퀴즈: 페이지에 window.QUIZ = [{q, options, answer, explain} | {q, number, explain}] 를 두고 이 파일을 불러옴
(() => {
  const root = document.querySelector('#quiz');
  const scoreEl = document.querySelector('#score');
  const shuffle = a => a.map(v => [Math.random(), v]).sort((x, y) => x[0] - y[0]).map(v => v[1]);
  let solved;

  function render() {
    solved = new Map();
    root.innerHTML = '';
    QUIZ.forEach((item, i) => {
      const card = document.createElement('section');
      card.className = 'panel q';
      card.innerHTML = `<p class="eyebrow">문제 ${i + 1}</p><p class="qt">${item.q}</p><div class="ans"></div>
        <div class="fb" role="status" aria-live="polite"></div>`;
      const ans = card.querySelector('.ans');
      const fb = card.querySelector('.fb');
      const grade = ok => {
        if (!solved.has(i)) solved.set(i, ok);     // 첫 시도만 점수에 반영
        fb.className = `fb ${ok ? 'ok' : 'bad'}`;
        fb.innerHTML = ok ? `<b>정답</b> · ${item.explain}` : '<b>다시 생각해 보기</b> · ' + (item.hint || '회전·뒤집기로 겹치는 경우 확인');
        if (ok) card.querySelectorAll('button, input').forEach(el => (el.disabled = true));
        updateScore();
      };
      if (item.options) {
        shuffle(item.options.map((t, k) => [t, k])).forEach(([t, k]) => {
          const b = document.createElement('button');
          b.className = 'btn opt';
          b.textContent = t;
          b.onclick = () => { b.classList.add(k === item.answer ? 'right' : 'wrong'); grade(k === item.answer); };
          ans.append(b);
        });
      } else {
        ans.innerHTML = `<input type="number" inputmode="numeric" aria-label="문제 ${i + 1} 답" placeholder="답 (숫자)">
          <button class="btn primary">확인</button>`;
        const inp = ans.querySelector('input');
        const go = () => inp.value !== '' && grade(Number(inp.value) === item.number);
        ans.querySelector('button').onclick = go;
        inp.onkeydown = e => e.key === 'Enter' && go();
      }
      root.append(card);
    });
    updateScore();
  }

  function updateScore() {
    const right = [...solved.values()].filter(Boolean).length;
    scoreEl.innerHTML = solved.size === QUIZ.length
      ? `<b>결과: ${QUIZ.length}문제 중 첫 시도 정답 ${right}개</b>`
      : `푼 문제 ${solved.size} / ${QUIZ.length} · 첫 시도 정답 ${right}개`;
  }

  document.querySelector('#retry').onclick = () => { render(); scrollTo({ top: 0, behavior: 'smooth' }); };
  render();
})();
