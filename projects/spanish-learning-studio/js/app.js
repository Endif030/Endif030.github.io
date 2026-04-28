(function () {
  function qs(id) { return document.getElementById(id); }

  function getCurrentDay() {
    const url = new URL(window.location.href);
    const dayId = url.searchParams.get("day") || window.siteConfig.defaultDayId;
    return window.curriculum.find(d => d.id === dayId) || window.curriculum[0];
  }

  const PREF_KEY = "spanish_studio_voice_prefs_v1";

  function saveVoicePrefs() {
    const select = qs("voiceSelect");
    const rate = qs("rate");
    const pitch = qs("pitch");
    try {
      localStorage.setItem(PREF_KEY, JSON.stringify({
        voiceName: select?.value || "",
        rate: Number(rate?.value || 1),
        pitch: Number(pitch?.value || 1)
      }));
    } catch (e) {}
  }

  function loadVoicePrefs() {
    try {
      const data = JSON.parse(localStorage.getItem(PREF_KEY) || "{}");
      const migrated = localStorage.getItem("spanish_voice_pref_migrated_v2");
      if (!migrated) {
        // one-time migration: reset legacy default to ensure Google español(es-ES) can be auto-selected
        if (data.voiceName && !/google español/i.test(data.voiceName)) {
          delete data.voiceName;
          localStorage.setItem(PREF_KEY, JSON.stringify(data));
        }
        localStorage.setItem("spanish_voice_pref_migrated_v2", "1");
      }
      return data;
    } catch (e) {
      return {};
    }
  }

  function getVoicePrefs() {
    const voiceName = qs("voiceSelect")?.value || "";
    const rate = Number(qs("rate")?.value || 1);
    const pitch = Number(qs("pitch")?.value || 1);
    return { voiceName, rate, pitch };
  }

  function resolveVoice() {
    const voices = window.speechSynthesis.getVoices() || [];
    const prefs = getVoicePrefs();
    if (prefs.voiceName) {
      const byName = voices.find(v => v.name === prefs.voiceName);
      if (byName) return byName;
    }
    return voices.find(v => v.lang === window.siteConfig.languageCode) || voices.find(v => v.lang === window.siteConfig.fallbackLanguageCode) || voices[0];
  }

  function speak(text, slow) {
    if (!("speechSynthesis" in window)) return;
    const u = new SpeechSynthesisUtterance(text);
    const prefs = getVoicePrefs();
    const voice = resolveVoice();
    if (voice) u.voice = voice;
    u.lang = voice?.lang || window.siteConfig.languageCode;
    u.rate = slow ? Math.max(0.6, prefs.rate - 0.2) : prefs.rate;
    u.pitch = prefs.pitch;
    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(u);
  }

  function renderVoiceControls() {
    const select = qs("voiceSelect");
    const rate = qs("rate");
    const pitch = qs("pitch");
    const rateValue = qs("rateValue");
    const pitchValue = qs("pitchValue");
    const voiceHint = qs("voiceHint");
    if (!select || !rate || !pitch) return;

    const allVoices = window.speechSynthesis.getVoices() || [];
    const voices = allVoices.filter(v => v.lang?.startsWith("es"));
    const all = voices.length ? voices : allVoices;

    const stored = loadVoicePrefs();
    const current = select.value || stored.voiceName || "";
    select.innerHTML = "";

    if (!all.length) {
      const opt = document.createElement("option");
      opt.value = "";
      opt.textContent = "暂无可用音色（请点刷新或稍等1-2秒）";
      select.appendChild(opt);
      if (voiceHint) voiceHint.textContent = "当前浏览器尚未加载语音引擎，可点击“刷新音色列表”重试。";
    } else {
      all.forEach(v => {
        const opt = document.createElement("option");
        opt.value = v.name;
        opt.textContent = `${v.name} (${v.lang})`;
        select.appendChild(opt);
      });
      if (voiceHint) voiceHint.textContent = voices.length
        ? `已加载 ${voices.length} 个西语音色`
        : `未检测到西语音色，已显示全部 ${all.length} 个系统音色`;
    }

    if (current) select.value = current;
    if (!select.value && all[0]) {
      const preferred = all.find(v => v.name.trim() === "Google español" && /es-ES/i.test(v.lang))
        || all.find(v => /google español/i.test(v.name) && /es-ES/i.test(v.lang))
        || all.find(v => /google español/i.test(v.name))
        || all.find(v => /es-ES/i.test(v.lang))
        || all.find(v => /es-MX/i.test(v.lang))
        || all[0];
      select.value = preferred.name;
      saveVoicePrefs();
    }

    if (stored.rate && !rate.dataset.inited) rate.value = String(stored.rate);
    if (stored.pitch && !pitch.dataset.inited) pitch.value = String(stored.pitch);
    rate.dataset.inited = "1";
    pitch.dataset.inited = "1";

    rateValue.textContent = Number(rate.value).toFixed(2);
    pitchValue.textContent = Number(pitch.value).toFixed(2);
  }

  function renderPracticeSummary(day) {
    const summary = window.reviewEngine?.getSummary?.(day.id);
    const box = qs("practiceSummary");
    const start = qs("startPractice");
    const boost = qs("startBoost");
    if (!box || !start || !boost) return;
    start.href = `practice.html?day=${day.id}&mode=normal`;
    boost.href = `practice.html?day=${day.id}&mode=boost`;
    if (!summary) {
      box.innerHTML = "<strong>今日练习状态：</strong>未开始（常规模式：软15 / 硬20）";
      return;
    }
    box.innerHTML = `<strong>最近练习：</strong>${summary.score}/${summary.total} · 模式：${summary.mode === 'boost' ? '错题巩固' : '常规'} · 合并 ${summary.mergedCount} · 顺延 ${summary.deferredCount}`;
  }

  function render() {
    renderVoiceControls();
    const day = getCurrentDay();
    const state = window.progressStore.getDay(day.id);
    qs("title").textContent = `Day ${day.dayNumber} · ${day.title}`;

    const goalUl = qs("goals");
    goalUl.innerHTML = "";
    day.goals.forEach(g => {
      const li = document.createElement("li");
      li.textContent = g;
      goalUl.appendChild(li);
    });

    const vocabWrap = qs("vocab");
    vocabWrap.innerHTML = "";
    day.vocab.forEach(v => {
      const card = document.createElement("div");
      card.className = "card";
      card.innerHTML = `<strong>${v.es}</strong><div>${v.zh}</div><div class="muted">/${v.ipa}/ · ${v.hint}</div>`;
      vocabWrap.appendChild(card);
    });

    const sentenceWrap = qs("sentences");
    sentenceWrap.innerHTML = "";
    day.sentences.forEach((s, i) => {
      const row = document.createElement("div");
      row.className = "sentence";
      const checked = state.completedSentenceIds.includes(i) ? "checked" : "";
      row.innerHTML = `
        <div>
          <div><strong>${s.es}</strong></div>
          <div>${s.zh}</div>
          <div class="muted">/${s.ipa}/</div>
        </div>
        <div class="actions">
          <button data-act="slow" data-i="${i}">慢速</button>
          <button data-act="normal" data-i="${i}">正常</button>
          <label><input type="checkbox" data-act="done" data-i="${i}" ${checked}/> 已跟读</label>
        </div>`;
      sentenceWrap.appendChild(row);
    });

    qs("task").textContent = `口语任务：${day.practice.outputTask}`;
    qs("shadowing").textContent = day.practice.shadowing;
    renderPracticeSummary(day);

    const progress = Math.round((state.completedSentenceIds.length / day.sentences.length) * 100);
    qs("progress").textContent = `今日跟读进度：${state.completedSentenceIds.length}/${day.sentences.length}（${progress}%）`;
    qs("finished").checked = !!state.finished;
  }

  document.addEventListener("click", (e) => {
    const el = e.target;
    if (!(el instanceof HTMLElement)) return;
    const act = el.getAttribute("data-act");
    const i = Number(el.getAttribute("data-i"));
    const day = getCurrentDay();
    if (act === "slow") speak(day.sentences[i].es, true);
    if (act === "normal") speak(day.sentences[i].es, false);
  });

  document.addEventListener("change", (e) => {
    const el = e.target;
    const day = getCurrentDay();

    if (el instanceof HTMLInputElement) {
      const act = el.getAttribute("data-act");
      const i = Number(el.getAttribute("data-i"));
      if (act === "done") {
        window.progressStore.setSentenceDone(day.id, i, el.checked);
        render();
      }
      if (el.id === "finished") {
        window.progressStore.setFinished(day.id, el.checked);
      }
      if (el.id === "rate" || el.id === "pitch") {
        renderVoiceControls();
      }
    }

    if (el instanceof HTMLSelectElement && el.id === "voiceSelect") {
      saveVoicePrefs();
    }

    if ((el instanceof HTMLInputElement) && (el.id === "rate" || el.id === "pitch")) {
      saveVoicePrefs();
    }
  });

  const previewBtn = qs("previewVoice");
  if (previewBtn) {
    previewBtn.addEventListener("click", () => {
      speak("Hola, mucho gusto. Soy tu profesor de español.", false);
    });
  }

  const refreshBtn = qs("refreshVoices");
  if (refreshBtn) {
    refreshBtn.addEventListener("click", () => renderVoiceControls());
  }

  const submitBtn = qs("practiceSubmit");
  const nextBtn = qs("practiceNext");
  if (submitBtn) {
    submitBtn.addEventListener("click", () => {
      const day = getCurrentDay();
      const items = day.practiceItems || [];
      if (!items.length) return;
      const item = items[Math.min(practiceIndex, items.length - 1)];
      const input = normalize(qs("practiceInput")?.value || "");
      const answer = normalize(item.answer || "");
      const ok = input === answer;
      if (ok) practiceScore += 1;
      const feedback = qs("practiceFeedback");
      if (feedback) {
        feedback.textContent = ok
          ? `✅ 正确`
          : `❌ 不对。正确答案：${item.answer}；提示：${item.hint || "继续加油"}`;
      }
      const pProgress = qs("practiceProgress");
      if (pProgress) pProgress.textContent = `进度：${Math.min(practiceIndex + 1, items.length)}/${items.length} · 得分：${practiceScore}`;
    });
  }
  if (nextBtn) {
    nextBtn.addEventListener("click", () => {
      const day = getCurrentDay();
      const items = day.practiceItems || [];
      if (!items.length) return;
      practiceIndex = Math.min(practiceIndex + 1, items.length - 1);
      renderPractice(day);
    });
  }

  const toggleBtn = qs("toggleSettings");
  const settingsPanel = qs("settingsPanel");
  if (toggleBtn && settingsPanel) {
    toggleBtn.addEventListener("click", () => {
      settingsPanel.classList.toggle("hidden");
    });
  }

  function scheduleVoiceWarmup() {
    [0, 300, 1000, 2000].forEach(ms => {
      setTimeout(() => renderVoiceControls(), ms);
    });
  }

  window.speechSynthesis?.addEventListener?.("voiceschanged", () => renderVoiceControls());
  render();
  scheduleVoiceWarmup();
})();
