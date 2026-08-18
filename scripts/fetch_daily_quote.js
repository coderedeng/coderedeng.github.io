/**
 * Hexo 插件：从 hitokoto.cn API 获取每日名言并设置到副标题
 * 使用 before_generate 钩子，在生成页面之前完成 API 调用和配置更新
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

// hitokoto.cn API 地址（支持多种类型）
const HITOKOTO_API_URL = 'https://v1.hitokoto.cn/?c=a&encode=json'; // a=动画类，可改为其他类型

function fetchHitokoto() {
  return new Promise((resolve, reject) => {
    https.get(HITOKOTO_API_URL, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          resolve(json.hitokoto + ' —— ' + json.from);
        } catch (e) {
          reject(e);
        }
      });
    }).on('error', reject);
  });
}

function updateSubtitle(quote, configPath) {
  let content = fs.readFileSync(configPath, 'utf8');
  
  // 替换 subtitle: "" 为 subtitle: "每日一言内容"
  const newContent = content.replace(/subtitle:\s*["']?([^"'#]*)["']?\s*(#.*)?$/, `subtitle: "${quote}"`);
  
  fs.writeFileSync(configPath, newContent, 'utf8');
}

// Hexo 插件标准写法：导出一个函数，接收 hexo 实例作为参数
module.exports = function(hexo) {
  const configPath = path.join(hexo.base_dir, '_config.yml');
  
  // 注册 before_generate 钩子（同步版本）
  hexo.extend.filter.register('before_generate', async function() {
    try {
      const quote = await fetchHitokoto();
      updateSubtitle(quote, configPath);
      console.log('[daily-quote] Subtitle updated to:', quote);
    } catch (err) {
      console.error('[daily-quote] Failed to fetch hitokoto:', err.message);
      // 如果获取失败，保留原有副标题不变（不修改 _config.yml）
    }
  });
};
