# -*- coding: utf-8 -*-
"""
DEMO FILE: Architecture and Design Pattern Issues

このファイルは、アーキテクチャとデザインパターンの問題を示すデモファイルです。
"""

from typing import Optional, List, Dict

# DESIGN ISSUE: God Class - クラスが多すぎる責任を持っている
class ApplicationManager:
    """
    ISSUE: 単一責任の原則違反
    このクラスは多すぎる責任を持っている
    """
    
    def __init__(self):
        self.users = []
        self.products = []
        self.orders = []
        self.payments = []
        self.inventory = {}
        self.notifications = []
    
    # ユーザー管理
    def create_user(self, name: str, email: str):
        """ISSUE: ユーザー管理の責任"""
        user = {'name': name, 'email': email}
        self.users.append(user)
        return user
    
    def validate_email(self, email: str) -> bool:
        """ISSUE: バリデーションロジックも含む"""
        return '@' in email
    
    # 商品管理
    def add_product(self, name: str, price: float):
        """ISSUE: 商品管理の責任"""
        product = {'name': name, 'price': price}
        self.products.append(product)
        return product
    
    def calculate_discount(self, price: float) -> float:
        """ISSUE: 価格計算ロジック"""
        return price * 0.9
    
    # 注文管理
    def create_order(self, user_id: int, product_id: int):
        """ISSUE: 注文処理の責任"""
        order = {'user_id': user_id, 'product_id': product_id}
        self.orders.append(order)
        return order
    
    # 支払い処理
    def process_payment(self, order_id: int, amount: float):
        """ISSUE: 支払い処理の責任"""
        payment = {'order_id': order_id, 'amount': amount}
        self.payments.append(payment)
        return payment
    
    # 在庫管理
    def update_inventory(self, product_id: int, quantity: int):
        """ISSUE: 在庫管理の責任"""
        self.inventory[product_id] = quantity
    
    # 通知送信
    def send_notification(self, user_id: int, message: str):
        """ISSUE: 通知機能の責任"""
        notification = {'user_id': user_id, 'message': message}
        self.notifications.append(notification)
    
    # データベース操作
    def save_to_database(self, data: Dict):
        """ISSUE: データアクセス層の責任も持っている"""
        # データベース保存処理
        pass
    
    # ログ記録
    def log_activity(self, activity: str):
        """ISSUE: ロギングの責任"""
        print(f"Activity: {activity}")

# DESIGN ISSUE: Tight Coupling - 密結合
class OrderProcessor:
    """ISSUE: 具体的なクラスに直接依存している"""
    
    def __init__(self):
        # ISSUE: ハードコーディングされた依存関係
        self.email_service = EmailService()  # 具体クラスに依存
        self.sms_service = SMSService()      # 具体クラスに依存
        self.payment_gateway = StripePayment()  # 具体クラスに依存
    
    def process(self, order: Dict):
        # 変更に弱い実装
        self.payment_gateway.charge(order['amount'])
        self.email_service.send(order['user_email'], "Order confirmed")
        self.sms_service.send(order['user_phone'], "Order confirmed")

class EmailService:
    def send(self, to: str, message: str):
        print(f"Email sent to {to}: {message}")

class SMSService:
    def send(self, to: str, message: str):
        print(f"SMS sent to {to}: {message}")

class StripePayment:
    def charge(self, amount: float):
        print(f"Charged {amount} via Stripe")

# DESIGN ISSUE: No Interface/Protocol - インターフェース不使用
class ReportGenerator:
    """
    ISSUE: インターフェースを定義していない
    異なる形式のレポートを柔軟に扱えない
    """
    
    def generate(self, data: Dict, format: str) -> str:
        # ISSUE: if-elseで形式を判定（Open/Closed原則違反）
        if format == "pdf":
            return self._generate_pdf(data)
        elif format == "excel":
            return self._generate_excel(data)
        elif format == "csv":
            return self._generate_csv(data)
        else:
            return ""
    
    def _generate_pdf(self, data: Dict) -> str:
        return "PDF content"
    
    def _generate_excel(self, data: Dict) -> str:
        return "Excel content"
    
    def _generate_csv(self, data: Dict) -> str:
        return "CSV content"

# DESIGN ISSUE: Anemic Domain Model - 貧血ドメインモデル
class Product:
    """
    ISSUE: データしか持たず、振る舞いがない
    ビジネスロジックが外部のサービスクラスに散在
    """
    def __init__(self, name: str, price: float, stock: int):
        self.name = name
        self.price = price
        self.stock = stock
        # ビジネスロジックがない

class ProductService:
    """ISSUE: ビジネスロジックがドメインモデルの外にある"""
    
    def calculate_final_price(self, product: Product, discount_rate: float) -> float:
        """ISSUE: 価格計算ロジックがProductクラス外にある"""
        return product.price * (1 - discount_rate)
    
    def is_available(self, product: Product) -> bool:
        """ISSUE: 在庫チェックロジックがProductクラス外にある"""
        return product.stock > 0
    
    def apply_promotion(self, product: Product) -> float:
        """ISSUE: プロモーションロジックも外部にある"""
        if product.stock > 100:
            return product.price * 0.9
        return product.price

# DESIGN ISSUE: Feature Envy - 他クラスのデータばかり使う
class InvoiceCalculator:
    """
    ISSUE: Orderクラスのデータばかり使っている
    このロジックはOrderクラスに属すべき
    """
    
    def calculate_total(self, order) -> float:
        """ISSUE: order.items, order.tax_rate, order.shipping_fee など、orderのデータばかり使う"""
        subtotal = sum(item.price * item.quantity for item in order.items)
        tax = subtotal * order.tax_rate
        total = subtotal + tax + order.shipping_fee
        
        if order.discount_code:
            total = total * (1 - order.discount_rate)
        
        return total

# DESIGN ISSUE: Circular Dependency - 循環依存
class UserRepository:
    """ISSUE: OrderRepositoryに依存"""
    def __init__(self):
        from .order_repository import OrderRepository
        self.order_repo = OrderRepository()  # 循環参照の可能性
    
    def get_user_with_orders(self, user_id: int):
        user = self._get_user(user_id)
        user.orders = self.order_repo.get_orders_by_user(user_id)
        return user
    
    def _get_user(self, user_id: int):
        return {'id': user_id, 'name': 'User'}

# DESIGN ISSUE: Primitive Obsession - プリミティブ型への執着
def create_user(name: str, email: str, phone: str, 
                address_line1: str, address_line2: str, 
                city: str, state: str, zip_code: str, country: str):
    """
    ISSUE: プリミティブ型ばかり使用
    Address、EmailAddress、PhoneNumberなどの値オブジェクトを作るべき
    """
    # 多すぎるパラメータ
    user = {
        'name': name,
        'email': email,
        'phone': phone,
        'address': {
            'line1': address_line1,
            'line2': address_line2,
            'city': city,
            'state': state,
            'zip': zip_code,
            'country': country
        }
    }
    return user

# DESIGN ISSUE: No Dependency Injection - DIなし
class NotificationService:
    """
    ISSUE: 依存関係がハードコーディング
    テストが困難
    """
    def __init__(self):
        # ISSUE: 内部で依存関係を生成
        self.email_sender = EmailSender()
        self.sms_sender = SMSSender()
        self.push_sender = PushNotificationSender()
    
    def notify(self, user: Dict, message: str):
        # ISSUE: 具体的な実装に依存
        self.email_sender.send(user['email'], message)
        self.sms_sender.send(user['phone'], message)
        self.push_sender.send(user['device_id'], message)

class EmailSender:
    def send(self, to: str, message: str):
        print(f"Email: {message}")

class SMSSender:
    def send(self, to: str, message: str):
        print(f"SMS: {message}")

class PushNotificationSender:
    def send(self, device_id: str, message: str):
        print(f"Push: {message}")

# DESIGN ISSUE: Magic Strings - マジック文字列
class UserValidator:
    """ISSUE: マジック文字列の使用"""
    
    def validate_role(self, role: str) -> bool:
        # ISSUE: ハードコーディングされた文字列
        return role in ["admin", "user", "guest", "moderator"]
    
    def validate_status(self, status: str) -> bool:
        # ISSUE: enumや定数を使うべき
        return status in ["active", "inactive", "suspended", "pending"]
