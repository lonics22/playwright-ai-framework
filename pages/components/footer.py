"""页面底部组件"""
from playwright.sync_api import Page
from core.elements.smart_locator import SmartLocator


class Footer:
    """页面底部组件"""

    # 选择器定义
    SELECTORS = {
        "footer_container": "footer, .footer, [data-testid='footer']",
        "copyright": "footer .copyright, .footer-copyright, [data-testid='copyright']",
        "social_links": "footer .social-links a, .social-media a, [data-testid='social-link']",
        "contact_link": "footer a[href*='contact'], .contact-link, [data-testid='contact-link']",
        "about_link": "footer a[href*='about'], .about-link, [data-testid='about-link']",
        "help_link": "footer a[href*='help'], .help-link, [data-testid='help-link']",
        "terms_link": "footer a[href*='terms'], .terms-link, [data-testid='terms-link']",
        "privacy_link": "footer a[href*='privacy'], .privacy-link, [data-testid='privacy-link']",
        "newsletter_input": "footer input[type='email'], .newsletter-input, [data-testid='newsletter-input']",
        "newsletter_submit": "footer .newsletter-submit, [data-testid='newsletter-submit']",
    }

    def __init__(self, page: Page):
        self.page = page
        self.locator = SmartLocator(page)

    def scroll_to_footer(self):
        """滚动到页面底部"""
        self.locator.find(self.SELECTORS["footer_container"]).scroll_into_view_if_needed()

    def get_copyright_text(self) -> str:
        """
        获取版权信息文本

        Returns:
            版权文本
        """
        return self.locator.find(self.SELECTORS["copyright"]).text_content() or ""

    def click_contact(self):
        """点击联系我们链接"""
        self.locator.find(self.SELECTORS["contact_link"]).click()

    def click_about(self):
        """点击关于我们链接"""
        self.locator.find(self.SELECTORS["about_link"]).click()

    def click_help(self):
        """点击帮助链接"""
        self.locator.find(self.SELECTORS["help_link"]).click()

    def click_terms(self):
        """点击服务条款链接"""
        self.locator.find(self.SELECTORS["terms_link"]).click()

    def click_privacy(self):
        """点击隐私政策链接"""
        self.locator.find(self.SELECTORS["privacy_link"]).click()

    def get_social_links(self) -> list:
        """
        获取社交媒体链接

        Returns:
            链接文本列表
        """
        links = self.page.locator(self.SELECTORS["social_links"]).all()
        return [link.get_attribute("href") for link in links]

    def subscribe_newsletter(self, email: str):
        """
        订阅邮件通讯

        Args:
            email: 邮箱地址
        """
        self.locator.find(self.SELECTORS["newsletter_input"]).fill(email)
        self.locator.find(self.SELECTORS["newsletter_submit"]).click()

    def is_newsletter_input_visible(self) -> bool:
        """
        检查邮件订阅输入框是否可见

        Returns:
            是否可见
        """
        try:
            return self.locator.find(self.SELECTORS["newsletter_input"]).is_visible()
        except Exception:
            return False

    def get_footer_links(self) -> list:
        """
        获取底部所有链接

        Returns:
            链接文本列表
        """
        footer = self.locator.find(self.SELECTORS["footer_container"])
        links = footer.locator("a").all()
        return [link.text_content() for link in links if link.text_content()]
