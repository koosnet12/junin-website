(function () {
  // 모바일 메뉴
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('site-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  // 공정 영상 구간 이동
  var video = document.getElementById('process-video');
  document.querySelectorAll('[data-seek]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      if (!video) return;
      video.currentTime = parseFloat(btn.getAttribute('data-seek')) || 0;
      var p = video.play();
      if (p && p.catch) p.catch(function () {});
    });
  });

  // 견적 문의 양식
  // 정적 사이트라 서버 전송 대신 메일 프로그램을 엽니다.
  // 배포할 때 폼 접수 서비스(예: Formspree, Netlify Forms)를 연결하면 data-endpoint에 주소를 넣으세요.
  var form = document.getElementById('quote-form');
  if (form) {
    var status = document.getElementById('form-status');
    var TO = form.getAttribute('data-mailto');
    var endpoint = form.getAttribute('data-endpoint');
    function show(msg, err) {
      status.hidden = false;
      status.className = 'form-status' + (err ? ' err' : '');
      status.innerHTML = msg;
      status.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    }
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      var d = new FormData(form);
      var type = d.get('type') || '견적 요청';
      var lines = [
        '[문의 유형] ' + type,
        '[회사명] ' + (d.get('company') || ''),
        '[담당자] ' + (d.get('name') || ''),
        '[연락처] ' + (d.get('phone') || ''),
        '[이메일] ' + (d.get('email') || ''),
        '[현장·프로젝트] ' + (d.get('project') || ''),
        '[규격·수량] ' + (d.get('spec') || ''),
        '[납기 희망일] ' + (d.get('due') || ''),
        '',
        d.get('message') || ''
      ];
      if (endpoint) {
        fetch(endpoint, { method: 'POST', body: d, headers: { Accept: 'application/json' } })
          .then(function (r) {
            if (!r.ok) throw new Error();
            form.reset();
            show('<strong>문의가 접수되었습니다.</strong> 담당자가 확인 후 연락드리겠습니다.');
          })
          .catch(function () {
            show('전송하지 못했습니다. 잠시 후 다시 시도하시거나 <strong>' + TO + '</strong> 로 메일을 보내 주세요.', true);
          });
        return;
      }
      var subject = '[홈페이지 ' + type + '] ' + (d.get('company') || '') + ' ' + (d.get('name') || '');
      var href = 'mailto:' + TO + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(lines.join('\n'));
      show('메일 프로그램에서 작성된 메일을 확인하고 보내 주세요. 메일 창이 열리지 않으면 <strong>' + TO + '</strong> 로 직접 보내 주시고, 도면 파일은 메일에 첨부해 주세요.');
      window.location.href = href;
    });
  }
})();
