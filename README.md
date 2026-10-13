# 深圳岸钓踏勘

深圳岸线图集、出行与鱼情、海堤与港堤，以及宝安河口、深圳湾、深圳出发、石岩水库周边和黄脚立生物学与岸钓专题。

正式站点：https://shenzhen-fishing-atlas.pages.dev/

网页、卫星影像、来源记录及可下载表格位于 `outputs/coastline-survey/`。网站首页为岸线图集，专题从“专题索引”进入。各报告保留自己的调查日期和证据范围。

## 发布

`main` 分支更新网页、影像或部署配置后，GitHub Actions 检查本地文件链接与锚点，再通过 Wrangler Direct Upload 发布到 Cloudflare Pages。也可在 Actions 中手动运行 `Deploy to Cloudflare Pages`。

仓库使用两个 Actions secrets：`CLOUDFLARE_API_TOKEN`、`CLOUDFLARE_ACCOUNT_ID`。令牌需有对应账户的 Cloudflare Pages 编辑权限，不写入仓库文件。

Cloudflare Pages 项目名为 `shenzhen-fishing-atlas`，生产分支为 `main`。项目采用 Direct Upload，部署由 GitHub Actions 负责。

## 本地检查

```sh
python3 scripts/prepare_pages.py
```

部署目录 `.pages-dist/` 由检查脚本生成，不纳入 Git。研究中间文件和离线压缩包不发布到仓库。

报告中的影像与外部资料按文件内来源说明使用；它们不因收录于仓库而获得统一的开源授权。
