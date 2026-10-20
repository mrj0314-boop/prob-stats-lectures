// 웹 슬라이드덱: 화면 맞춤 확대·축소, 키보드·터치 넘기기, 진행 막대와 쪽 번호 자동 표시
(() => {
  const stage = document.querySelector('.stage');
  const slides = [...stage.querySelectorAll('.slide')];
  const footer = stage.dataset.footer || '';
  const counter = document.querySelector('#counter');
  let cur = 0;

  slides.forEach((s, i) => {
    if (!s.classList.contains('cover')) {
      if (s.querySelector('.bar')) {
        const p = document.createElement('div');
        p.className = 'progress';
        p.style.width = `${((i + 1) / slides.length) * 100}%`;
        s.append(p);
      }
      const f = document.createElement('div');
      f.className = 'foot';
      f.innerHTML = `<span>${footer}</span><span>${i + 1} / ${slides.length}</span>`;
      s.append(f);
    }
  });

  function fit() {
    const k = Math.min(innerWidth / 1920, innerHeight / 1080);
    stage.style.transform = `scale(${k}) translate(-50%, -50%)`;
  }

  function show(i) {
    cur = Math.max(0, Math.min(slides.length - 1, i));
    slides.forEach((s, j) => {
      s.classList.toggle('active', j === cur);
      // 영상은 보이는 슬라이드에서만 재생 (브라우저 정책상 처음엔 소리 끔)
      s.querySelectorAll('video').forEach(v => (j === cur ? v.play().catch(() => {}) : v.pause()));
    });
    counter.textContent = `${cur + 1} / ${slides.length}`;
    history.replaceState(null, '', `#${cur + 1}`);
  }

  addEventListener('resize', fit);
  addEventListener('keydown', e => {
    if (['ArrowRight', 'PageDown', ' ', 'Enter'].includes(e.key)) { e.preventDefault(); show(cur + 1); }
    else if (['ArrowLeft', 'PageUp', 'Backspace'].includes(e.key)) { e.preventDefault(); show(cur - 1); }
    else if (e.key === 'Home') show(0);
    else if (e.key === 'End') show(slides.length - 1);
    else if (e.key === 'f' || e.key === 'F') document.documentElement.requestFullscreen?.();
  });
  let x0 = null;
  addEventListener('touchstart', e => { x0 = e.touches[0].clientX; }, { passive: true });
  addEventListener('touchend', e => {
    const dx = e.changedTouches[0].clientX - x0;
    if (Math.abs(dx) > 50) show(cur + (dx < 0 ? 1 : -1));
  });
  document.querySelector('#prev').onclick = () => show(cur - 1);
  document.querySelector('#next').onclick = () => show(cur + 1);
  document.querySelector('#full').onclick = () => document.documentElement.requestFullscreen?.();

  fit();
  show((parseInt(location.hash.slice(1), 10) || 1) - 1);
})();
