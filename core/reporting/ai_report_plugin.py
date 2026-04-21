"""AI 测试洞察报告插件"""
import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class AIExecutionRecord:
    """AI 执行记录"""
    test_name: str
    task: str
    success: bool
    duration: float
    steps: List[str]
    errors: List[str]
    timestamp: str
    llm_provider: str
    model: str


@dataclass
class TestInsight:
    """测试洞察"""
    test_name: str
    status: str
    ai_suggestions: str
    failure_analysis: str
    optimization_tips: List[str]


class AIReportPlugin:
    """AI 测试洞察报告插件"""

    def __init__(self, output_dir: str = "reports/ai-insights"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.execution_records: List[AIExecutionRecord] = []
        self.test_insights: List[TestInsight] = []

    def record_execution(
        self,
        test_name: str,
        task: str,
        result: Any,
        llm_provider: str = "unknown",
        model: str = "unknown"
    ):
        """
        记录 AI 执行

        Args:
            test_name: 测试名称
            task: 任务描述
            result: 执行结果
            llm_provider: LLM 提供商
            model: 模型名称
        """
        record = AIExecutionRecord(
            test_name=test_name,
            task=task,
            success=getattr(result, "success", False),
            duration=getattr(result, "duration", 0),
            steps=getattr(result, "steps", []),
            errors=getattr(result, "errors", []),
            timestamp=datetime.now().isoformat(),
            llm_provider=llm_provider,
            model=model
        )
        self.execution_records.append(record)

    def add_insight(
        self,
        test_name: str,
        status: str,
        ai_suggestions: str = "",
        failure_analysis: str = "",
        optimization_tips: List[str] = None
    ):
        """
        添加测试洞察

        Args:
            test_name: 测试名称
            status: 测试状态
            ai_suggestions: AI 建议
            failure_analysis: 失败分析
            optimization_tips: 优化建议
        """
        insight = TestInsight(
            test_name=test_name,
            status=status,
            ai_suggestions=ai_suggestions,
            failure_analysis=failure_analysis,
            optimization_tips=optimization_tips or []
        )
        self.test_insights.append(insight)

    def generate_report(self) -> Dict[str, Any]:
        """
        生成 AI 洞察报告

        Returns:
            报告字典
        """
        total_tests = len(self.execution_records)
        successful_tests = sum(1 for r in self.execution_records if r.success)
        failed_tests = total_tests - successful_tests
        success_rate = (successful_tests / total_tests * 100) if total_tests > 0 else 0

        # 按 LLM 提供商统计
        provider_stats = {}
        for record in self.execution_records:
            provider = record.llm_provider
            if provider not in provider_stats:
                provider_stats[provider] = {"total": 0, "success": 0}
            provider_stats[provider]["total"] += 1
            if record.success:
                provider_stats[provider]["success"] += 1

        # 计算平均执行时间
        avg_duration = (
            sum(r.duration for r in self.execution_records) / total_tests
            if total_tests > 0 else 0
        )

        report = {
            "summary": {
                "generated_at": datetime.now().isoformat(),
                "total_tests": total_tests,
                "successful": successful_tests,
                "failed": failed_tests,
                "success_rate": f"{success_rate:.2f}%",
                "avg_duration_seconds": round(avg_duration, 2),
            },
            "provider_stats": {
                provider: {
                    "total": stats["total"],
                    "success": stats["success"],
                    "rate": f"{(stats['success'] / stats['total'] * 100):.2f}%"
                }
                for provider, stats in provider_stats.items()
            },
            "execution_records": [asdict(r) for r in self.execution_records],
            "insights": [asdict(i) for i in self.test_insights],
        }

        return report

    def save_report(self, filename: str = "ai-insights-report.json"):
        """
        保存报告到文件

        Args:
            filename: 文件名
        """
        report = self.generate_report()
        filepath = self.output_dir / filename

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        return filepath

    def generate_html_report(self, filename: str = "ai-insights-report.html") -> Path:
        """
        生成 HTML 格式报告

        Args:
            filename: 文件名

        Returns:
            报告文件路径
        """
        report = self.generate_report()

        html_content = self._build_html(report)

        filepath = self.output_dir / filename
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html_content)

        return filepath

    def _build_html(self, report: Dict) -> str:
        """
        构建 HTML 报告内容

        Args:
            report: 报告数据

        Returns:
            HTML 字符串
        """
        summary = report["summary"]

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>AI 测试洞察报告</title>
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    margin: 0;
                    padding: 20px;
                    background-color: #f5f5f5;
                }}
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                    background: white;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    padding: 30px;
                }}
                h1 {{
                    color: #333;
                    border-bottom: 2px solid #4CAF50;
                    padding-bottom: 10px;
                }}
                h2 {{
                    color: #555;
                    margin-top: 30px;
                }}
                .summary-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 20px;
                    margin: 20px 0;
                }}
                .summary-card {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 20px;
                    border-radius: 8px;
                    text-align: center;
                }}
                .summary-card.success {{
                    background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
                }}
                .summary-card.error {{
                    background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
                }}
                .summary-card h3 {{
                    margin: 0 0 10px 0;
                    font-size: 14px;
                    opacity: 0.9;
                }}
                .summary-card .value {{
                    font-size: 32px;
                    font-weight: bold;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                }}
                th, td {{
                    padding: 12px;
                    text-align: left;
                    border-bottom: 1px solid #ddd;
                }}
                th {{
                    background-color: #f8f9fa;
                    font-weight: 600;
                    color: #555;
                }}
                tr:hover {{
                    background-color: #f5f5f5;
                }}
                .status-success {{
                    color: #28a745;
                    font-weight: bold;
                }}
                .status-failed {{
                    color: #dc3545;
                    font-weight: bold;
                }}
                .timestamp {{
                    color: #999;
                    font-size: 12px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>AI 测试洞察报告</h1>
                <p class="timestamp">生成时间: {summary['generated_at']}</p>

                <h2>执行概览</h2>
                <div class="summary-grid">
                    <div class="summary-card">
                        <h3>总测试数</h3>
                        <div class="value">{summary['total_tests']}</div>
                    </div>
                    <div class="summary-card success">
                        <h3>成功</h3>
                        <div class="value">{summary['successful']}</div>
                    </div>
                    <div class="summary-card error">
                        <h3>失败</h3>
                        <div class="value">{summary['failed']}</div>
                    </div>
                    <div class="summary-card">
                        <h3>成功率</h3>
                        <div class="value">{summary['success_rate']}</div>
                    </div>
                </div>

                <h2>LLM 提供商统计</h2>
                <table>
                    <thead>
                        <tr>
                            <th>提供商</th>
                            <th>总测试数</th>
                            <th>成功数</th>
                            <th>成功率</th>
                        </tr>
                    </thead>
                    <tbody>
        """

        for provider, stats in report["provider_stats"].items():
            html += f"""
                        <tr>
                            <td>{provider}</td>
                            <td>{stats['total']}</td>
                            <td>{stats['success']}</td>
                            <td>{stats['rate']}</td>
                        </tr>
            """

        html += """
                    </tbody>
                </table>

                <h2>执行记录</h2>
                <table>
                    <thead>
                        <tr>
                            <th>测试名称</th>
                            <th>任务</th>
                            <th>状态</th>
                            <th>耗时</th>
                            <th>提供商</th>
                        </tr>
                    </thead>
                    <tbody>
        """

        for record in report["execution_records"]:
            status_class = "status-success" if record["success"] else "status-failed"
            status_text = "成功" if record["success"] else "失败"
            html += f"""
                        <tr>
                            <td>{record['test_name']}</td>
                            <td>{record['task'][:50]}...</td>
                            <td class="{status_class}">{status_text}</td>
                            <td>{record['duration']:.2f}s</td>
                            <td>{record['llm_provider']}</td>
                        </tr>
            """

        html += """
                    </tbody>
                </table>
            </div>
        </body>
        </html>
        """

        return html

    def clear(self):
        """清除所有记录"""
        self.execution_records.clear()
        self.test_insights.clear()


# 全局插件实例
_global_plugin: Optional[AIReportPlugin] = None


def get_plugin(output_dir: str = "reports/ai-insights") -> AIReportPlugin:
    """
    获取全局插件实例

    Args:
        output_dir: 输出目录

    Returns:
        AIReportPlugin 实例
    """
    global _global_plugin
    if _global_plugin is None:
        _global_plugin = AIReportPlugin(output_dir)
    return _global_plugin
