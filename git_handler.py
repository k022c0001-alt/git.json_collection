import os
import json
from IntentInspector import IntentInspector

class GitHandler:
    def __init__(self):
        # 自身のファイルがあるディレクトリを基準に、git_knowledgeフォルダのパスを指定
        self._dir = os.path.dirname(__file__)
        self.knowledge_dir = os.path.join(self._dir, "git_knowledge")

    def handle(self, message: str) -> str:
        """
        メッセージを受け取り、IntentInspectorで解析後、適切なGitナレッジを返す
        """
        # 1. IntentInspectorを使ってメッセージを解析
        inspector = IntentInspector(message)
        intent = inspector.inspect()

        # 2. 抽出されたターゲットやアクション、または元のメッセージからキーワードを取得
        # （IntentInspectorが抽出したtargetsや、生のメッセージを小文字にしたものを検索に使う）
        search_keywords = intent.get("targets", [])
        raw_query = message.lower()

        # 3. ナレッジの検索
        results = self._search_knowledge(raw_query, search_keywords)

        # 4. 結果のフォーマット
        if not results:
            return "申し訳ありません。git_knowledge フォルダから関連する情報を見つけられませんでした。別のキーワードで試してみてください。"

        return self._format_response(results)

    def _search_knowledge(self, raw_query: str, extracted_targets: list) -> list:
        """
        git_knowledgeフォルダ内のJSONを走査し、キーワードに一致するものを探す
        """
        if not os.path.exists(self.knowledge_dir):
            print(f"⚠️ [GitHandler] フォルダが見つかりません: {self.knowledge_dir}")
            return []

        matched_data = []
        for filename in os.listdir(self.knowledge_dir):
            if not filename.endswith(".json"):
                continue
            
            filepath = os.path.join(self.knowledge_dir, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                
                # 検索ロジック:
                # 1. JSON内のキーワードが、ユーザーの質問(raw_query)に含まれているか
                # 2. IntentInspectorが抽出したターゲットが、JSONのキーワードに含まれているか
                json_keywords = [kw.lower() for kw in data.get("keywords", [])]
                
                match_found = False
                for kw in json_keywords:
                    if kw in raw_query:
                        match_found = True
                        break
                
                if not match_found and extracted_targets:
                    for target in extracted_targets:
                        if target.lower() in json_keywords:
                            match_found = True
                            break
                
                if match_found:
                    matched_data.append(data)
            
            except Exception as e:
                print(f"⚠️ [GitHandler] {filename} の読み込みエラー: {e}")

        return matched_data

    def _format_response(self, results: list) -> str:
        """
        見つかったJSONデータを、ユーザーに読みやすいマークダウン形式に整形する
        """
        response_lines = ["Gitのナレッジから以下の情報が見つかりました：\n"]
        
        for data in results:
            response_lines.append(f"### {data.get('name', '無題のナレッジ')}")
            response_lines.append(f"**概要**: {data.get('description', '')}\n")
            
            problem = data.get("problem", {})
            if problem:
                response_lines.append(f"> **目的**: {problem.get('title', '')}")
            
            solutions = data.get("solutions", {})
            for step_key, step_info in solutions.items():
                response_lines.append(f"\n#### {step_key.capitalize()}: {step_info.get('title', '')}")
                response_lines.append(step_info.get('description', ''))
                commands = step_info.get('commands', [])
                if commands:
                    response_lines.append("```bash")
                    for cmd in commands:
                        response_lines.append(cmd)
                    response_lines.append("```")
            
            response_lines.append("\n---\n")

        return "\n".join(response_lines)
