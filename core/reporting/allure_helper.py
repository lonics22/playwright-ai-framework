"""Allure 报告增强工具"""
import json
import base64
from typing import Any, Dict, List, Optional
import allure
from allure_commons.types import AttachmentType
from playwright.sync_api import Page


class AllureHelper:
    """Allure 报告增强工具类"""

    @staticmethod
    def attach_screenshot(page: Page, name: str = "截图"):
        """
        附加截图到报告

        Args:
            page: Playwright 页面实例
            name: 截图名称
        """
        screenshot = page.screenshot()
        allure.attach(
            screenshot,
            name=name,
            attachment_type=AttachmentType.PNG
        )

    @staticmethod
    def attach_screenshot_with_annotation(
        page: Page,
        annotation: str,
        highlight_selector: str = None
    ):
        """
        截图并附加标注

        Args:
            page: Playwright 页面实例
            annotation: 标注文本
            highlight_selector: 高亮元素选择器
        """
        # 如果有高亮选择器，尝试高亮元素
        if highlight_selector:
            try:
                page.evaluate(f"""
                    const element = document.querySelector('{highlight_selector}');
                    if (element) {{
                        element.style.border = '3px solid red';
                    }}
                """)
            except:
                pass

        screenshot = page.screenshot()
        allure.attach(
            screenshot,
            name=f"截图 - {annotation}",
            attachment_type=AttachmentType.PNG
        )

        # 移除高亮
        if highlight_selector:
            try:
                page.evaluate(f"""
                    const element = document.querySelector('{highlight_selector}');
                    if (element) {{
                        element.style.border = '';
                    }}
                """)
            except:
                pass

    @staticmethod
    def attach_page_source(page: Page, name: str = "页面源码"):
        """
        附加页面源码到报告

        Args:
            page: Playwright 页面实例
            name: 附件名称
        """
        html = page.content()
        allure.attach(
            html,
            name=name,
            attachment_type=AttachmentType.HTML
        )

    @staticmethod
    def attach_console_logs(logs: List[Dict], name: str = "浏览器日志"):
        """
        附加浏览器控制台日志

        Args:
            logs: 日志列表
            name: 附件名称
        """
        log_text = "\n".join(
            f"[{log.get('type', 'unknown')}] {log.get('text', '')}"
            for log in logs
        )
        allure.attach(
            log_text,
            name=name,
            attachment_type=AttachmentType.TEXT
        )

    @staticmethod
    def attach_network_logs(logs: List[Dict], name: str = "网络请求日志"):
        """
        附加网络请求日志

        Args:
            logs: 网络请求日志列表
            name: 附件名称
        """
        allure.attach(
            json.dumps(logs, indent=2, ensure_ascii=False),
            name=name,
            attachment_type=AttachmentType.JSON
        )

    @staticmethod
    def attach_ai_execution(task: str, result: Dict[str, Any]):
        """
        附加 AI 执行详情到报告

        Args:
            task: 任务描述
            result: 执行结果
        """
        allure.attach(
            json.dumps({
                "task": task,
                "success": result.get("success"),
                "steps": result.get("steps", []),
                "duration": result.get("duration"),
                "errors": result.get("errors", []),
            }, indent=2, ensure_ascii=False),
            name="AI 执行详情",
            attachment_type=AttachmentType.JSON
        )

    @staticmethod
    def attach_ai_thinking(thinking: str, name: str = "AI 思考过程"):
        """
        附加 AI 思考过程

        Args:
            thinking: 思考内容
            name: 附件名称
        """
        allure.attach(
            thinking,
            name=name,
            attachment_type=AttachmentType.TEXT
        )

    @staticmethod
    def attach_form_data(form_data: Dict[str, str], name: str = "表单数据"):
        """
        附加表单数据

        Args:
            form_data: 表单数据字典
            name: 附件名称
        """
        allure.attach(
            json.dumps(form_data, indent=2, ensure_ascii=False),
            name=name,
            attachment_type=AttachmentType.JSON
        )

    @staticmethod
    def attach_test_data(data: Any, name: str = "测试数据"):
        """
        附加测试数据

        Args:
            data: 测试数据
            name: 附件名称
        """
        if isinstance(data, (dict, list)):
            content = json.dumps(data, indent=2, ensure_ascii=False)
            attach_type = AttachmentType.JSON
        else:
            content = str(data)
            attach_type = AttachmentType.TEXT

        allure.attach(content, name=name, attachment_type=attach_type)

    @staticmethod
    def step(title: str):
        """
        创建步骤装饰器

        Args:
            title: 步骤标题

        Returns:
            allure.step 装饰器
        """
        return allure.step(title)

    @staticmethod
    def feature(name: str):
        """
        设置功能/模块名称

        Args:
            name: 功能名称
        """
        return allure.feature(name)

    @staticmethod
    def story(name: str):
        """
        设置故事/场景名称

        Args:
            name: 故事名称
        """
        return allure.story(name)

    @staticmethod
    def title(name: str):
        """
        设置测试标题

        Args:
            name: 标题
        """
        return allure.title(name)

    @staticmethod
    def description(text: str):
        """
        设置测试描述

        Args:
            text: 描述文本
        """
        return allure.description(text)

    @staticmethod
    def severity(level: str):
        """
        设置严重级别

        Args:
            level: 严重级别 (blocker, critical, normal, minor, trivial)
        """
        return allure.severity(getattr(allure.severity_level, level.upper(), allure.severity_level.NORMAL))

    @staticmethod
    def link(url: str, name: str = None, link_type: str = "link"):
        """
        添加链接

        Args:
            url: URL
            name: 链接名称
            link_type: 链接类型
        """
        return allure.link(url, name=name, link_type=link_type)

    @staticmethod
    def issue(url: str, name: str = None):
        """
        添加 Issue 链接

        Args:
            url: Issue URL
            name: Issue 名称
        """
        return allure.issue(url, name=name)

    @staticmethod
    def testcase(url: str, name: str = None):
        """
        添加测试用例链接

        Args:
            url: 测试用例 URL
            name: 测试用例名称
        """
        return allure.testcase(url, name=name)


    @staticmethod
    def step_context(title: str):
        """
        创建步骤上下文管理器

        Args:
            title: 步骤标题

        Returns:
            AllureStepContext 上下文管理器
        """
        return AllureStepContext(title)


class AllureStepContext:
    """Allure 步骤上下文管理器"""

    def __init__(self, title: str):
        self.title = title
        self.step = None

    def __enter__(self):
        self.step = allure.step(self.title)
        self.step.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.step.__exit__(exc_type, exc_val, exc_tb)


# 快捷函数
def attach_screenshot(page: Page, name: str = "截图"):
    """快捷函数：附加截图"""
    return AllureHelper.attach_screenshot(page, name)


def attach_ai_execution(task: str, result: Dict[str, Any]):
    """快捷函数：附加 AI 执行详情"""
    return AllureHelper.attach_ai_execution(task, result)


def step(title: str):
    """快捷函数：创建步骤"""
    return AllureHelper.step(title)
