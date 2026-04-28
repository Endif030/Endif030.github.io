(function () {
  const KEY = "spanish_studio_progress_v1";

  function read() {
    try {
      return JSON.parse(localStorage.getItem(KEY) || "{}");
    } catch (e) {
      return {};
    }
  }

  function write(data) {
    try {
      localStorage.setItem(KEY, JSON.stringify(data));
    } catch (e) {
      console.warn("save failed", e);
    }
  }

  window.progressStore = {
    getDay(dayId) {
      const data = read();
      return data[dayId] || { completedSentenceIds: [], finished: false };
    },
    setSentenceDone(dayId, sentenceIndex, done) {
      const data = read();
      const current = data[dayId] || { completedSentenceIds: [], finished: false };
      const set = new Set(current.completedSentenceIds);
      if (done) set.add(sentenceIndex);
      else set.delete(sentenceIndex);
      current.completedSentenceIds = Array.from(set).sort((a, b) => a - b);
      data[dayId] = current;
      write(data);
    },
    setFinished(dayId, finished) {
      const data = read();
      const current = data[dayId] || { completedSentenceIds: [], finished: false };
      current.finished = !!finished;
      data[dayId] = current;
      write(data);
    }
  };
})();
