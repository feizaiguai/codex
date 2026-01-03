"""27-explainability-analyzer 引擎（精简可用版）"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Dict, List, Any, Tuple
import csv
import math


class ExplainMethod(Enum):
    SHAP = "shap"
    LIME = "lime"
    FEATURE_IMPORTANCE = "feature_importance"
    COUNTERFACTUAL = "counterfactual"


class BiasType(Enum):
    DEMOGRAPHIC_PARITY = "demographic_parity"


@dataclass
class FeatureImportance:
    name: str
    score: float


class ExplainabilityAnalyzer:
    def _to_float(self, value: str) -> float | None:
        try:
            return float(value)
        except Exception:
            return None

    def _pearson(self, xs: List[float], ys: List[float]) -> float:
        n = len(xs)
        if n == 0:
            return 0.0
        mean_x = sum(xs) / n
        mean_y = sum(ys) / n
        num = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
        den_x = math.sqrt(sum((x - mean_x) ** 2 for x in xs))
        den_y = math.sqrt(sum((y - mean_y) ** 2 for y in ys))
        if den_x == 0 or den_y == 0:
            return 0.0
        return num / (den_x * den_y)

    def analyze_csv(self, path: str, target: str, sensitive: str | None = None, top_k: int = 5) -> Dict[str, Any]:
        p = Path(path)
        rows = []
        with p.open("r", encoding="utf-8", errors="replace") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)

        if not rows:
            raise ValueError("CSV 无数据")

        numeric_cols: Dict[str, List[float]] = {}
        target_vals: List[float] = []
        for row in rows:
            tval = self._to_float(row.get(target, ""))
            if tval is not None:
                target_vals.append(tval)
            for k, v in row.items():
                if k == target or k == sensitive:
                    continue
                num = self._to_float(v)
                if num is None:
                    continue
                numeric_cols.setdefault(k, []).append(num)

        features: List[FeatureImportance] = []
        for name, values in numeric_cols.items():
            if len(values) != len(target_vals):
                continue
            score = abs(self._pearson(values, target_vals)) if target_vals else 0.0
            features.append(FeatureImportance(name=name, score=score))

        features.sort(key=lambda f: f.score, reverse=True)
        top_features = features[:top_k]

        bias_report: Dict[str, Any] = {}
        if sensitive:
            groups: Dict[str, List[float]] = {}
            for row in rows:
                key = row.get(sensitive, "UNKNOWN")
                val = self._to_float(row.get(target, ""))
                if val is None:
                    continue
                groups.setdefault(key, []).append(val)
            bias_report = {
                "sensitive": sensitive,
                "group_means": {k: (sum(v)/len(v)) for k, v in groups.items() if v},
            }

        return {
            "file": str(p),
            "target": target,
            "top_features": [f.__dict__ for f in top_features],
            "bias": bias_report,
        }

    def generate_report(self, analysis: Dict[str, Any]) -> str:
        lines = [
            f"# 可解释性分析报告 - {Path(analysis['file']).name}",
            "",
            f"目标列: {analysis['target']}",
            "",
            "## 特征重要性",
        ]
        if not analysis["top_features"]:
            lines.append("- 未检测到可用数值特征")
        else:
            for item in analysis["top_features"]:
                lines.append(f"- {item['name']}: {item['score']:.4f}")
        if analysis.get("bias"):
            lines.append("")
            lines.append("## 偏差检查")
            for k, v in analysis["bias"].get("group_means", {}).items():
                lines.append(f"- {k}: 平均值 {v:.4f}")
        return "\n".join(lines)


if __name__ == "__main__":
    print("27-explainability-analyzer engine ready")