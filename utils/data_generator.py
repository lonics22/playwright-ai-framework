"""测试数据生成工具"""
from typing import Dict, List, Optional
from faker import Faker
import random
import string


class DataGenerator:
    """测试数据生成器"""

    def __init__(self, locale: str = "zh_CN"):
        self.faker = Faker(locale)
        self.faker_en = Faker("en_US")

    def generate_user(self) -> Dict[str, str]:
        """
        生成用户数据

        Returns:
            用户数据字典
        """
        return {
            "username": self.faker.user_name(),
            "email": self.faker.email(),
            "password": self.generate_password(),
            "first_name": self.faker.first_name(),
            "last_name": self.faker.last_name(),
            "phone": self.faker.phone_number(),
            "address": self.faker.address(),
            "city": self.faker.city(),
            "postcode": self.faker.postcode(),
        }

    def generate_product(self) -> Dict[str, any]:
        """
        生成商品数据

        Returns:
            商品数据字典
        """
        return {
            "name": self.faker.catch_phrase(),
            "description": self.faker.text(max_nb_chars=200),
            "price": round(random.uniform(10, 1000), 2),
            "sku": self.generate_sku(),
            "category": self.faker.word(),
            "brand": self.faker.company(),
            "in_stock": random.choice([True, False]),
            "quantity": random.randint(0, 100),
        }

    def generate_order(self) -> Dict[str, any]:
        """
        生成订单数据

        Returns:
            订单数据字典
        """
        items_count = random.randint(1, 5)
        items = [self.generate_product() for _ in range(items_count)]
        total = sum(item["price"] for item in items)

        return {
            "order_id": self.generate_order_id(),
            "customer": self.generate_user(),
            "items": items,
            "total": round(total, 2),
            "status": random.choice(["pending", "processing", "shipped", "delivered"]),
            "payment_method": random.choice(["credit_card", "paypal", "alipay"]),
            "shipping_address": self.faker.address(),
            "created_at": self.faker.date_time_this_month().isoformat(),
        }

    def generate_credit_card(self) -> Dict[str, str]:
        """
        生成信用卡数据（测试用）

        Returns:
            信用卡数据字典
        """
        return {
            "number": self.faker.credit_card_number(),
            "holder": self.faker.name(),
            "expiry": self.faker.credit_card_expire(),
            "cvv": str(random.randint(100, 999)),
            "brand": self.faker.credit_card_provider(),
        }

    def generate_password(self, length: int = 12) -> str:
        """
        生成随机密码

        Args:
            length: 密码长度

        Returns:
            随机密码
        """
        characters = string.ascii_letters + string.digits + "!@#$%^&*"
        return ''.join(random.choice(characters) for _ in range(length))

    def generate_sku(self) -> str:
        """
        生成 SKU

        Returns:
            SKU 字符串
        """
        return f"SKU-{random.randint(10000, 99999)}-{random.randint(100, 999)}"

    def generate_order_id(self) -> str:
        """
        生成订单 ID

        Returns:
            订单 ID 字符串
        """
        timestamp = random.randint(1000000000, 9999999999)
        return f"ORD-{timestamp}"

    def generate_text(self, min_chars: int = 10, max_chars: int = 200) -> str:
        """
        生成随机文本

        Args:
            min_chars: 最小字符数
            max_chars: 最大字符数

        Returns:
            随机文本
        """
        return self.faker.text(max_nb_chars=max_chars)

    def generate_email(self, domain: str = None) -> str:
        """
        生成邮箱地址

        Args:
            domain: 指定域名

        Returns:
            邮箱地址
        """
        if domain:
            username = self.faker.user_name()
            return f"{username}@{domain}"
        return self.faker.email()

    def generate_phone(self) -> str:
        """
        生成手机号码

        Returns:
            手机号码
        """
        return self.faker.phone_number()

    def generate_address(self) -> Dict[str, str]:
        """
        生成地址信息

        Returns:
            地址数据字典
        """
        return {
            "street": self.faker.street_address(),
            "city": self.faker.city(),
            "state": self.faker.state(),
            "postcode": self.faker.postcode(),
            "country": self.faker.country(),
        }

    def generate_company(self) -> Dict[str, str]:
        """
        生成公司信息

        Returns:
            公司数据字典
        """
        return {
            "name": self.faker.company(),
            "catch_phrase": self.faker.catch_phrase(),
            "bs": self.faker.bs(),
            "address": self.faker.address(),
            "phone": self.faker.phone_number(),
            "email": self.faker.company_email(),
        }

    @staticmethod
    def generate_random_string(length: int = 10) -> str:
        """
        生成随机字符串

        Args:
            length: 长度

        Returns:
            随机字符串
        """
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    @staticmethod
    def generate_random_number(min_val: int = 0, max_val: int = 100) -> int:
        """
        生成随机数字

        Args:
            min_val: 最小值
            max_val: 最大值

        Returns:
            随机整数
        """
        return random.randint(min_val, max_val)

    @staticmethod
    def generate_random_choice(choices: List) -> any:
        """
        从列表中随机选择

        Args:
            choices: 选项列表

        Returns:
            随机选项
        """
        return random.choice(choices)


# 全局数据生成器实例
data_generator = DataGenerator()


# 快捷函数
def generate_user() -> Dict[str, str]:
    """生成用户数据"""
    return data_generator.generate_user()


def generate_product() -> Dict[str, any]:
    """生成商品数据"""
    return data_generator.generate_product()


def generate_order() -> Dict[str, any]:
    """生成订单数据"""
    return data_generator.generate_order()


def generate_credit_card() -> Dict[str, str]:
    """生成信用卡数据"""
    return data_generator.generate_credit_card()


def generate_password(length: int = 12) -> str:
    """生成随机密码"""
    return data_generator.generate_password(length)
