"""页面头部组件"""
from playwright.sync_api import Page
from core.elements.smart_locator import SmartLocator


class Header:
    """页面头部组件"""

    # 选择器定义
    SELECTORS = {
        "logo": "header .logo, .header-logo, [data-testid='logo']",
        "nav_menu": "header nav, .nav-menu, [data-testid='nav-menu']",
        "search_box": "header input[type='search'], .search-box input, [data-testid='search-input']",
        "search_button": "header button[type='submit'], .search-button, [data-testid='search-button']",
        "user_menu": "header .user-menu, .user-dropdown, [data-testid='user-menu']",
        "login_link": "header a[href*='login'], .login-link, [data-testid='login-link']",
        "register_link": "header a[href*='register'], .register-link, [data-testid='register-link']",
        "cart_icon": "header .cart-icon, .shopping-cart, [data-testid='cart-icon']",
        "cart_count": "header .cart-count, .cart-badge, [data-testid='cart-count']",
    }

    def __init__(self, page: Page):
        self.page = page
        self.locator = SmartLocator(page)

    def click_logo(self):
        """点击 Logo 返回首页"""
        self.locator.find(self.SELECTORS["logo"]).click()

    def search(self, keyword: str):
        """
        在头部搜索框搜索

        Args:
            keyword: 搜索关键词
        """
        self.locator.find(self.SELECTORS["search_box"]).fill(keyword)
        self.locator.find(self.SELECTORS["search_button"]).click()

    def click_login(self):
        """点击登录链接"""
        self.locator.find(self.SELECTORS["login_link"]).click()

    def click_register(self):
        """点击注册链接"""
        self.locator.find(self.SELECTORS["register_link"]).click()

    def click_cart(self):
        """点击购物车图标"""
        self.locator.find(self.SELECTORS["cart_icon"]).click()

    def get_cart_count(self) -> int:
        """
        获取购物车商品数量

        Returns:
            商品数量
        """
        try:
            count_text = self.locator.find(self.SELECTORS["cart_count"]).text_content()
            return int(count_text) if count_text else 0
        except Exception:
            return 0

    def is_logged_in(self) -> bool:
        """
        检查用户是否已登录

        Returns:
            是否已登录
        """
        try:
            return self.locator.find(self.SELECTORS["user_menu"]).is_visible()
        except Exception:
            return False

    def click_user_menu(self):
        """点击用户菜单"""
        self.locator.find(self.SELECTORS["user_menu"]).click()

    def get_nav_items(self) -> list:
        """
        获取导航菜单项

        Returns:
            菜单项文本列表
        """
        nav = self.locator.find(self.SELECTORS["nav_menu"])
        items = nav.locator("a, li").all()
        return [item.text_content() for item in items]
