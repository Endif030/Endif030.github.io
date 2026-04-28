(function () {
  const STATE_KEY = "spanish_review_state_v1";
  const DEFAULT_POLICY = {
    normal: { softCap: 15, hardCap: 20 },
    boost: { softCap: 25, hardCap: 35 }
  };

  function nowISO() { return new Date().toISOString(); }
  function addDays(date, d) { const x = new Date(date); x.setDate(x.getDate() + d); return x; }
  const intervals = [1, 2, 4, 7, 15, 30];

  function getState() {
    try {
      return JSON.parse(localStorage.getItem(STATE_KEY) || "{}");
    } catch { return {}; }
  }
  function saveState(s) { localStorage.setItem(STATE_KEY, JSON.stringify(s)); }

  function ensure(s) {
    s.memory = s.memory || {};
    s.lastResult = s.lastResult || {};
    s.deferredQueue = s.deferredQueue || [];
    return s;
  }

  function ensureUnit(unitId, s) {
    if (!s.memory[unitId]) {
      s.memory[unitId] = { level: 0, nextReviewAt: nowISO(), wrongCount: 0, lastReviewedAt: null };
    }
    return s.memory[unitId];
  }

  function buildPracticeSet(day, mode) {
    const s = ensure(getState());
    const policy = DEFAULT_POLICY[mode] || DEFAULT_POLICY.normal;
    const items = day.practiceItems || [];

    // attach unit ids if absent
    const normalized = items.map((q, idx) => ({ ...q, id: q.id || `${day.id}_q_${idx+1}`, unitIds: q.unitIds || [q.answer?.toLowerCase?.().replace(/\s+/g, "_") || `unit_${idx+1}`], sourceDay: q.sourceDay || day.id }));

    const today = new Date();
    const dueUnits = Object.entries(s.memory)
      .filter(([,v]) => new Date(v.nextReviewAt) <= today)
      .map(([k]) => k);

    const coveredByNew = new Set(normalized.flatMap(q => q.unitIds));
    const mergedUnits = dueUnits.filter(u => coveredByNew.has(u));
    const reviewOnlyUnits = dueUnits.filter(u => !coveredByNew.has(u));

    const reviewQuestions = reviewOnlyUnits.map((u, i) => ({
      id: `review_${u}_${i}`,
      type: "spelling",
      prompt: `复习：请写出 ${u.replaceAll("_", " ")}`,
      answer: u.replaceAll("_", " "),
      hint: "来自历史复习",
      unitIds: [u],
      sourceDay: "review"
    }));

    let assembled = [...normalized, ...reviewQuestions];
    const deferred = [];
    if (assembled.length > policy.hardCap) {
      deferred.push(...assembled.slice(policy.hardCap));
      assembled = assembled.slice(0, policy.hardCap);
    }

    s.deferredQueue = [...s.deferredQueue, ...deferred.map(q => ({ ...q, deferredAt: nowISO() }))];
    saveState(s);

    return {
      mode,
      policy,
      totalRaw: normalized.length + reviewQuestions.length,
      mergedCount: mergedUnits.length,
      deferredCount: deferred.length,
      items: assembled,
      stats: {
        newCount: normalized.length,
        reviewCount: reviewQuestions.length,
        finalCount: assembled.length
      }
    };
  }

  function gradeAndUpdate(dayId, practiceSet, answers) {
    const s = ensure(getState());
    let correct = 0;
    const results = practiceSet.items.map((q, i) => {
      const input = (answers[i] || "").trim().toLowerCase().replace(/[。\.]/g, "").replace(/\s+/g, " ");
      const std = (q.answer || "").trim().toLowerCase().replace(/[。\.]/g, "").replace(/\s+/g, " ");
      const ok = input === std;
      if (ok) correct += 1;

      (q.unitIds || []).forEach(uid => {
        const u = ensureUnit(uid, s);
        u.lastReviewedAt = nowISO();
        if (ok) {
          u.level = Math.min(5, (u.level || 0) + 1);
        } else {
          u.level = Math.max(0, (u.level || 0) - 1);
          u.wrongCount = (u.wrongCount || 0) + 1;
        }
        u.nextReviewAt = addDays(new Date(), intervals[u.level] || 1).toISOString();
      });

      return { questionId: q.id, ok, input, answer: q.answer };
    });

    s.lastResult[dayId] = {
      score: correct,
      total: practiceSet.items.length,
      mode: practiceSet.mode,
      mergedCount: practiceSet.mergedCount,
      deferredCount: practiceSet.deferredCount,
      at: nowISO()
    };

    saveState(s);
    return { score: correct, total: practiceSet.items.length, results, summary: s.lastResult[dayId] };
  }

  function getSummary(dayId) {
    const s = ensure(getState());
    return s.lastResult[dayId] || null;
  }

  window.reviewEngine = { buildPracticeSet, gradeAndUpdate, getSummary };
})();
