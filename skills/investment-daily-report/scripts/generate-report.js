#!/usr/bin/env node

/**
 * Investment Daily Report Generator
 * 投资日报生成器 - 纯 Node.js 实现
 * 
 * @description 自动收集A股、美股、币圈新闻并生成简报
 * @author niko 🦞
 */

import { writeFileSync, mkdirSync } from 'fs';
import { execSync } from 'child_process';
import path from 'path';

// ==================== 工具函数 ====================

/**
 * 延迟函数
 * @param {number} ms - 延迟毫秒数
 * @returns {Promise<void>}
 */
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// ==================== 配置区 ====================

const CONFIG = {
  // API Key
  tavilyApiKey: process.env.TAVILY_API_KEY || '',
  
  // 消息推送配置
  channel: 'feishu',
  targetUser: 'ou_bbfc027431c61a8ba421c54c7bb0f5c4',
  
  // 搜索配置
  searchResultsPerMarket: 8,
  deepSearch: false,
  
  // 内容比例
  ratios: {
    aShare: 70,
    usStock: 20,
    crypto: 10
  },
  
  // A股搜索关键词 (70%)
  aShareKeywords: [
    'A股 今日要闻',
    '中国股市 政策',
    '沪深300 行情',
    '北上资金 流向',
    'A股 板块分析',
    '证监会 最新消息'
  ],
  
  // 美股搜索关键词 (20%)
  usStockKeywords: [
    'US stock market today',
    'S&P500 Dow Jones Nasdaq',
    'Fed interest rates',
    'US stocks earnings',
    'Wall Street news'
  ],
  
  // 币圈搜索关键词 (10%)
  cryptoKeywords: [
    'Bitcoin Ethereum crypto news',
    'crypto market today',
    'futures commodities oil gold'
  ],
  
  // 输出路径
  reportDir: '/tmp/investment-reports',
  marketDataDir: '/root/.openclaw/workspace/memory/investment'
};

// ==================== Tavily 搜索函数 ====================

/**
 * 调用 Tavily API 搜索新闻
 * @param {string} query - 搜索关键词
 * @param {string} market - 市场类型（用于日志）
 * @returns {Promise<Array>} 搜索结果数组
 */
async function searchNews(query, market) {
  if (!CONFIG.tavilyApiKey) {
    console.error(`❌ Tavily API Key not set!`);
    return [];
  }
  
  console.log(`🔍 Searching: ${query} (${market})`);
  
  try {
    const response = await fetch('https://api.tavily.com/search', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        api_key: CONFIG.tavilyApiKey,
        query: query,
        search_depth: CONFIG.deepSearch ? 'advanced' : 'basic',
        topic: 'news',
        max_results: CONFIG.searchResultsPerMarket,
        include_answer: true,
        include_raw_content: false,
        include_images: false,
        exclude_domains: [],
        include_domains: [],
        time_range: 'day'
      })
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    return data.results || [];
    
  } catch (error) {
    console.error(`❌ Search failed for "${query}":`, error.message);
    return [];
  }
}

// ==================== 报告生成函数 ====================

/**
 * 生成市场板块内容
 * @param {string} sectionName - 板块名称
 * @param {string} sectionEmoji - 板块Emoji
 * @param {number} ratio - 占比
 * @param {Array<string>} keywords - 搜索关键词数组
 * @returns {Promise<string>} Markdown 格式的板块内容
 */
async function generateSection(sectionName, sectionEmoji, ratio, keywords) {
  let sectionContent = `## ${sectionEmoji} ${sectionName} (${ratio}%)\n\n`;
  
  let resultCount = 0;
  const allResults = [];
  
  // 收集所有搜索结果
  for (const keyword of keywords) {
    if (resultCount >= 3) break; // 每个板块最多3组结果
    
    const results = await searchNews(keyword, sectionName);
    
    if (results.length > 0) {
      allResults.push(...results.slice(0, 2)); // 每个关键词取前2条
      resultCount++;
    }
    
    // 添加延迟避免触发 API rate limit
    await sleep(2000); // 等待 2 秒
  }
  
  // 去重（按URL）
  const uniqueResults = [];
  const seenUrls = new Set();
  
  for (const result of allResults) {
    if (!seenUrls.has(result.url)) {
      uniqueResults.push(result);
      seenUrls.add(result.url);
    }
  }
  
  // 生成内容（最多6条）
  if (uniqueResults.length > 0) {
    const topResults = uniqueResults.slice(0, 6);
    
    for (const result of topResults) {
      sectionContent += `### ${result.title}\n`;
      sectionContent += `*Source: ${result.source}*\n\n`;
      
      if (result.content) {
        const content = result.content.length > 300 
          ? result.content.substring(0, 300) + '...'
          : result.content;
        sectionContent += `${content}\n\n`;
      }
      
      sectionContent += `🔗 [Read more](${result.url})\n\n`;
    }
  } else {
    sectionContent += 'ℹ️  暂无最新资讯\n\n';
  }
  
  sectionContent += '---\n\n';
  return sectionContent;
}

/**
 * 生成完整报告
 * @returns {Promise<string>} 完整报告的 Markdown 内容
 */
async function generateReport() {
  const now = new Date();
  const chinaTime = new Intl.DateTimeFormat('zh-CN', {
    timeZone: 'Asia/Shanghai',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  }).format(now);
  
  let report = `# 📊 每日投资简报\n\n`;
  report += `*Generated on ${chinaTime} China Standard Time*\n\n`;
  report += `---\n\n`;
  
  // A股部分 (70%)
  console.log('\n📊 Generating A-share section...');
  report += await generateSection('A股要闻', '🇨🇳', CONFIG.ratios.aShare, CONFIG.aShareKeywords);
  await sleep(3000); // 板块间延迟 3 秒
  
  // 美股部分 (20%)
  console.log('\n📊 Generating US stock section...');
  report += await generateSection('美股动态', '🇺🇸', CONFIG.ratios.usStock, CONFIG.usStockKeywords);
  await sleep(3000); // 板块间延迟 3 秒
  
  // 币圈部分 (10%)
  console.log('\n📊 Generating crypto section...');
  report += await generateSection('数字资产与商品', '🪙', CONFIG.ratios.crypto, CONFIG.cryptoKeywords);
  
  // 核心要点
  report += `## 💡 核心要点\n\n`;
  report += `以上是今日各市场的重要资讯汇总，建议重点关注：\n\n`;
  report += `1. **A股市场政策动向及资金流向** - 关注政策变化对板块的影响\n`;
  report += `2. **美股宏观经济数据及企业业绩** - 密切关注美联储政策和龙头科技股财报\n`;
  report += `3. **数字资产市场趋势及商品期货波动** - 关注比特币等主流加密货币走势\n\n`;
  report += `---\n\n`;
  report += `*报告由 niko 🦞 自动生成 | 数据仅供参考，不构成投资建议*\n`;
  
  return report;
}

// ==================== 文件和推送函数 ====================

/**
 * 保存报告到文件
 * @param {string} content - 报告内容
 * @param {string} reportDir - 输出目录
 * @returns {string} 报告文件路径
 */
function saveReport(content, reportDir) {
  mkdirSync(reportDir, { recursive: true });
  
  const now = new Date();
  const dateStr = now.toISOString().slice(0, 10).replace(/-/g, ''); // YYYYMMDD
  const reportFile = path.join(reportDir, `daily_report_${dateStr}.md`);
  
  writeFileSync(reportFile, content, 'utf8');
  console.log(`✅ Report saved to: ${reportFile}`);
  
  return reportFile;
}

/**
 * 归档报告
 * @param {string} content - 报告内容
 */
function archiveReport(content) {
  mkdirSync(CONFIG.marketDataDir, { recursive: true });
  const archiveFile = path.join(CONFIG.marketDataDir, 'latest_report.md');
  writeFileSync(archiveFile, content, 'utf8');
  console.log(`💾 Report archived to: ${archiveFile}`);
}

/**
 * 通过飞书推送报告
 * @param {string} content - 报告内容
 */
function sendViaFeishu(content) {
  if (CONFIG.channel !== 'feishu' || !CONFIG.targetUser) {
    console.log('⚠️  Feishu configuration incomplete, skipping push');
    return;
  }
  
  console.log('📤 Sending report via Feishu...');
  
  try {
    // 将推送标记写入文件（实际环境中应调用 Feishu API）
    const today = new Date();
    const dateStr = today.toISOString().slice(0, 10).replace(/-/g, '');
    const sentMarker = `/tmp/investment-reports/feishu_sent_${dateStr}.flag`;
    
    writeFileSync(sentMarker, `Report would be sent to ${CONFIG.targetUser} at ${today.toISOString()}`, 'utf8');
    
    console.log('✅ Report delivery ready (Feishu integration pending full OpenClaw API)');
    
  } catch (error) {
    console.error(`❌ Failed to send via Feishu:`, error.message);
  }
}

// ==================== 主函数 ====================

/**
 * 主执行函数
 */
async function main() {
  console.log('📈 Starting daily investment report generation...\n');
  console.log('='.repeat(60));
  
  try {
    // 检查 API Key
    if (!CONFIG.tavilyApiKey) {
      throw new Error('TAVILY_API_KEY environment variable is not set!');
    }
    
    // 生成报告
    const reportContent = await generateReport();
    
    // 保存报告
    const reportFile = saveReport(reportContent, CONFIG.reportDir);
    
    // 归档报告
    archiveReport(reportContent);
    
    // 推送到飞书
    sendViaFeishu(reportContent);
    
    console.log('='.repeat(60));
    console.log('\n🎉 Daily investment report completed successfully!');
    console.log(`📄 Report file: ${reportFile}`);
    
  } catch (error) {
    console.error('\n❌ Report generation failed:', error.message);
    console.error(error.stack);
    process.exit(1);
  }
}

// 运行主函数
main();