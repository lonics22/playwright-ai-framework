"""截图辅助工具"""
import os
from typing import Optional, Tuple
from datetime import datetime
from pathlib import Path
from PIL import Image
import io


class ScreenshotHelper:
    """截图辅助工具类"""

    def __init__(self, output_dir: str = "reports/screenshots"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def save_screenshot(self, screenshot_bytes: bytes, name: str = None) -> str:
        """
        保存截图

        Args:
            screenshot_bytes: 截图字节数据
            name: 截图名称（可选）

        Returns:
            保存的文件路径
        """
        if name is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            name = f"screenshot_{timestamp}.png"

        filepath = self.output_dir / name

        with open(filepath, "wb") as f:
            f.write(screenshot_bytes)

        return str(filepath)

    def compare_screenshots(
        self,
        screenshot1_path: str,
        screenshot2_path: str,
        threshold: float = 0.95
    ) -> Tuple[bool, float]:
        """
        比较两张截图的相似度

        Args:
            screenshot1_path: 第一张截图路径
            screenshot2_path: 第二张截图路径
            threshold: 相似度阈值

        Returns:
            (是否相似, 相似度分数)
        """
        try:
            img1 = Image.open(screenshot1_path)
            img2 = Image.open(screenshot2_path)

            # 确保尺寸一致
            if img1.size != img2.size:
                img2 = img2.resize(img1.size)

            # 计算像素差异
            diff = 0
            pixels1 = img1.load()
            pixels2 = img2.load()

            for i in range(img1.width):
                for j in range(img1.height):
                    p1 = pixels1[i, j]
                    p2 = pixels2[i, j]
                    # 计算像素差异
                    pixel_diff = sum(abs(a - b) for a, b in zip(p1, p2))
                    if pixel_diff > 30:  # 阈值
                        diff += 1

            total_pixels = img1.width * img1.height
            similarity = 1 - (diff / total_pixels)

            return similarity >= threshold, similarity

        except Exception as e:
            print(f"截图比较失败: {e}")
            return False, 0.0

    def crop_screenshot(
        self,
        screenshot_path: str,
        box: Tuple[int, int, int, int],
        output_name: str = None
    ) -> str:
        """
        裁剪截图

        Args:
            screenshot_path: 截图路径
            box: 裁剪区域 (left, top, right, bottom)
            output_name: 输出文件名

        Returns:
            裁剪后的文件路径
        """
        img = Image.open(screenshot_path)
        cropped = img.crop(box)

        if output_name is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_name = f"cropped_{timestamp}.png"

        output_path = self.output_dir / output_name
        cropped.save(output_path)

        return str(output_path)

    def add_annotation(
        self,
        screenshot_path: str,
        text: str,
        position: Tuple[int, int] = (10, 10),
        output_name: str = None
    ) -> str:
        """
        在截图上添加文字标注

        Args:
            screenshot_path: 截图路径
            text: 标注文字
            position: 文字位置
            output_name: 输出文件名

        Returns:
            标注后的文件路径
        """
        from PIL import ImageDraw, ImageFont

        img = Image.open(screenshot_path)
        draw = ImageDraw.Draw(img)

        # 使用默认字体
        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except:
            font = ImageFont.load_default()

        # 添加文字（带背景）
        bbox = draw.textbbox(position, text, font=font)
        draw.rectangle(bbox, fill="yellow")
        draw.text(position, text, fill="red", font=font)

        if output_name is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_name = f"annotated_{timestamp}.png"

        output_path = self.output_dir / output_name
        img.save(output_path)

        return str(output_path)

    def highlight_element(
        self,
        screenshot_path: str,
        element_box: Tuple[int, int, int, int],
        output_name: str = None
    ) -> str:
        """
        高亮截图中的元素

        Args:
            screenshot_path: 截图路径
            element_box: 元素区域 (left, top, right, bottom)
            output_name: 输出文件名

        Returns:
            高亮后的文件路径
        """
        from PIL import ImageDraw

        img = Image.open(screenshot_path)
        draw = ImageDraw.Draw(img)

        # 绘制红色边框
        draw.rectangle(element_box, outline="red", width=3)

        if output_name is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_name = f"highlighted_{timestamp}.png"

        output_path = self.output_dir / output_name
        img.save(output_path)

        return str(output_path)

    def cleanup_old_screenshots(self, days: int = 7):
        """
        清理旧的截图文件

        Args:
            days: 保留天数
        """
        import time

        current_time = time.time()
        cutoff_time = current_time - (days * 24 * 60 * 60)

        for file in self.output_dir.glob("*.png"):
            if file.stat().st_mtime < cutoff_time:
                file.unlink()
