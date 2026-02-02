# -*- coding: utf-8 -*-
"""
DEMO FILE: Performance and Best Practices Issues for Copilot Review

このファイルは、GitHub Copilotのコードレビュー機能をデモンストレーションするために
意図的にパフォーマンス問題とベストプラクティス違反を含んでいます。
"""

import time
import json
import requests
from typing import List, Dict

# PERFORMANCE ISSUE: N+1 Query Pattern
class UserService:
    """ユーザーサービス - パフォーマンス問題あり"""
    
    def get_users_with_orders(self, user_ids: List[int]) -> List[Dict]:
        """
        ISSUE: N+1 クエリパターン
        各ユーザーに対して個別にAPI呼び出しを行っている
        """
        users = []
        for user_id in user_ids:  # ISSUE: ループ内でAPI呼び出し
            user = requests.get(f"https://api.example.com/users/{user_id}").json()
            # ISSUE: さらに各ユーザーの注文を個別に取得
            orders = requests.get(f"https://api.example.com/users/{user_id}/orders").json()
            user['orders'] = orders
            users.append(user)
        return users

# PERFORMANCE ISSUE: Inefficient string concatenation
def build_report(items: List[str]) -> str:
    """
    ISSUE: 大きなループでの文字列連結
    文字列の+=は非効率（毎回新しいオブジェクトを作成）
    """
    report = ""
    for item in items:
        report += f"Item: {item}\n"  # ISSUE: 非効率な文字列連結
        report += f"Status: Active\n"
        report += "---\n"
    return report

# PERFORMANCE ISSUE: Loading all data into memory
def process_large_file(filename: str):
    """
    ISSUE: 大きなファイルを一度にメモリに読み込む
    ファイルサイズが大きい場合、メモリ不足になる可能性
    """
    with open(filename, 'r') as f:
        lines = f.readlines()  # ISSUE: ファイル全体をメモリに読み込む
        
    processed = []
    for line in lines:
        # 重い処理
        processed.append(line.strip().upper())
    
    return processed

# PERFORMANCE ISSUE: Redundant calculations
def calculate_totals(items: List[Dict]) -> Dict:
    """
    ISSUE: 同じリストを複数回走査
    一度のループで計算できるものを分けている
    """
    total_price = sum([item['price'] for item in items])  # 1回目のループ
    total_quantity = sum([item['quantity'] for item in items])  # 2回目のループ
    average_price = sum([item['price'] for item in items]) / len(items)  # 3回目のループ（重複）
    
    return {
        'total_price': total_price,
        'total_quantity': total_quantity,
        'average_price': average_price
    }

# PERFORMANCE ISSUE: Creating unnecessary objects
def filter_active_users(users: List[Dict]) -> List[Dict]:
    """
    ISSUE: リストを複数回処理し、中間リストを作成
    """
    # 1回目: コピーを作成
    user_copies = [user.copy() for user in users]
    
    # 2回目: フィルタリング
    active_users = []
    for user in user_copies:
        if user.get('is_active'):
            active_users.append(user)
    
    # 3回目: ソート用の新しいリスト
    sorted_users = []
    for user in active_users:
        sorted_users.append(user)
    
    return sorted(sorted_users, key=lambda x: x['name'])

# BEST PRACTICE ISSUE: Not using context managers properly
def write_data_unsafe(filename: str, data: str):
    """
    ISSUE: リソースの適切な管理ができていない
    例外が発生した場合、ファイルが閉じられない可能性
    """
    file = open(filename, 'w')
    try:
        file.write(data)
    except Exception as e:
        print(f"Error: {e}")
    # ISSUE: finally句でcloseしていない
    file.close()

# BEST PRACTICE ISSUE: Not using built-in functions
def find_max_value(numbers: List[int]) -> int:
    """
    ISSUE: 組み込み関数max()を使わず、手動でループ
    """
    if not numbers:
        return None
    
    max_val = numbers[0]
    for num in numbers:
        if num > max_val:
            max_val = num
    return max_val

# PERFORMANCE ISSUE: Deep copying when not needed
def update_user_status(users: List[Dict], status: str) -> List[Dict]:
    """
    ISSUE: 不要なディープコピー
    元のデータを変更しない場合でも、全体をコピー
    """
    import copy
    users_copy = copy.deepcopy(users)  # ISSUE: 常にディープコピー
    
    for user in users_copy:
        user['status'] = status
    
    return users_copy

# BEST PRACTICE ISSUE: Not using enumerate
def add_indices(items: List[str]) -> List[Dict]:
    """
    ISSUE: enumerate()を使わず、手動でインデックスを管理
    """
    result = []
    index = 0
    for item in items:
        result.append({
            'index': index,
            'value': item
        })
        index += 1  # ISSUE: 手動でインクリメント
    return result

# PERFORMANCE ISSUE: Inefficient data structure usage
def check_duplicates(items: List[str]) -> bool:
    """
    ISSUE: リストで検索（O(n)）を繰り返す
    setを使えばO(1)で検索可能
    """
    seen = []  # ISSUE: リストを使用
    for item in items:
        if item in seen:  # ISSUE: リスト内検索はO(n)
            return True
        seen.append(item)
    return False

# BEST PRACTICE ISSUE: Not using dictionary get() method
def get_user_name(user: Dict) -> str:
    """
    ISSUE: get()メソッドを使わず、キーの存在チェック
    """
    if 'name' in user:
        return user['name']
    else:
        return 'Unknown'

# PERFORMANCE ISSUE: Sleeping in loops
def poll_api_status(url: str, max_attempts: int = 10):
    """
    ISSUE: ポーリングでの固定待機時間
    エクスポネンシャルバックオフを使用していない
    """
    for i in range(max_attempts):
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        time.sleep(5)  # ISSUE: 毎回同じ待機時間
    return None

# BEST PRACTICE ISSUE: Using mutable default arguments
def add_item_to_list(item: str, items: List[str] = []):  # ISSUE: ミュータブルなデフォルト引数
    """
    ISSUE: リストをデフォルト引数として使用
    呼び出し間で状態が共有される
    """
    items.append(item)
    return items

# PERFORMANCE ISSUE: Not using generator expressions
def process_large_dataset(data: List[int]) -> List[int]:
    """
    ISSUE: 大きなデータセットをリスト内包表記で一度に処理
    ジェネレーター式を使えばメモリ効率が良い
    """
    # ISSUE: 全結果を一度にメモリに保持
    results = [x * 2 for x in data if x > 0]
    
    # さらに別の処理でも全体をメモリに保持
    final_results = [x + 10 for x in results]
    
    return final_results

# BEST PRACTICE ISSUE: Not using pathlib
def join_paths_old_style(base: str, *parts: str) -> str:
    """
    ISSUE: 文字列結合でパスを構築
    pathlibを使うべき
    """
    import os
    path = base
    for part in parts:
        path = path + os.sep + part  # ISSUE: 文字列結合
    return path

# PERFORMANCE ISSUE: Repeatedly accessing dictionary keys
def calculate_user_score(user: Dict) -> float:
    """
    ISSUE: 同じ辞書キーに何度もアクセス
    """
    score = 0
    score += user['activity']['posts'] * 2
    score += user['activity']['comments'] * 1
    score += user['activity']['likes'] * 0.5
    
    if user['activity']['posts'] > 10:  # ISSUE: 再度アクセス
        score *= 1.5
    
    if user['activity']['comments'] > 50:  # ISSUE: 再度アクセス
        score *= 1.2
    
    return score
