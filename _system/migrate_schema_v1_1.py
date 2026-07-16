#!/usr/bin/env python3
"""Migrate Progressive-KG notes and MOCs from Schema 1.0 to 1.1.

The command is dry-run by default. Use --apply to write changes.
It is intentionally deterministic and safe to run more than once.
"""

from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path
from typing import Any

import yaml


TODAY = date.today().isoformat()
CONTENT_ROOTS = {"Cognition", "Skill", "Language", "Meta", "Horizon"}
SKIP_NAMES = {"_moc.md"}

ALIASES: dict[str, list[str]] = {
    "Log-Sum-Exp": ["LSE", "logsumexp"],
    "Softmax": ["Softmax Function", "指数归一化"],
    "AGI实现路径-人类智能融合": ["AGI 人类智能融合路径"],
    "RRF(Reciprocal Rank Fusion)": ["RRF", "Reciprocal Rank Fusion", "倒数排位融合"],
    "主成分分析(PCA)": ["PCA", "Principal Component Analysis"],
    "偏微分方程": ["PDE", "Partial Differential Equation"],
    "内积": ["Inner Product", "点积", "Dot Product"],
    "均方误差": ["MSE", "Mean Squared Error"],
    "外积": ["Outer Product"],
    "奇异值": ["Singular Value"],
    "帕累托(Pareto)": ["Pareto", "帕累托"],
    "幂等性(Idempotence)": ["Idempotence", "幂等性"],
    "自指": ["Self-reference", "自指性"],
    "MoE架构": ["MoE", "Mixture of Experts", "混合专家模型"],
    "RoPE": ["Rotary Position Embedding", "旋转位置编码"],
    "Transformer架构": ["Transformer"],
    "flash-attention": ["FlashAttention", "Flash-Attention"],
    "kv-cache": ["KV-Cache", "KV缓存"],
    "位置编码": ["Positional Encoding"],
    "卷积神经网络": ["CNN", "Convolutional Neural Network"],
    "反向传播": ["Backpropagation", "BP"],
    "在线学习": ["Online Learning"],
    "归一化层": ["Normalization Layer"],
    "循环神经网络": ["RNN", "Recurrent Neural Network"],
    "感受野": ["Receptive Field"],
    "扩散模型": ["Diffusion Model"],
    "损失函数": ["Loss Function"],
    "梯度消失与梯度爆炸": ["Vanishing Gradient", "Exploding Gradient"],
    "正则化": ["Regularization"],
    "残差连接": ["Residual Connection", "Skip Connection"],
    "注意力机制": ["Attention Mechanism", "Attention"],
    "激活函数": ["Activation Function"],
    "联邦学习": ["Federated Learning"],
    "词嵌入": ["Word Embedding"],
    "Muon优化器": ["Muon", "Muon Optimizer"],
    "分布式训练": ["Distributed Training"],
    "动量": ["Momentum"],
    "参数高效微调": ["PEFT", "Parameter-Efficient Fine-Tuning"],
    "学习率调度": ["Learning Rate Scheduling"],
    "数据增强": ["Data Augmentation"],
    "梯度下降优化": ["Gradient Descent", "优化器"],
    "模型量化": ["Model Quantization"],
    "混合精度训练": ["Mixed Precision Training"],
    "知识蒸馏": ["Knowledge Distillation"],
    "训练调试": ["Training Debugging"],
    "超参数调优": ["Hyperparameter Tuning"],
    "类比导航学习法": ["类比学习法"],
    "交叉熵": ["Cross-Entropy", "Cross Entropy Loss"],
    "幂变换": ["Power Transform", "Power Transformation"],
}

TAGS: dict[str, list[str]] = {
    "Log-Sum-Exp": ["数值稳定性", "概率计算", "凸分析"],
    "Softmax": ["注意力机制", "概率归一化", "多分类", "Transformer"],
    "AGI实现路径-人类智能融合": ["AGI", "人机协作", "研究假设"],
    "RRF(Reciprocal Rank Fusion)": ["信息检索", "排序融合"],
    "主成分分析(PCA)": ["线性代数", "降维", "统计学习"],
    "内积": ["线性代数", "向量"],
    "均方误差": ["统计学", "回归", "损失函数"],
    "外积": ["线性代数", "向量"],
    "奇异值": ["线性代数", "矩阵分解"],
    "帕累托(Pareto)": ["多目标优化", "概率分布", "决策"],
    "幂等性(Idempotence)": ["数学性质", "分布式系统", "HTTP"],
    "自指": ["逻辑", "计算机科学", "认知科学"],
    "MoE架构": ["模型架构", "稀疏模型", "LLM"],
    "RoPE": ["位置编码", "注意力机制", "LLM"],
    "Transformer架构": ["模型架构", "注意力机制", "LLM"],
    "flash-attention": ["注意力机制", "GPU", "推理优化"],
    "kv-cache": ["注意力机制", "LLM推理", "缓存"],
    "位置编码": ["Transformer", "序列建模"],
    "卷积神经网络": ["CNN", "计算机视觉", "模型架构"],
    "反向传播": ["自动微分", "神经网络训练"],
    "在线学习": ["机器学习范式", "数据流"],
    "归一化层": ["神经网络训练", "归一化"],
    "循环神经网络": ["RNN", "序列建模"],
    "感受野": ["CNN", "计算机视觉"],
    "扩散模型": ["生成模型", "概率模型"],
    "损失函数": ["优化", "模型训练"],
    "梯度消失与梯度爆炸": ["优化", "深度网络"],
    "正则化": ["泛化", "模型训练"],
    "残差连接": ["模型架构", "深度网络"],
    "注意力机制": ["Attention", "序列建模", "Transformer"],
    "激活函数": ["神经网络", "非线性"],
    "联邦学习": ["分布式学习", "隐私"],
    "词嵌入": ["NLP", "表示学习"],
    "Muon优化器": ["优化器", "矩阵正交化"],
    "分布式训练": ["训练工程", "并行计算"],
    "动量": ["优化器", "梯度下降"],
    "参数高效微调": ["微调", "LLM", "训练工程"],
    "学习率调度": ["优化", "训练工程"],
    "数据增强": ["泛化", "训练工程"],
    "梯度下降优化": ["优化器", "神经网络训练"],
    "模型量化": ["模型压缩", "推理优化"],
    "混合精度训练": ["训练工程", "数值精度", "GPU"],
    "知识蒸馏": ["模型压缩", "迁移学习"],
    "训练调试": ["训练工程", "故障诊断"],
    "超参数调优": ["训练工程", "优化"],
    "类比导航学习法": ["学习方法", "知识管理"],
    "交叉熵": ["信息论", "分类", "损失函数", "概率模型"],
    "幂变换": ["Box-Cox", "Yeo-Johnson", "数据预处理", "分布校正"],
}

PROCEDURES = {
    "分布式训练",
    "参数高效微调",
    "学习率调度",
    "数据增强",
    "模型量化",
    "混合精度训练",
    "知识蒸馏",
    "训练调试",
    "超参数调优",
}

EXTRA_RELATIONS: dict[str, list[tuple[str, str, str]]] = {
    "kv-cache": [
        ("前置", "注意力机制", "缓存的是注意力层已经计算出的 K/V"),
        ("对比", "flash-attention", "两者分别优化重复计算与内存 IO"),
        ("应用", "Transformer架构", "用于自回归 Transformer 解码"),
    ],
    "在线学习": [
        ("对比", "联邦学习", "在线学习按数据到达顺序更新，联邦学习按客户端聚合"),
        ("相关", "梯度下降优化", "SGD 是常见在线更新方法"),
    ],
    "联邦学习": [
        ("对比", "在线学习", "二者解决的数据组织问题不同"),
        ("应用", "分布式训练", "都涉及多节点协调，但信任边界不同"),
    ],
}

LINK_TARGETS: dict[str, str | None] = {
    "../Model/Transformer架构": "Cognition/Model/Transformer架构",
    "KV-Cache": "kv-cache",
    "Flash-Attention": "flash-attention",
    "标准化(Standardization)": "标准化",
    "梯度下降": "梯度下降优化#基础梯度下降",
    "Adam": "梯度下降优化#自适应优化器",
    "AdamW": "梯度下降优化#自适应优化器",
    "SGD-Momentum": "动量",
    "优化器": "梯度下降优化",
    "Newton-Schulz迭代": "Muon优化器#Newton-Schulz 迭代",
    "正交矩阵": "正交#正交矩阵",
    "谱范数": "奇异值",
    "RMSE": "均方误差#与相关指标对比",
    "MAE": "均方误差#与相关指标对比",
    "Speech Act Theory": None,
    "意图分类框架": None,
    "用户反馈驱动学习": None,
    "语义聚类": None,
    "BM25": None,
    "密集检索(Dense Retrieval)": None,
    "RAG(检索增强生成)": None,
    "交叉编码器(Cross-encoder)": None,
    "排序学习(Learning to Rank)": None,
    "余弦相似度": None,
    "矩阵乘法": None,
    "偏差-方差分解": None,
    "过拟合": None,
    "LinUCB": None,
    "协方差矩阵": None,
    "多任务学习": None,
    "特征工程": None,
    "奇异值分解": "奇异值",
    "特征值分解": None,
    "quine": None,
    "元认知": None,
    "哥德尔不完备定理": None,
    "怪圈": None,
    "意识": None,
    "递归": None,
    "深度学习学习路径": None,
    "深度学习知识图谱": None,
    "Moonlight": None,
    "Shampoo": None,
    "鞍点": None,
}

DOMAIN_NAV = {
    "Cognition": [
        ("Cognition/Math/_moc", "📐 数学"),
        ("Cognition/Model/_moc", "🤖 模型"),
        ("Cognition/work/_moc", "💼 工作"),
        ("Cognition/life/_moc", "🌱 生活"),
    ],
    "Skill": [
        ("Skill/dl-training/_moc", "🧪 深度学习训练"),
        ("Skill/coding/_moc", "💻 编程"),
        ("Skill/Research/_moc", "🔬 研究"),
        ("Skill/writing/_moc", "✍️ 写作"),
        ("Skill/management/_moc", "📋 管理"),
    ],
    "Language": [("Language/academic-english/_moc", "📚 学术英语")],
    "Meta": [
        ("Meta/methodology/_moc", "🧭 方法论"),
        ("Meta/reviews/_moc", "🔁 复盘与审阅"),
    ],
    "Horizon": [
        ("Horizon/questions/_moc", "❓ 待探索问题"),
        ("Horizon/experiments/_moc", "🧫 实验记录"),
    ],
}


def split_frontmatter(content: str) -> tuple[dict[str, Any], str]:
    match = re.match(r"\A---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|\Z)", content, re.DOTALL)
    if not match:
        raise ValueError("missing or invalid frontmatter")
    fm = yaml.safe_load(match.group(1)) or {}
    if not isinstance(fm, dict):
        raise ValueError("frontmatter must be a mapping")
    return fm, content[match.end() :]


def iso(value: Any, default: str = "") -> str:
    if value in (None, ""):
        return default
    return value.isoformat() if hasattr(value, "isoformat") else str(value)


def dump_frontmatter(fm: dict[str, Any]) -> str:
    rendered = yaml.safe_dump(
        fm,
        allow_unicode=True,
        sort_keys=False,
        default_flow_style=False,
        width=1000,
    ).rstrip()
    rendered = rendered.replace("verified: null", "verified:")
    rendered = rendered.replace("review_due: null", "review_due:")
    return f"---\n{rendered}\n---\n\n"


def quote_text(summary: str) -> str:
    return summary if summary.endswith(("。", "！", "？", ".", "!", "?")) else summary + "。"


def ensure_l1(body: str, summary: str) -> str:
    first_h2 = re.search(r"^##\s+", body, re.MULTILINE)
    prefix_end = first_h2.start() if first_h2 else len(body)
    prefix = body[:prefix_end]
    definition = f"> {quote_text(summary)}"
    if re.search(r"^>\s+.+$", prefix, re.MULTILINE):
        return re.sub(r"^>\s+.+$", definition, body, count=1, flags=re.MULTILINE)

    h1 = re.search(r"^#\s+.+$", body, re.MULTILINE)
    if not h1:
        return body
    return body[: h1.end()] + f"\n\n{definition}" + body[h1.end() :]


def extract_legacy_related(values: Any) -> list[str]:
    if not isinstance(values, list):
        return []
    targets = []
    for value in values:
        raw = str(value).strip()
        match = re.fullmatch(r"\[\[([^\]]+)\]\]", raw)
        targets.append(match.group(1) if match else raw)
    return targets


def ensure_relation_section(body: str, stem: str, legacy_targets: list[str]) -> str:
    body = re.sub(r"^##\s+(?:相关概念|关联概念|相关资源)\s*$", "## 关系网络", body, flags=re.MULTILINE)
    relation = re.search(r"^## 关系网络\s*$", body, re.MULTILINE)
    relation_text = ""
    if relation:
        next_h2 = re.search(r"^##\s+", body[relation.end() :], re.MULTILINE)
        relation_end = relation.end() + (next_h2.start() if next_h2 else len(body[relation.end() :]))
        relation_text = body[relation.end() : relation_end]
    current_targets = {
        raw.split("|", 1)[0].split("#", 1)[0]
        for raw in re.findall(r"\[\[([^\]]+)\]\]", relation_text)
    }
    additions = []
    for target in legacy_targets:
        base = target.split("|", 1)[0].split("#", 1)[0]
        if base and base not in current_targets:
            additions.append(f"- 相关：[[{target}]] — 来自迁移前的关联元数据")
            current_targets.add(base)
    for label, target, explanation in EXTRA_RELATIONS.get(stem, []):
        if target not in current_targets:
            additions.append(f"- {label}：[[{target}]] — {explanation}")
            current_targets.add(target)

    if relation:
        if additions:
            body = body.replace("- 待补：至少建立两个指向现有概念的关系。", "")
            relation = re.search(r"^## 关系网络\s*$", body, re.MULTILINE)
            assert relation is not None
            next_h2 = re.search(r"^##\s+", body[relation.end() :], re.MULTILINE)
            insert_at = relation.end() + (next_h2.start() if next_h2 else len(body[relation.end() :]))
            text = "\n" + "\n".join(additions) + "\n"
            return body[:insert_at].rstrip() + text + body[insert_at:].lstrip("\n")
        return body

    block = "\n\n---\n\n## 关系网络\n\n"
    block += "\n".join(additions) if additions else "- 待补：至少建立两个指向现有概念的关系。"
    return body.rstrip() + block + "\n"


def repair_links(body: str) -> str:
    def replace(match: re.Match[str]) -> str:
        raw = match.group(1)
        target_and_heading, separator, label = raw.partition("|")
        target, hash_sep, heading = target_and_heading.partition("#")
        if target not in LINK_TARGETS:
            return match.group(0)
        replacement = LINK_TARGETS[target]
        display = label if separator else target.split("/")[-1]
        if replacement is None:
            return f"{display}（待建）"
        if hash_sep and "#" not in replacement:
            replacement = f"{replacement}#{heading}"
        return f"[[{replacement}|{display}]]"

    body = re.sub(r"\[\[([^\]]+)\]\]", replace, body)
    body = body.replace(
        "[深度学习核心概念：类比视角](../../human_ai_knowledge/deep-learning-metaphors.md)",
        "深度学习核心概念：类比视角（待补来源）",
    )
    return body


def migrate_note(path: Path) -> str:
    old_fm, body = split_frontmatter(path.read_text(encoding="utf-8"))
    stem = path.stem
    summary = str(old_fm.get("summary") or "").strip()
    legacy_related = extract_legacy_related(old_fm.get("related"))
    old_tags = old_fm.get("tags") if isinstance(old_fm.get("tags"), list) else []
    sources = old_fm.get("sources") if isinstance(old_fm.get("sources"), list) else []
    legacy_status = str(old_fm.get("status") or "").strip().lower()
    default_maturity = "seed" if legacy_status == "placeholder" else "growing"

    inferred_type = "hypothesis" if stem == "AGI实现路径-人类智能融合" else "procedure" if stem in PROCEDURES else "concept"
    note_type = str(old_fm.get("type") or inferred_type)
    fm = {
        "schema_version": "1.1",
        "title": str(old_fm.get("title") or stem),
        "aliases": old_fm.get("aliases") if isinstance(old_fm.get("aliases"), list) else ALIASES.get(stem, []),
        "summary": summary,
        "type": note_type,
        "maturity": str(old_fm.get("maturity") or default_maturity),
        "confidence": str(old_fm.get("confidence") or ("low" if note_type == "hypothesis" else "medium")),
        "tags": old_tags or TAGS.get(stem, []),
        "created": iso(old_fm.get("created"), TODAY),
        "updated": iso(old_fm.get("updated") or old_fm.get("last_verified"), TODAY),
        "verified": old_fm.get("verified"),
        "review_due": old_fm.get("review_due"),
        "sources": [iso(source) for source in sources],
    }

    body = re.sub(r"^## 概念\s*$", "## 核心概览", body, flags=re.MULTILINE)
    body = re.sub(r"^## 定义\s*$", "## 核心定义", body, flags=re.MULTILINE)
    body = ensure_l1(body, summary)
    body = ensure_relation_section(body, stem, legacy_related)
    body = repair_links(body)
    body = re.sub(r"\n{4,}", "\n\n\n", body).strip() + "\n"
    return dump_frontmatter(fm) + body


def moc_body(title: str, scope: str, domain_links: list[tuple[str, str]] | None) -> str:
    lines = [f"# {title}", ""]
    if domain_links:
        lines += ["## 子域导航", ""]
        lines += [f"- [[{target}|{label}]]" for target, label in domain_links]
        lines += ["", "## 全域概念", "", "```dataview"]
        lines += [
            'TABLE summary AS "定义", maturity AS "成熟度", updated AS "更新日期"',
            'FROM ""',
            'WHERE startswith(file.folder, this.scope) AND type != "moc"',
            "SORT title ASC",
            "```",
        ]
    else:
        lines += ["## 当前目录", "", "```dataview"]
        lines += [
            'TABLE summary AS "定义", maturity AS "成熟度", verified AS "已核验"',
            'FROM ""',
            'WHERE file.folder = this.scope AND type != "moc"',
            "SORT title ASC",
            "```",
        ]
    lines += [
        "",
        "## 待审阅",
        "",
        "```dataview",
        'TABLE summary AS "定义", maturity AS "成熟度", review_due AS "复核日期"',
        'FROM ""',
        'WHERE startswith(file.folder, this.scope) AND type != "moc" AND (maturity != "evergreen" OR confidence = "low" OR !verified OR !sources OR (review_due AND review_due <= date(today)))',
        "SORT review_due ASC",
        "```",
        "",
    ]
    return "\n".join(lines)


def migrate_moc(path: Path, vault: Path) -> str:
    old_fm, _ = split_frontmatter(path.read_text(encoding="utf-8"))
    rel = path.relative_to(vault)
    scope = rel.parent.as_posix()
    title = str(old_fm.get("title") or f"{path.parent.name}概念地图")
    fm = {"schema_version": "1.1", "title": title, "type": "moc", "scope": scope}
    return dump_frontmatter(fm) + moc_body(title, scope, DOMAIN_NAV.get(scope))


def candidates(vault: Path) -> list[Path]:
    paths = []
    for path in vault.rglob("*.md"):
        rel = path.relative_to(vault)
        if not rel.parts or rel.parts[0] not in CONTENT_ROOTS:
            continue
        paths.append(path)
    return sorted(paths)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("vault", nargs="?", type=Path, default=Path(__file__).parent.parent)
    parser.add_argument("--apply", action="store_true", help="write the migration instead of dry-run")
    args = parser.parse_args()

    vault = args.vault.resolve()
    changed: list[Path] = []
    errors: list[tuple[Path, str]] = []
    for path in candidates(vault):
        try:
            new_content = migrate_moc(path, vault) if path.name == "_moc.md" else migrate_note(path)
            old_content = path.read_text(encoding="utf-8")
            if new_content != old_content:
                changed.append(path.relative_to(vault))
                if args.apply:
                    path.write_text(new_content, encoding="utf-8")
        except Exception as exc:  # migration should report every problematic file
            errors.append((path.relative_to(vault), str(exc)))

    mode = "APPLY" if args.apply else "DRY-RUN"
    print(f"Schema 1.1 migration [{mode}]")
    print(f"  Changed: {len(changed)}")
    print(f"  Errors:  {len(errors)}")
    for path in changed:
        print(f"  {'updated' if args.apply else 'would update'}: {path.as_posix()}")
    for path, message in errors:
        print(f"  ERROR: {path.as_posix()}: {message}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
