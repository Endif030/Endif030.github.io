const Storage = {
  KEY: 'pilatesProgress',
  
  getAll() {
    try {
      const data = localStorage.getItem(this.KEY);
      return data ? JSON.parse(data) : {};
    } catch (e) {
      return {};
    }
  },
  
  saveAll(data) {
    try {
      localStorage.setItem(this.KEY, JSON.stringify(data));
      return true;
    } catch (e) {
      return false;
    }
  },
  
  get(id) {
    const data = this.getAll();
    return data[id] || { learned: false, learnedAt: null };
  },
  
  setLearned(id) {
    const data = this.getAll();
    data[id] = { learned: true, learnedAt: Date.now() };
    return this.saveAll(data);
  },
  
  unsetLearned(id) {
    const data = this.getAll();
    delete data[id];
    return this.saveAll(data);
  },
  
  toggleLearned(id) {
    const current = this.get(id);
    if (current.learned) {
      return this.unsetLearned(id);
    } else {
      return this.setLearned(id);
    }
  },
  
  getStats() {
    const data = this.getAll();
    const total = typeof WordRoots !== 'undefined' ? WordRoots.length : 30;
    const learned = Object.values(data).filter(item => item.learned).length;
    return {
      total,
      learned,
      percentage: total > 0 ? Math.round((learned / total) * 100) : 0
    };
  },
  
  getLearnedList() {
    const data = this.getAll();
    return Object.entries(data)
      .filter(([_, item]) => item.learned)
      .map(([id, item]) => ({ id: parseInt(id), ...item }));
  },
  
  clear() {
    try {
      localStorage.removeItem(this.KEY);
      return true;
    } catch (e) {
      return false;
    }
  }
};
