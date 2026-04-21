"""API 调用工具"""
import requests
from typing import Dict, Any, Optional
from urllib.parse import urljoin
import json


class APIClient:
    """API 客户端"""

    def __init__(
        self,
        base_url: str,
        headers: Dict[str, str] = None,
        timeout: int = 30,
        verify_ssl: bool = True
    ):
        self.base_url = base_url.rstrip("/")
        self.headers = headers or {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def _build_url(self, endpoint: str) -> str:
        """构建完整 URL"""
        return urljoin(f"{self.base_url}/", endpoint.lstrip("/"))

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """处理响应"""
        try:
            return {
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "data": response.json() if response.text else None,
                "text": response.text,
                "success": response.ok
            }
        except json.JSONDecodeError:
            return {
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "data": None,
                "text": response.text,
                "success": response.ok
            }

    def get(
        self,
        endpoint: str,
        params: Dict[str, Any] = None,
        headers: Dict[str, str] = None
    ) -> Dict[str, Any]:
        """
        GET 请求

        Args:
            endpoint: API 端点
            params: 查询参数
            headers: 额外请求头

        Returns:
            响应数据
        """
        url = self._build_url(endpoint)
        request_headers = {**self.headers, **(headers or {})}

        response = self.session.get(
            url,
            params=params,
            headers=request_headers,
            timeout=self.timeout,
            verify=self.verify_ssl
        )

        return self._handle_response(response)

    def post(
        self,
        endpoint: str,
        data: Dict[str, Any] = None,
        json_data: Dict[str, Any] = None,
        headers: Dict[str, str] = None
    ) -> Dict[str, Any]:
        """
        POST 请求

        Args:
            endpoint: API 端点
            data: 表单数据
            json_data: JSON 数据
            headers: 额外请求头

        Returns:
            响应数据
        """
        url = self._build_url(endpoint)
        request_headers = {**self.headers, **(headers or {})}

        response = self.session.post(
            url,
            data=data,
            json=json_data,
            headers=request_headers,
            timeout=self.timeout,
            verify=self.verify_ssl
        )

        return self._handle_response(response)

    def put(
        self,
        endpoint: str,
        data: Dict[str, Any] = None,
        json_data: Dict[str, Any] = None,
        headers: Dict[str, str] = None
    ) -> Dict[str, Any]:
        """
        PUT 请求

        Args:
            endpoint: API 端点
            data: 表单数据
            json_data: JSON 数据
            headers: 额外请求头

        Returns:
            响应数据
        """
        url = self._build_url(endpoint)
        request_headers = {**self.headers, **(headers or {})}

        response = self.session.put(
            url,
            data=data,
            json=json_data,
            headers=request_headers,
            timeout=self.timeout,
            verify=self.verify_ssl
        )

        return self._handle_response(response)

    def delete(
        self,
        endpoint: str,
        headers: Dict[str, str] = None
    ) -> Dict[str, Any]:
        """
        DELETE 请求

        Args:
            endpoint: API 端点
            headers: 额外请求头

        Returns:
            响应数据
        """
        url = self._build_url(endpoint)
        request_headers = {**self.headers, **(headers or {})}

        response = self.session.delete(
            url,
            headers=request_headers,
            timeout=self.timeout,
            verify=self.verify_ssl
        )

        return self._handle_response(response)

    def patch(
        self,
        endpoint: str,
        data: Dict[str, Any] = None,
        json_data: Dict[str, Any] = None,
        headers: Dict[str, str] = None
    ) -> Dict[str, Any]:
        """
        PATCH 请求

        Args:
            endpoint: API 端点
            data: 表单数据
            json_data: JSON 数据
            headers: 额外请求头

        Returns:
            响应数据
        """
        url = self._build_url(endpoint)
        request_headers = {**self.headers, **(headers or {})}

        response = self.session.patch(
            url,
            data=data,
            json=json_data,
            headers=request_headers,
            timeout=self.timeout,
            verify=self.verify_ssl
        )

        return self._handle_response(response)

    def set_auth_token(self, token: str, token_type: str = "Bearer"):
        """
        设置认证 Token

        Args:
            token: 认证令牌
            token_type: Token 类型
        """
        self.session.headers["Authorization"] = f"{token_type} {token}"

    def clear_auth_token(self):
        """清除认证 Token"""
        self.session.headers.pop("Authorization", None)

    def set_header(self, key: str, value: str):
        """
        设置请求头

        Args:
            key: 头名称
            value: 头值
        """
        self.session.headers[key] = value

    def remove_header(self, key: str):
        """
        移除请求头

        Args:
            key: 头名称
        """
        self.session.headers.pop(key, None)

    def update_base_url(self, base_url: str):
        """
        更新基础 URL

        Args:
            base_url: 新的基础 URL
        """
        self.base_url = base_url.rstrip("/")

    def close(self):
        """关闭会话"""
        self.session.close()


class AuthenticatedAPIClient(APIClient):
    """带认证的 API 客户端"""

    def __init__(
        self,
        base_url: str,
        username: str = None,
        password: str = None,
        token: str = None,
        **kwargs
    ):
        super().__init__(base_url, **kwargs)
        self.username = username
        self.password = password
        self.token = token

        if token:
            self.set_auth_token(token)

    def login(self, username: str = None, password: str = None) -> bool:
        """
        登录获取 Token

        Args:
            username: 用户名
            password: 密码

        Returns:
            是否登录成功
        """
        user = username or self.username
        pwd = password or self.password

        if not user or not pwd:
            raise ValueError("Username and password are required")

        response = self.post("/auth/login", json_data={
            "username": user,
            "password": pwd
        })

        if response["success"] and response["data"]:
            token = response["data"].get("token") or response["data"].get("access_token")
            if token:
                self.set_auth_token(token)
                self.token = token
                return True

        return False

    def logout(self):
        """登出"""
        try:
            self.post("/auth/logout")
        finally:
            self.clear_auth_token()
            self.token = None
