// 存储管理 - 攀岩学习工坊
const Storage = {
  KEY: 'rockClimbingProgress',
  
  // 获取所有进度数据
  getAll() {
    try {
      const data = localStorage.getItem(this.KEY);
      return data ? JSON.parse(data) : {};
    } catch (e) {
      console.error('Storage getAll error:', e);
      return {};
    }
  },
  
  // 保存所有进度数据
  saveAll(data) {
    try {
      localStorage.setItem(this.KEY, JSON.stringify(data));
      return true;
    } catch (e) {
      console.error('Storage saveAll error:', e);
      return false;
    }
  },
  
  // 获取单个项目的进度
  get(id) {
    const data = this.getAll();
    return data[id] || { learned: false, learnedAt: null };
  },
  
  // 设置单个项目为已学习
  setLearned(id) {
    const data = this.getAll();
    data[id] = { learned: true, learnedAt: Date.now() };
    return this.saveAll(data);
  },
  
  // 取消学习状态
  unsetLearned(id) {
    const data = this.getAll();
    delete data[id];
    return this.saveAll(data);
  },
  
  // 切换学习状态
  toggleLearned(id) {
    const current = this.get(id);
    if (current.learned) {
      return this.unsetLearned(id);
    } else {
      return this.setLearned(id);
    }
  },
  
  // 获取学习进度统计
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
  
  // 获取已学习列表
  getLearnedList() {
    const data = this.getAll();
    return Object.entries(data)
      .filter(([_, item]) => item.learned)
      .map(([id, item]) => ({ id: parseInt(id), ...item }));
  },
  
  // 清空所有进度
  clear() {
    try {
      localStorage.removeItem(this.KEY);
      return true;
    } catch (e) {
      console.error('Storage clear error:', e);
      return false;
    }
  }
};
