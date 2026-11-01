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
    var EN = (document.documentElement.lang || '').slice(0, 2) === 'en';
    var L = EN ? {
      type: 'Inquiry type', company: 'Company', name: 'Contact name', phone: 'Phone', email: 'E-mail',
      country: 'Country', project: 'Project', spec: 'Specification / quantity', due: 'Required delivery date',
      def: 'Quotation', subj: 'Website',
      ok: '<strong>Thank you. Your inquiry has been received.</strong> Our team will get back to you shortly.',
      fail: function (to) { return 'Your inquiry could not be sent. Please try again later or e-mail us at <strong>' + to + '</strong>.'; },
      mail: function (to) { return 'Please check and send the e-mail prepared in your mail app. If it does not open, e-mail us directly at <strong>' + to + '</strong> and attach your drawings.'; }
    } : {
      type: '문의 유형', company: '회사명', name: '담당자', phone: '연락처', email: '이메일',
      country: '국가', project: '현장·프로젝트', spec: '규격·수량', due: '납기 희망일',
      def: '견적 요청', subj: '홈페이지',
      ok: '<strong>문의가 접수되었습니다.</strong> 담당자가 확인 후 연락드리겠습니다.',
      fail: function (to) { return '전송하지 못했습니다. 잠시 후 다시 시도하시거나 <strong>' + to + '</strong> 로 메일을 보내 주세요.'; },
      mail: function (to) { return '메일 프로그램에서 작성된 메일을 확인하고 보내 주세요. 메일 창이 열리지 않으면 <strong>' + to + '</strong> 로 직접 보내 주시고, 도면 파일은 메일에 첨부해 주세요.'; }
    };
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      var d = new FormData(form);
      var type = d.get('type') || L.def;
      var lines = ['[' + L.type + '] ' + type];
      ['company', 'name', 'phone', 'email', 'country', 'project', 'spec', 'due'].forEach(function (k) {
        if (k === 'country' && !form.elements.country) return;
        lines.push('[' + L[k] + '] ' + (d.get(k) || ''));
      });
      lines.push('', d.get('message') || '');
      if (endpoint) {
        fetch(endpoint, { method: 'POST', body: d, headers: { Accept: 'application/json' } })
          .then(function (r) {
            if (!r.ok) throw new Error();
            form.reset();
            show(L.ok);
          })
          .catch(function () {
            show(L.fail(TO), true);
          });
        return;
      }
      var subject = '[' + L.subj + ' ' + type + '] ' + (d.get('company') || '') + ' ' + (d.get('name') || '');
      var href = 'mailto:' + TO + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(lines.join('\n'));
      show(L.mail(TO));
      window.location.href = href;
    });
  }
})();
